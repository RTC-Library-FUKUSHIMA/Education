/*
 * TurtleBot2TurnLineController.cpp
 *
 *  Created on: 2020/01/23
 *      Author: Tsuyoshi Anazawa
 *
 *  $B35MW(B: TurtleBot2$B%b%G%k$rGr@~$r<hF@$7%i%$%s%H%l!<%9!J<+N'Av9T!K$9$k%W%m%0%i%`(B
 */

#include <cnoid/SimpleController>
#include <cnoid/Camera>
#include <fmt/format.h>
#include <iostream>

using namespace std;
using namespace cnoid;

class TurtleBot2TurnLineController : public SimpleController
{
	// $B%[%$!<%k?t(B
	static const int WHEEL_NUM = 2;
	// body$B%U%!%$%k$KDj5A$5$l$?%[%$!<%kL>(B
	const string wheelNames[WHEEL_NUM] = { "wheel_left", "wheel_right" };
	// $B%"%/%A%e%(!<%7%g%s%b!<%I3JG<JQ?t(B
	Link::ActuationMode actuationMode;
	// $B%[%$!<%k3JG<G[Ns(B
	Link* wheels[2];
	// $B%?%$%`%9%F%C%W3JG<JQ?t(B
	double dt;
	// Body$B>pJs3JG<JQ?t(B
	Body* body;
	// $B%+%a%i%G%P%$%9>pJs3JG<JQ?t(B
	CameraPtr camera;
	// $BA02s$N2hA|3JG<JQ?t(B
	std::shared_ptr<const Image> prevImage;
	// $B2hA|Fb$N%0%l!<!"Gr!"2+?'$N?t$N3JG<JQ?t(B
	int cnt[3] = { 0, 0, 0 };
	// $B%H%l%C%II}(B/2($B<VBN$NCf?4$+$i<VNX$^$G$N5wN%(B)
	const double d = 0.115;
	// PID$B@)8f$N78?t(B
	const double Kp = 48.0;
	const double Ki = 0.009;
	const double Kd = 0.00015;
	// $B2hA|Fb$NGr@~$NL\I8CM(B
	static const int TARGET = 10000; //6000;
	// $BA02s$H8=:_$NJP:9CM3JG<JQ?t(B
	double diff_R[2] = { 0, 0 };
	double diff_L[2] = { 0, 0 };
	// $BJP:9$N@QJ,CM3JG<JQ?t(B
	double integral[2] = { 0, 0 };
	// $BJP:9$NHyJ,CM3JG<JQ?t(B
	double derivation[2] = { 0, 0 };
	// $B%7%0%J%k@_Dj>uBV<hF@JQ?t(B
	ScopedConnection cameraConnection;

public:
	virtual bool initialize(SimpleControllerIO* io) override
	{
		ostream& os = io->os();
		// Body$B$N<hF@(B
		body = io->body();

		// $B%j%s%/$N%"%/%A%e%(!<%7%g%s%b!<%I$N=i4|2=(B
		actuationMode = Link::JOINT_TORQUE;
		// $B%3%s%H%m!<%i%*%W%7%g%s$N<hF@(B
		string option = io->optionString();

		if(!option.empty()){
			// $B%3%s%H%m!<%i%*%W%7%g%s$,F~NO$5$l$F$$$k>l9g(B
			if(option == "velocity" || option == "position"){
				// velocity $B$^$?$O(B position$B$N>l9g(B
				actuationMode = Link::JOINT_VELOCITY;
			} else if(option == "torque"){
				// torque$B$N>l9g(B
				actuationMode = Link::JOINT_TORQUE;
			} else {
				// $B$=$l0J30$N>l9g(B
				os << fmt::format("Warning: Unknown option \"{}\".", option) << endl;
			}
		}

		for(int i = 0; i < WHEEL_NUM; ++i){
			// $BG[Ns$K%[%$!<%k%j%s%/$r3JG<(B
			wheels[i] = body->link(wheelNames[i]);
			if(!wheels[i]){
				// $B%j%s%/$,<hF@$G$-$J$+$C$?>l9g(B
				os << fmt::format("{0} of {1} is not found.", wheelNames[i], body->name()) << endl;
				return false;
			}

			// $B%j%s%/$N%"%/%A%e%(!<%7%g%s%b!<%I$N@_Dj(B
			wheels[i]->setActuationMode(actuationMode);
			// $B%[%$!<%k%j%s%/$X%3%s%H%m!<%i$+$i$N=PNO$rM-8z2=(B
			io->enableOutput(wheels[i]);
		}

		// LineTrace$B%+%a%i$r<hF@(B
		camera = body->findDevice<Camera>("LineTrace");
		// $B%+%a%i$N%3%s%H%m!<%i$X$NF~NO$rM-8z2=(B
		io->enableInput(camera);
		// $B@\B3$N@ZCG(B
		cameraConnection.disconnect();
		// $B%;%s%5$N>uBV$,JQ$o$C$?>l9g!"(BonCameraStateChanged()$B$r8F$S=P$9(B
		cameraConnection = camera->sigStateChanged().connect(
				[&](){ onCameraStateChanged(); });
		// $B%?%$%`%9%F%C%W$N@_Dj(B
		dt = io->timeStep();

		return true;
	}

	virtual bool control() override
	{
		// $B<VBN$NCf?4$NB.EY(Bvx(m/s), $B@{2s3QB.EY(Bva(rad/s)
		double vx, va;
		va = 0.5;
		vx = 0.3;

		// $BA02s$NJP:9CM$r@_Dj(B
		diff_L[0] = diff_L[1];
		// $B8=:_$NJP:9CM(B($BL\I8CM(B - $B%;%s%5CM(B)$B$r<hF@(B($B%;%s%5$G2+?'$N3d9g$r<hF@(B)
		diff_L[1] = (TARGET - cnt[1]) / 2500;
		// $BJP:9$N@QJ,CM$r<hF@!#JP:9$N@QJ,CM(B = (( $B:G?7$NJP:9(B + $BA02s$NJP:9(B ) / 2 ) * $B;~4V(B
		//                                = $BJP:9$NJ?6Q(B * $B;~4V(B
		integral[0] += (diff_L[1] + diff_L[0]) / 2.0 * dt;
		// $BJP:9$NHyJ,CM$r<hF@!#JP:9$NHyJ,CM(B = ( $B:G?7$NJP:9(B - $BA02s$NJP:9(B ) / $B;~4V(B
		derivation[0] = (diff_L[1] - diff_L[0]) / dt;

		diff_R[0] = diff_R[1];
		// $B8=:_$NJP:9CM(B($BL\I8CM(B - $B%;%s%5CM(B)$B$r<hF@(B($B%;%s%5$GGr$N3d9g$r<hF@(B)
		diff_R[1] = (TARGET - cnt[1])  / 2500;
		integral[1] += (diff_R[1] + diff_R[0]) / 2.0 * dt;
		derivation[1] = (diff_R[1] - diff_R[0]) / dt;

//		cout << "$B%+%&%s%H(B($BGr(B) : " << cnt[1] << endl;
		if(actuationMode == Link::JOINT_VELOCITY){
			// $B%"%/%A%e%(!<%7%g%s%b!<%I$,(Bvelocity$B$N>l9g(B
			// $B4X@aB.EY$N;XNaCM3JG<JQ?t(B
			double dq_target[2];

			// PID$B@)8f(B
			dq_target[0] = Kp * (vx - (va * d * diff_L[1])) + Ki * (integral[0] * va * d) + Kd * (derivation[0] * va * d);
			dq_target[1] = Kp * (vx + (va * d * diff_R[1])) + Ki * (integral[1] * va * d) + Kd * (derivation[1] * va * d);

//			cout << "$B:8(B: " << Kp * (vx - (va * d * diff_L[1])) << "\t" << Ki * (integral[0] * va * d) << "\t" << Kd * (derivation[0] * va * d) << endl;
//			cout << "$B1&(B: " << Kp * (vx + (va * d * diff_R[1])) << "\t" << Ki * (integral[1] * va * d) << "\t" << Kd * (derivation[1] * va * d) << endl;

			// $B:81&$N%[%$!<%k$K;XNaCM$rM?$($k(B
			wheels[0]->dq_target() = dq_target[0];
			wheels[1]->dq_target() = dq_target[1];
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
	}

	void onCameraStateChanged()
	{
		size_t length = 0;
		if(camera->sharedImage() != prevImage){
			// $B%+%a%i2hA|$,99?7$5$l$?$+3NG'(B
			const Image& image = camera->constImage();
			if(!image.empty()){
				// $B%+%a%i2hA|$,<hF@$G$-$?>l9g(B
				int width, height;
				// $B2hA|$N%5%$%:$r<hF@(B
				height = image.height();
				width = image.width();
				length = width * height * image.numComponents() * sizeof(unsigned char);
			}

			// $B2hA|$N(B1$B%T%/%;%k$4$H$N%G!<%?$r<hF@(B
			unsigned char* src = (unsigned char*)image.pixels();

			// $B%0%l!<!"Gr!"2+?'$N%+%&%s%HMQG[Ns$N=i4|2=(B
			cnt[0] = cnt[1] = cnt[2] = 0;
			// RGB$BCM3JG<G[Ns(B
			int rgb[3];

			// $B%G!<%??tJ,%k!<%W(B
			for(int i = 0; i < length / 3; ++i){
				// RGB$B$NCM$r3JG<(B
				rgb[0] = (int)src[i * 3];
				rgb[1] = (int)src[i * 3 + 1];
				rgb[2] = (int)src[i * 3 + 2];

				if((rgb[0] >= 100 && rgb[0] < 180)
						&& (rgb[1] >= 100 && rgb[1] < 180)
						&& (rgb[2] >= 100 && rgb[2] < 180)
						&& abs(rgb[0] - rgb[1]) <= 10
						&& abs(rgb[1] - rgb[2]) <= 10
						&& abs(rgb[2] - rgb[0]) <= 10){
					// $B%0%l!<$N8D?t$r%+%&%s%H(B
					cnt[0]++;
				}else if(rgb[0] >= 180 && rgb[1] >= 180 && rgb[2] >= 180){
					// $BGr$N8D?t$r%+%&%s%H(B
					cnt[1]++;
				}else if(rgb[0] >= 170 && rgb[1] >= 170 && rgb[2] <= 100){
					// $B2+?'$N8D?t$r%+%&%s%H(B
					cnt[2]++;
				}
			}
			// $BA02sCM$N99?7(B
			prevImage = camera->sharedImage();
		}
	}
};

CNOID_IMPLEMENT_SIMPLE_CONTROLLER_FACTORY(TurtleBot2TurnLineController)

