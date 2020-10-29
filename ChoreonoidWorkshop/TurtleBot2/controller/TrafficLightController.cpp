/*
 * TrafficLightController.cpp
 *
 *  Created on: 2020/02/18
 *      Author: Tsuyoshi Anazawa
 *
 *  概要: AutoRaceCourse.bodyの信号機のライトを5秒毎に変更するプログラム
 */

#include <cnoid/SimpleController>
#include <cnoid/SpotLight>
#include <cnoid/RootItem>
#include <cnoid/SimulatorItem>
#include <fmt/format.h>
#include <iostream>

using namespace cnoid;
using namespace std;

class TrafficLightController : public SimpleController
{
	// Light格納変数
	vector<SpotLight*> light;
	// Lightの数
	static const int LIGHTNUM = 3;
	// Lightの名称
	string lightNames[LIGHTNUM] = { "RedLight", "YellowLight", "BlueLight" };
	// シンプルコントローラ入出力格納変数
	SimpleControllerIO* io;
	// 切り替え時間
	double simTime;
	double switchTime;
	bool onFlg;

public:
	virtual bool initialize(SimpleControllerIO* io) override
	{
		this->io = io;

		for(int i = 0; i < LIGHTNUM; ++i){
			onFlg = false;
			light.push_back(io->body()->findDevice<SpotLight>(lightNames[i]));

			if(i == 0){
				onFlg = true;
			}
			light[i]->on(onFlg);
			light[i]->notifyStateChange();
		}

		switchTime = 0.0;

		return true;
	}

	virtual bool control() override
	{
		// 切り替えフラグ
		bool changed = false;

		if((io->currentTime() - switchTime) >= 5.0){
			// シミュレーション時間で5秒経過した場合
			if(light[0]->on()){
				// 赤信号の場合
				light[0]->on(!light[0]->on());
				light[2]->on(!light[2]->on());
			}else if(light[1]->on()){
				// 黄色信号の場合
				light[1]->on(!light[1]->on());
				light[0]->on(!light[0]->on());
			}else{
				// 青信号の場合
				light[2]->on(!light[2]->on());
				light[1]->on(!light[1]->on());
			}
			changed = true;
			switchTime += 5.0;
		}

		if(changed){
			for(int i = 0; i < LIGHTNUM; ++i){
				light[i]->notifyStateChange();
			}
		}

		return true;
	}
};

CNOID_IMPLEMENT_SIMPLE_CONTROLLER_FACTORY(TrafficLightController)
