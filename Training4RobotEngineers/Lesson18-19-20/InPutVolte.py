#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import rospy # pythonでROSのプログラムを記述
from robotcar_pkg.msg import Msg
import smbus  # I2Cを使用するためのモジュール
import time   # sleepを使用するためのモジュール


bus = smbus.SMBus(1)       # I2Cを使用するための宣言
SLAVE_ADDRESS_LEFT  = 0x63 # 左モータ用DRV8830のアドレス
SLAVE_ADDRESS_RIGHT = 0x64 # 右モータ用DRV8830のアドレス
CONTROL = 0x00             # 出力の設定
STOP = 0x00                # モータ停止の値

def callback(msg):
	# メッセージ通信から値を受け取る
    left_sval=msg.left_sval
    right_sval=msg.right_sval
    print left_sval
    print right_sval
    # 左モータ用DRV8830に前進の値を入力
    bus.write_i2c_block_data(SLAVE_ADDRESS_LEFT,CONTROL,[left_sval])
    # 右モータ用DRV8830に前進の値を入力
    bus.write_i2c_block_data(SLAVE_ADDRESS_RIGHT,CONTROL,[right_sval])

def InPut():

    # ノード名をInPutVolteで初期化
    rospy.init_node('InPutVolte', anonymous=True)
	# RobotCarというトピックからString型受け取り callback関数で処理
    rospy.Subscriber('RobotCar', Msg, callback)

    # ノードが止まるまで待機状態に移行する
    rospy.spin()
    # 左モータ用DRV8830に停止の値を入力
    bus.write_i2c_block_data(SLAVE_ADDRESS_LEFT,CONTROL,[STOP])
    # 右モータ用DRV8830に停止の値を入力
    bus.write_i2c_block_data(SLAVE_ADDRESS_RIGHT,CONTROL,[STOP])

if __name__ == '__main__':
    InPut()
