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

	// ファイル名
	string fileName = "plot.tsv";
	// 配列の定義(t: time, x: x axis, y: y axis)
	vector<double> t, x, y;
//	vector<double> x_itrv, y_itrv;
	// タブ区切りのデータ格納変数
	string tmp;
	// ファイル入出力の宣言
	FILE* fp;
	// バッファサイズ
	static const int BUF_SIZE = 100;
	char str[BUF_SIZE];
	// カレントディレクトリ取得コマンド
#ifdef _WIN32
	string cmd = "echo %CD%\\";
#else
	string cmd = "pwd | tr '\n' '/'";
#endif // !_WIN32
	int cnt = 0;
	// ファイルパス
	string filePath = "";
	
#ifdef _WIN32
	if((fp = _popen(cmd.c_str(), "r")) != NULL){
		// プロセスをオープンしコマンドを実行
		while(fgets(str, sizeof(str), fp) != NULL){
			// コマンド結果を1行ずつ読み込む
			str[strlen(str) - 1] = '\0';
			// カレントディレクトリの取得
			filePath += str;
		}
		// プロセスをクローズ
		_pclose(fp);
	}
	filePath += "..\\..\\";
#else
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
#endif // !_WIN32

	// ディレクトリ名とファイル名を連結
	filePath = filePath + fileName;
	// ファイルを読み込む
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
