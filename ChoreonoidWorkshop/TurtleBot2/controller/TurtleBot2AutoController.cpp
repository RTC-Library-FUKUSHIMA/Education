/*
 * TurtleBotAutoController.cpp
 *
 *  Created on: 2019/04/17
 *      Author: Tsuyoshi Anazawa
 *
 *  概要: TurtleBot2モデルをAutoRaceCourse.bodyのコースにある白線と黄色線を
 *        取得しライントレース（自律走行）するプログラム
 */

#include <cnoid/SimpleController>
#include <cnoid/Camera>
#include <cnoid/RootItem>
#include <cnoid/SimulatorItem>
#include <fmt/format.h>
#include <fstream>

using namespace std;
using namespace cnoid;

class TurtleBot2AutoController : public SimpleController
{
	// ホイール数
	static const int WHEEL_NUM = 2;
	// bodyファイルに定義されたホイール名
	const string wheelNames[WHEEL_NUM] = { "wheel_left", "wheel_right" };
	// アクチュエーションモード格納変数
	Link::ActuationMode actuationMode;
	// ホイール格納配列
	Link* wheels[2];
	Link* rootLink;
	// タイムステップ格納変数
	double dt;
	// シンプルコントローラ入出力格納変数
	SimpleControllerIO* io;
	// Body情報格納変数
	Body* body;
	// カメラデバイス情報格納変数
	CameraPtr camera;
	// 前回の画像格納変数
	std::shared_ptr<const Image> prevImage;
	// 画像内のグレー、白、黄色の数の格納変数
	int cnt[3] = { 0, 0, 0 };
	// トレッド幅/2(車体の中心から車輪までの距離)
	const double d = 0.115;
	// PID制御の係数
	const double Kp = 48.0;
	const double Ki = 0.002;
	const double Kd = 0.0007;
	// 画像内の白、黄色の線の目標値
	static const int TARGET = 1700;
	// 前回と現在の偏差値格納変数
	double diff_R[2] = { 0, 0 };
	double diff_L[2] = { 0, 0 };
	// 偏差の積分値格納変数
	double integral[2] = { 0, 0 };
	// 偏差の微分値格納変数
	double derivation[2] = { 0, 0 };
	double startTime, waitTime;
	const double INTERVAL = 0.1;
	// ファイル出力ストリーム
	ofstream ofs;
	FILE* fp;
	// バッファサイズ
	static const int BUF_SIZE = 100;
	char str[BUF_SIZE];
	// カレントディレクトリ取得コマンド
	string cmd = "cd; cd choreonoid/ext/Education/ChoreonoidWorkshop/TurtleBot2/plot/; pwd | tr '\n' '/'";
	// ファイルパス
	string filePath = "";
	const string FILENAME = "plot.tsv";
	// シグナル設定状態取得変数
	ScopedConnection cameraConnection;

public:
	virtual bool initialize(SimpleControllerIO* io) override
	{
		// ioオブジェクトの取得
		this->io = io;
		// 出力ストリームの取得
		ostream& os = io->os();
		// Bodyの取得
		body = io->body();

		// アクチュエーションモードの初期化
		actuationMode = Link::JOINT_TORQUE;
		// コントローラオプションの取得
		string option = io->optionString();

		if(!option.empty()){
			// コントローラオプションが入力されている場合
			if(option == "velocity" || option == "position"){
				// velocity または positionの場合
				actuationMode = Link::JOINT_VELOCITY;
			} else if(option == "torque"){
				// torqueの場合
				actuationMode = Link::JOINT_TORQUE;
			} else {
				// それ以外の場合
				os << fmt::format("Warning: Unknown option \"{}\".", option) << endl;
			}
		}

		for(int i = 0; i < WHEEL_NUM; ++i){
			// 配列にホイールリンクを格納
			wheels[i] = body->link(wheelNames[i]);
			if(!wheels[i]){
				// リンクが取得できなかった場合
				os << fmt::format("{0} of {1} is not found.", wheelNames[i], body->name()) << endl;
				return false;
			}

			// リンクのアクチュエーションモードの設定
			wheels[i]->setActuationMode(actuationMode);
			// ホイールリンクへコントローラからの出力を有効化
			io->enableOutput(wheels[i]);
		}

		// TurtleBot2のコントローラへの入力を有効化
		rootLink = body->link("kobuki");
		rootLink->setActuationMode(Link::LINK_POSITION);
		io->enableInput(rootLink);

		// LineTraceカメラを取得
		camera = body->findDevice<Camera>("LineTrace");
		// カメラのコントローラへの入力を有効化
		io->enableInput(camera);
		// 接続の切断
		cameraConnection.disconnect();
		// センサの状態が変わった場合、onCameraStateChanged()を呼び出す
		cameraConnection = camera->sigStateChanged().connect(
				[&](){ onCameraStateChanged(); });
		// タイムステップの設定
		dt = io->timeStep();

		if((fp = popen(cmd.c_str(), "r")) != NULL){
			// プロセスをオープンしコマンドを実行
			while(fgets(str, sizeof(str), fp) != NULL){
				// コマンド結果を1行ずつ読み込む
				// カレントディレクトリの取得
				filePath += str;
			}
			// プロセスをクローズ
			pclose(fp);
		}
		io->os() << filePath << endl;

		// ディレクトリ名とファイル名を連結
		filePath = filePath + FILENAME;

		ofs.open(filePath, ios::out);
		startTime = 0.0;

		return true;
	}

	virtual bool control() override
	{
		// 車体の中心の速度vx(m/s), 旋回角速度va(rad/s)
		double vx, va;
		va = 0.5;
		vx = 0.3;

		// 前回の偏差値を設定
		diff_L[0] = diff_L[1];
		// 現在の偏差値(目標値 - センサ値)を取得(センサで黄色の割合を取得)
		diff_L[1] = TARGET - cnt[2];
		// 偏差の積分値を取得。偏差の積分値 = (( 最新の偏差 + 前回の偏差 ) / 2 ) * 時間
		//                                = 偏差の平均 * 時間
		integral[0] += (diff_L[1] + diff_L[0]) / 2.0 * dt;
		// 偏差の微分値を取得。偏差の微分値 = ( 最新の偏差 - 前回の偏差 ) / 時間
		derivation[0] = (diff_L[1] - diff_L[0]) / dt;

		diff_R[0] = diff_R[1];
		// 現在の偏差値(目標値 - センサ値)を取得(センサで白の割合を取得)
		diff_R[1] = -(TARGET - cnt[1]);
		integral[1] += (diff_R[1] + diff_R[0]) / 2.0 * dt;
		derivation[1] = (diff_R[1] - diff_R[0]) / dt;

		if(actuationMode == Link::JOINT_VELOCITY){
			// アクチュエーションモードがvelocityの場合
			// 関節速度の指令値格納変数
			double dq_target[2];
			// 右車輪の角速度を Wr, 左車輪の角速度を Wl
			// 右車輪の速度を Vr, 左車輪の速度を Vl
			// 車輪の半径を r、中心から車輪までの距離(トレッドの 1/2)を d
			// Wr = (vx + va * d) / r
			// Wl = (vx - va * d) / r
			// r: 0.038(m), d: 0.115(m)
			// Wr = (vx + va * 0.115) / 0.038
			// Wl = (vx - va * 0.115) / 0.038
			// Vr = vx + va * 0.115
			// Vl = vx - va * 0.115

			// PID制御
			dq_target[0] = Kp * (vx - (va * d * diff_L[1] / 500)) + Ki * (integral[0] * va * d) + Kd * (derivation[0] * va * d);
			dq_target[1] = Kp * (vx + (va * d * diff_R[1] / 500)) + Ki * (integral[1] * va * d) + Kd * (derivation[1] * va * d);

			// 左右のホイールに指令値を与える
			wheels[0]->dq_target() = dq_target[0];
			wheels[1]->dq_target() = dq_target[1];

			// 黄色と白の線がなくなったら停止
			if(cnt[1] == 0 and cnt[2] == 0){
				wheels[0]->dq_target() = 0.0;
				wheels[1]->dq_target() = 0.0;
			}
		}

		waitTime = io->currentTime() - startTime;
		// 0.5s毎にファイル出力を行う
		if(waitTime >= INTERVAL){
			ofs << io->currentTime() << "\t" << rootLink->position().translation().x() << "\t" << rootLink->position().translation().y() << "\t" << endl;
			startTime = io->currentTime();
		}

		return true;
	}

	virtual void stop() override
	{
		for(int i = 0; i < WHEEL_NUM; ++i){
			diff_R[i] = diff_L[i] = 0;
			integral[i] = derivation[i] = 0;
		}

		for(int i = 0; i < 3; ++i){
			cnt[i] = 0;
		}

		cameraConnection.disconnect();
		ofs.close();
	}

	void onCameraStateChanged()
	{
		size_t length = 0;
		if(camera->sharedImage() != prevImage){
			// カメラ画像が更新されたか確認
			const Image& image = camera->constImage();
			if(!image.empty()){
				// カメラ画像が取得できた場合
				int width, height;
				// 画像のサイズを取得
				height = image.height();
				width = image.width();
				length = width * height * image.numComponents() * sizeof(unsigned char);
			}

			// 画像の1ピクセルごとのデータを取得
			unsigned char* src = (unsigned char*)image.pixels();

			// グレー、白、黄色のカウント用配列の初期化
			cnt[0] = cnt[1] = cnt[2] = 0;
			// RGB値格納配列
			int rgb[3];

			// データ数分ループ
			for(int i = 0; i < length / 3; ++i){
				// RGBの値を格納
				rgb[0] = (int)src[i * 3];
				rgb[1] = (int)src[i * 3 + 1];
				rgb[2] = (int)src[i * 3 + 2];

				if((rgb[0] >= 100 and rgb[0] < 180)
						and (rgb[1] >= 100 and rgb[1] < 180)
						and (rgb[2] >= 100 and rgb[2] < 180)
						and abs(rgb[0] - rgb[1]) <= 10
						and abs(rgb[1] - rgb[2]) <= 10
						and abs(rgb[2] - rgb[0]) <= 10){
					// グレーの個数をカウント
					cnt[0]++;
				}else if(rgb[0] >= 180 and rgb[1] >= 180 and rgb[2] >= 180){
					// 白の個数をカウント
					cnt[1]++;
				}else if(rgb[0] >= 170 and rgb[1] >= 170 and rgb[2] <= 100){
					// 黄色の個数をカウント
					cnt[2]++;
				}
			}
			// 前回値の更新
			prevImage = camera->sharedImage();
		}
	}
};

CNOID_IMPLEMENT_SIMPLE_CONTROLLER_FACTORY(TurtleBot2AutoController)

