/*
 * TurtleBotJoystickController.cpp
 *
 *  Created on: 2019/12/16
 *      Author: Tsuyoshi Anazawa
 *
 *  概要: TurtleBot2モデルを前進させ2秒後に停止させるプログラム
 */

#include <cnoid/SimpleController>
#include <fmt/format.h>

using namespace std;
using namespace cnoid;

class TurtleBot2StraightController : public SimpleController
{
	// ホイール数
	static const int WHEEL_NUM = 2;
	// bodyファイルに定義されたホイール名
	const string wheelNames[WHEEL_NUM] = { "wheel_left", "wheel_right" };
	// アクチュエーションモード格納変数
	Link::ActuationMode actuationMode;
	// ホイール格納配列
	Link* wheels[2];
	// シンプルコントローラ入出力格納変数
	SimpleControllerIO* io;
	// Body情報格納変数
	Body* body;
	// 開始時間格納変数
	double startTime;
	// トレッド幅/2(車体の中心から車輪までの距離)
	const double d = 0.115;
	// 比例係数
	double Kp = 48.0;

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

		for(auto& option : io->options()){
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
//					os << fmt::format("Warning: Unknown option \"{}\".", option) << endl;
					Kp = stoi(option);
				}
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

		// 開始時間の初期化
		startTime = 0.0;

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

			if(startTime == 0.0){
				// 開始時間が0.0の場合
				// 開始時間に現在のシミュレーション時間を設定
				startTime = io->currentTime();

			}

			if(io->currentTime() - startTime > 2.0){
				// 現在のシミュレーション時間 - 開始時間が2.0より大きい場合
				// 左右のホイールの指令値を0.0に設定
				wheels[0]->dq_target() = 0.0;
				wheels[1]->dq_target() = 0.0;

			}else{
				dq_target[0] = Kp * (vx - va * d);
				dq_target[1] = Kp * (vx + va * d);
				// 左右のホイールに指令値を与える
				wheels[0]->dq_target() = dq_target[0];
				wheels[1]->dq_target() = dq_target[1];
			}
		}

		return true;
	}
};

CNOID_IMPLEMENT_SIMPLE_CONTROLLER_FACTORY(TurtleBot2StraightController)
