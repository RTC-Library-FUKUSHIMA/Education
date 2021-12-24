/*
 * TurtleBot2StopLineController.cpp
 *
 *  Created on: 2020/01/23
 *      Author: Tsuyoshi Anazawa
 *
 *  概要: TurtleBot2モデル前進させ白線上で停止させるプログラム
 */

#include <cnoid/SimpleController>
#include <cnoid/Camera>
#include <fmt/format.h>

using namespace std;
using namespace cnoid;

class TurtleBot2StopLineController : public SimpleController
{
	// ホイール数
	static const int WHEEL_NUM = 2;
	// bodyファイルに定義されたホイール名
	const string wheelNames[WHEEL_NUM] = { "wheel_left", "wheel_right" };
	// アクチュエーションモード格納変数
	Link::ActuationMode actuationMode;
	// ホイール格納配列
	Link* wheels[2];
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
	// 画像内の白線の目標値
	static const int TARGET = 15000;
	// シグナル設定状態取得変数
	ScopedConnection cameraConnection;

public:
	virtual bool initialize(SimpleControllerIO* io) override
	{
		ostream& os = io->os();
		// Bodyの取得
		body = io->body();

		// リンクのアクチュエーションモードの初期化
		actuationMode = Link::JOINT_TORQUE;
		// コントローラオプションの取得
		string option = io->optionString();

		if(!option.empty()){
			// コントローラオプションが空の場合
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

		// LineTraceカメラを取得
		camera = body->findDevice<Camera>("LineTrace");
		// カメラのコントローラへの入力を有効化
		io->enableInput(camera);
		// 接続の切断
		cameraConnection.disconnect();
		// センサの状態が変わった場合、onCameraStateChanged()を呼び出す
		cameraConnection = camera->sigStateChanged().connect(
				[&](){ onCameraStateChanged(); });

		return true;
	}

	virtual bool control() override
	{
		// 車体の中心の速度vx(m/s), 旋回角速度va(rad/s)
		double vx, va;
		va = 0.0;
		vx = 0.3;

		if(actuationMode == Link::JOINT_VELOCITY){
			// アクチュエーションモードがvelocityの場合
			// 関節速度の指令値格納変数
			double dq_target[2];

			dq_target[0] = Kp * (vx - va * d);
			dq_target[1] = Kp * (vx + va * d);

			// 左右のホイールに指令値を与える
			wheels[0]->dq_target() = dq_target[0];
			wheels[1]->dq_target() = dq_target[1];

			if(cnt[1] > TARGET){
				// 白線が近くなったら停止
				wheels[0]->dq_target() = 0.0;
				wheels[1]->dq_target() = 0.0;
			}
		}
		return true;
	}

	virtual void stop() override
	{
		for(int i = 0; i < 3; ++i){
			cnt[i] = 0;
		}
		cameraConnection.disconnect();
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

				if((rgb[0] >= 100 && rgb[0] < 180)
						&& (rgb[1] >= 100 && rgb[1] < 180)
						&& (rgb[2] >= 100 && rgb[2] < 180)
						&& abs(rgb[0] - rgb[1]) <= 10
						&& abs(rgb[1] - rgb[2]) <= 10
						&& abs(rgb[2] - rgb[0]) <= 10){
					// グレーの個数をカウント
					cnt[0]++;
				}else if(rgb[0] >= 180 && rgb[1] >= 180 && rgb[2] >= 180){
					// 白の個数をカウント
					cnt[1]++;
				}else if(rgb[0] >= 170 && rgb[1] >= 170 && rgb[2] <= 100){
					// 黄色の個数をカウント
					cnt[2]++;
				}
			}
			// 前回値の更新
			prevImage = camera->sharedImage();
		}
	}
};

CNOID_IMPLEMENT_SIMPLE_CONTROLLER_FACTORY(TurtleBot2StopLineController)

