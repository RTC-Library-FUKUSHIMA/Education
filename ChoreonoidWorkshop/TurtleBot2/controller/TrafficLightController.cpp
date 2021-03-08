/*
 * TrafficLightController.cpp
 *
 *  Created on: 2020/02/18
 *      Author: Tsuyoshi Anazawa
 *
 *  $B35MW(B: AutoRaceCourse.body$B$N?.9f5!$N%i%$%H$r(B5$BICKh$KJQ99$9$k%W%m%0%i%`(B
 */

#include <cnoid/SimpleController>
#include <cnoid/SpotLight>

using namespace cnoid;
using namespace std;

class TrafficLightController : public SimpleController
{
	// Light$B3JG<JQ?t(B
	vector<SpotLight*> light;
	// Light$B$N?t(B
	static const int LIGHTNUM = 3;
	// Light$B$NL>>N(B
	string lightNames[LIGHTNUM] = { "RedLight", "YellowLight", "BlueLight" };
	// $B%7%s%W%k%3%s%H%m!<%iF~=PNO3JG<JQ?t(B
	SimpleControllerIO* io;
	// $B@Z$jBX$(;~4V(B
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
		// $B@Z$jBX$(%U%i%0(B
		bool changed = false;

		if((io->currentTime() - switchTime) >= 5.0){
			// $B%7%_%e%l!<%7%g%s;~4V$G(B5$BIC7P2a$7$?>l9g(B
			if(light[0]->on()){
				// $B@V?.9f$N>l9g(B
				light[0]->on(!light[0]->on());
				light[2]->on(!light[2]->on());
			}else if(light[1]->on()){
				// $B2+?'?.9f$N>l9g(B
				light[1]->on(!light[1]->on());
				light[0]->on(!light[0]->on());
			}else{
				// $B@D?.9f$N>l9g(B
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
