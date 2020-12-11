# Choreonoid講習会で使用するソース類のビルドまでの手順
## 1. ディレクトリ説明
|ディレクトリ名|説明|
|----|----|
|TurtleBot2|TurtleBot2モデルをシミュレータChoreonoidで操作するためのソース一式|
|TurtleBot2/controller|TurtleBot2モデルを操作するためのシンプルコントローラ|
|TurtleBot2/model|TurtleBot2と環境モデル|
|TurtleBot2/project|Choreonoidで読み込むことができるプロジェクトファイル|

## 2. ソースファイル説明
### 2.1. controllerディレクトリに格納されているファイル
|ファイル名|説明|
|----|----|
|TrafficLightController.cpp|ライントレースコースの信号機制御コントローラ|
|TurtleBot2AutoController.cpp|TurtleBot2モデルのライントレース制御コントローラ|
|TurtleBot2JoystickController.cpp|TurtleBot2モデルのDual Shock4操作用の制御コントローラ|
|TurtleBot2StopLineController.cpp|TurtleBot2モデルの白線で停止する用の制御コントローラ|
|TurtleBot2StraightController.cpp|TurtleBot2モデルの直進する用の制御コントローラ|
|TurtleBot2TurningController.cpp|TurtleBot2モデルの旋回する用の制御コントローラ|
|TurtleBot2TurnLineController.cpp|TurtleBot2モデルの白線の外周を走行する用の制御コントローラ|

### 2.2. modelディレクトリに格納されているファイル
|ファイル名|説明|
|----|----|
|AutoRaceCourse.body|Choreonoid用のライントレースコースモデル|
|HexagonsPlate.body|Choreonoid用のTurtleBot2のプレートモデル|
|HexagonsPlatePrimitives.yaml|Choreonoid用のTurtleBot2のプレートの干渉モデル|
|Kinect.body|Choreonoid用のKinectモデル|
|KinectPrimitives.yaml|Choreonoid用のKinectの干渉モデル|
|Kobuki.body|Choreonoid用のKobukiモデル|
|LineCourse.body|Choreonoid用の簡易コースモデル|
|TurtleBot2.body|Choreonoid用のTurtleBot2モデル|
|resource <sup>[[1]](#note1)</sup>|三次元CADデータ格納ディレクトリ|

<sup id="note1">[[1]](#note1)</sup> kobuki, sensors, stacksディレクトリ内のファイル、AutoRaceCourse.wrlファイルは以下のリポジトリのデータを修正し使用しています。<br>
* kobuki : [https://github.com/yujinrobot/kobuki.git](https://github.com/yujinrobot/kobuki.git)<br>
* sensors, stacks : [https://github.com/turtlebot/turtlebot.git](https://github.com/turtlebot/turtlebot.git)<br>
* AutoRaceCourse.wrl <sup>[[2]](#note2)</sup> : [https://github.com/ROBOTIS-GIT/autorace_track.git](https://github.com/ROBOTIS-GIT/autorace_track.git)

<sup id="note2">[[2]](#note2)</sup> AutoRaceCourse.wrl © ROBOTIS Co.,Ltd. [クリエイティブ・コモンズ・ライセンス（表示4.0 国際）](https://creativecommons.org/licenses/by/4.0/)<br>

### 2.3. projectディレクトリに格納されているファイル
|ファイル名|説明|
|----|----|
|TurtleBot2_Autorace.cnoid|TurtleBot2モデルがライントレースする用のプロジェクトファイル|
|TurtleBot2_StopLine.cnoid|TurtleBot2モデルが白線で停止する用のプロジェクトファイル|
|TurtleBot2_Straight.cnoid|TurtleBot2モデルが直進する用のプロジェクトファイル|
|TurtleBot2_Turning.cnoid|TurtleBot2モデルが旋回する用のプロジェクトファイル|
|TurtleBot2_TurnLine.cnoid|TurtleBot2モデルが外周を走行する用のプロジェクトファイル|
|TurtleBot2.cnoid|TurtleBot2モデルをDual Shock4で操作する用のプロジェクトファイル|

## 3. ビルド手順
1. Choreonoidをダウンロードします。ダウンロード手順は[Choreonoid公式サイトのソースコードからのビルドとインストール](https://choreonoid.org/ja/manuals/latest/install/build-ubuntu.html)を参照ください。<br>
2. ターミナルを起動し、以下のコマンドを実行します。ext以下にダウンロードすることでChoreonoidのビルド時に併せてビルドされます。<br>

【リポジトリのクローン方法】<br>
```bash
$ cd ~/choreonoid/ext/
$ git clone https://github.com/RTC-Library-FUKUSHIMA/Education.git
```

上記コマンドですと、リポジトリ全体をクローンするため、今回使用しないディレクトリも取得することになります。今回使用するディレクトリのみを取得したい方は、以下の手順を実行してください。<br><br>
【特定のディレクトリの取得方法】<br>
```bash
$ cd ~/choreonoid/ext/
$ mkdir Education
$ cd Education
$ git init
$ git config core.sparsecheckout true
$ git remote add origin https://github.com/RTC-Library-FUKUSHIMA/Education.git
$ echo ChoreonoidWorkshop > .git/info/sparse-checkout
$ git pull origin master
```

3. 以下のコマンドでCMakeLists.txtを生成し、ビルド対象"ChoreonoidWorkshop"ディレクトリがビルド対象に含まれるようにします。<br>
```bash
$ cd ~/choreonoid/ext/Education/ChoreonoidWorkshop/
$ ./createCMakeLists.sh
```

4. Choreonoidのビルドを行います。<br>
```bash
$ cd ~/choreonoid
$ mkdir build
$ mkdir program
$ cd build
$ cmake -DCMAKE_INSTALL_PREFIX=~/choreonoid/program ..
$ make -j4
$ sudo make install
```

## 4. Choreonoidによるプロジェクトファイル起動確認
プロジェクトの起動確認をします。以下のコマンドを実行し正常に表示されることを確認します。
```bash
$ cd ~/choreonoid/program
$ choreonoid share/choreonoid-1.8/TurtleBot2/project/TurtleBot2.cnoid
```

## 5. matplotlib-cppのインストール方法
```bash
$ cd /usr/local/include/
$ sudo git clone https://github.com/lava/matplotlib-cpp.git
$ sudo apt install -y python3-matplotlib python3-numpy python3.6-dev
```
