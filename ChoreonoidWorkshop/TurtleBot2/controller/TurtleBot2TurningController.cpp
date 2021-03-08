/*
 * TurtleBot2TurningController.cpp
 *
 *  Created on: 2019/12/16
 *      Author: Tsuyoshi Anazawa
 *
 *  概要: TurtleBot2モデルを"2秒間前進"→"90°右旋回"→"2秒間前進"→90°左旋回
 *        →"2秒間前進"→"停止"させるプログラム
 */

#include <cnoid/SimpleController>
#include <fmt/format.h>

using namespace std;
using namespace cnoid;

class TurtleBot2TurningController : public SimpleController
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
	// トレッド/2(車体の中心から車輪までの距離)
	const double d = 0.115;
	// 比例係数
	const double Kp = 48.0;
	// 開始時間
	double startTime = 0.0;

public:
	virtual bool initialize(SimpleControllerIO* io) override
	{
		// ioオブジェクトの取得
		this->io = io;
		// 出力ストリームの取得
		ostream& os = io->os();
		// Bodyの取得
		body = io->body();

		// リンクのアクチュエーションモード設定
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
		
		startTime = io->currentTime();
		return true;
	}

	virtual bool control() override
	{
		// 車体の中心の速度vx(m/s), 旋回角速度va(rad/s)
		double vx, va;

		if(io->currentTime() - startTime < 2.0){
			// シミュレーション時間が2s未満の場合、直進
			va = 0.0;
			vx = 0.3;
		} else if(io->currentTime() - startTime < 2.2){
			va = vx = 0.0;
		} else if(io->currentTime() - startTime < 2.7){
			// 0.5s間右旋回
			va = -2.1;
			vx = 0.0;
		} else if(io->currentTime() - startTime < 2.9){
			va = vx = 0.0;
		} else if(io->currentTime() - startTime < 4.9){
			// 2s間直進
			va = 0.0;
			vx = 0.3;
		} else if(io->currentTime() - startTime < 5.1){
			va = vx = 0.0;
		} else if(io->currentTime() - startTime < 5.6){
			// 0.5s間左旋回
			va = 2.1;
			vx = 0.0;
		} else if(io->currentTime() - startTime < 5.8){
			va = vx = 0.0;
		} else if(io->currentTime() - startTime < 7.8){
			// 2s間直進
			va = 0.0;
			vx = 0.3;
		} else {
			// 停止
			va = vx = 0.0;
		}

		if(actuationMode == Link::JOINT_VELOCITY){
			// アクチュエーションモードがvelocityの場合
			// 関節速度の指令値格納変数
			double dq_target[2];

			dq_target[0] = Kp * (vx - va * d);
			dq_target[1] = Kp * (vx + va * d);
			// 左右のホイールに指令値を与える
			wheels[0]->dq_target() = dq_target[0];
			wheels[1]->dq_target() = dq_target[1];
		}

		return true;
	}
};

CNOID_IMPLEMENT_SIMPLE_CONTROLLER_FACTORY(TurtleBot2TurningController)
