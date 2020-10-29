/*
 * TurtleBotJoystickController.cpp
 *
 *  Created on: 2019/04/17
 *      Author: Tsuyoshi Anazawa
 *
 *  概要: TurtleBot2モデルをPS4コントローラや仮想ジョイスティックを用いて
 *        動作させるプログラム
 */

#include <cnoid/SimpleController>
#include <cnoid/Joystick>
#include <fmt/format.h>

using namespace std;
using namespace cnoid;
using fmt::format;

class TurtleBot2JoystickController : public SimpleController
{
	// ホイール数格納定数
	static const int WHEEL_NUM = 2;
	// bodyファイルに定義されたホイール名格納配列
	const string wheelNames[WHEEL_NUM] = { "wheel_left", "wheel_right" };
	// リンクのアクチュエーションモード格納変数
	Link::ActuationMode actuationMode;
	// ホイール格納配列
	Link* wheels[2];
	// ジョイスティック情報格納変数
	Joystick joystick;
	// Body情報格納変数
	Body* body;

public:
	virtual bool initialize(SimpleControllerIO* io) override
	{
		ostream& os = io->os();
		// Bodyの取得
		body = io->body();

		// アクチュエーションモードの初期化
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
				// 上記以外の場合
				os << format("Warning: Unknown option \"{}\".", option) << endl;
			}
		}

		for(int i = 0; i < WHEEL_NUM; ++i){
			// 配列にホイールリンクを格納
			wheels[i] = body->link(wheelNames[i]);
			if(!wheels[i]){
				// リンクが取得できない場合
				os << format("{0} of {1} is not found.", wheelNames[i], body->name()) << endl;
				return false;
			}

			// リンクのアクチュエーションモードを設定
			wheels[i]->setActuationMode(actuationMode);
			// ホイールへの出力を有効化
			io->enableOutput(wheels[i]);
		}

		return true;
	}

	virtual bool control() override
	{
		// ジョイスティックの状態取得
		joystick.readCurrentState();

		double pos[2];		// ジョイスティックの変化量格納変数.
		for(int i = 0; i < 2; ++i){
			// ジョイスティックの値取得
			pos[i] = joystick.getPosition(
					i == 0 ? Joystick::L_STICK_H_AXIS : Joystick::L_STICK_V_AXIS);

			if(fabs(pos[i]) < 0.2){
				// 変化量の絶対値が0.2未満の場合
				pos[i] = 0.0;
			}
		}

		if(actuationMode == Link::JOINT_VELOCITY){
			// アクチュエーションモードが velocityの場合
			static const double K = 20.0;
			wheels[0]->dq_target() = K * (-pos[1] + pos[0]);
			wheels[1]->dq_target() = K * (-pos[1] - pos[0]);
		}

		return true;
	}
};

CNOID_IMPLEMENT_SIMPLE_CONTROLLER_FACTORY(TurtleBot2JoystickController)

