#include <fstream>
#include <matplotlib-cpp/matplotlibcpp.h>
#include <cmath>
#ifndef _WIN32
#include <stdio.h>
#endif // !_WIN32

using namespace std;
namespace plt = matplotlibcpp;

int main(){
	cout << "matplot start" << endl;

	// $B%U%!%$%kL>(B
	string fileName = "plot.tsv";
	// $BG[Ns$NDj5A(B(t: time, x: x axis, y: y axis)
	vector<double> t, x, y;
//	vector<double> x_itrv, y_itrv;
	// $B%?%V6h@Z$j$N%G!<%?3JG<JQ?t(B
	string tmp;
	// $B%U%!%$%kF~=PNO$N@k8@(B
	FILE* fp;
	// $B%P%C%U%!%5%$%:(B
	static const int BUF_SIZE = 100;
	char str[BUF_SIZE];
	// $B%+%l%s%H%G%#%l%/%H%j<hF@%3%^%s%I(B
#ifdef _WIN32
	string cmd = "echo %CD%\\";
#else
	string cmd = "pwd | tr '\n' '/'";
#endif // !_WIN32
	int cnt = 0;
	// $B%U%!%$%k%Q%9(B
	string filePath = "";
	
#ifdef _WIN32
	if((fp = _popen(cmd.c_str(), "r")) != NULL){
		// $B%W%m%;%9$r%*!<%W%s$7%3%^%s%I$r<B9T(B
		while(fgets(str, sizeof(str), fp) != NULL){
			// $B%3%^%s%I7k2L$r(B1$B9T$:$DFI$_9~$`(B
			str[strlen(str) - 1] = '\0';
			// $B%+%l%s%H%G%#%l%/%H%j$N<hF@(B
			filePath += str;
		}
		// $B%W%m%;%9$r%/%m!<%:(B
		_pclose(fp);
	}
	filePath += "..\\..\\";
#else
	if((fp = popen(cmd.c_str(), "r")) != NULL){
		// $B%W%m%;%9$r%*!<%W%s$7%3%^%s%I$r<B9T(B
		while(fgets(str, sizeof(str), fp) != NULL){
			// $B%3%^%s%I7k2L$r(B1$B9T$:$DFI$_9~$`(B
			// $B%+%l%s%H%G%#%l%/%H%j$N<hF@(B
			filePath += str;
		}
		// $B%W%m%;%9$r%/%m!<%:(B
		pclose(fp);
	}
#endif // !_WIN32

	// $B%G%#%l%/%H%jL>$H%U%!%$%kL>$rO"7k(B
	filePath = filePath + fileName;
	// $B%U%!%$%k$rFI$_9~$`(B
	ifstream ifs(filePath);
	if(ifs.fail()){
		cerr << "Failed to open file." << endl;
		return false;
	} else {
		while(getline(ifs, tmp, '\t')){
			if(ifs.eof()){
				ifs.close();
				break;
			} else {
				if(cnt == 0){
					t.push_back(stod(tmp));
					cnt++;
				} else if(cnt == 1){
					x.push_back(stod(tmp));
					cnt++;
				} else if(cnt == 2){
					y.push_back(stod(tmp));
					cnt = 0;
				}
			}	
		}
	}
	
	plt::xlabel("T");
	plt::ylabel("X, Y");
//	plt::xlabel("X");
//	plt::ylabel("Y");
	
	plt::plot(t, x, "b");
	plt::plot(t, y, "r");
//	plt::plot(x, y, "r");

//	int sec = 0;
//	for(int i = 0; i < x.size(); ++i){
//		int val = t[i] - (t[i] - (int)t[i]);
//		if(val == sec){
//			if(val % 5 == 0){
//				x_itrv.push_back(x[i]);
//				y_itrv.push_back(y[i]);
//				plt::text(x[i], y[i], std::to_string((int)t[i]));
//			}
//			sec++;
//		}
//	}
//	plt::scatter(x_itrv, y_itrv, 100.0, { { "c", "pink" }, { "marker", "o" },
//			{ "alpha", "0.5" }, { "linewidths", "2" }, { "edgecolors", "red" } });
	plt::show();
	cout << "matplot end" << endl;

	return 0;
}
