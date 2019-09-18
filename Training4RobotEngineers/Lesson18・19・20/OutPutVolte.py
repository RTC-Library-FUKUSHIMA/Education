#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy  # pythonでROSのプログラムを記述
from robotcar_pkg.msg import Msg  # 作成したメッセージを使用する宣言
import sys  # 標準入力使用

def OutPut():
	# RobotCarというトピックへString型をバッファ10で送信
    pub = rospy.Publisher('RobotCar', Msg, queue_size=10)
	# ノード名をOutPutVolteで初期化
    rospy.init_node('OutPutVolte', anonymous=True)
    # メッセージ型追加
    msg = Msg()
	# 1秒間に10回Publisherが動作
    rate = rospy.Rate(10) # 10hz
    # ノードが落ちない限り無限ループ
    while not rospy.is_shutdown():
        print"volte left Value input"
	    # 標準入力でボルト数を入力
        left_value = raw_input()
        print"volte right Value input"
	    # 標準入力でボルト数を入力
        right_value = raw_input()
        msg.left_sval =int(left_value)
        msg.right_sval =int(right_value)
        # メッセージ通信で出力
        pub.publish(msg)
        print"volte Value send"
	    # プログラムをスリープさせる
        rate.sleep()

if __name__ == '__main__':
    try:
        OutPut()
    except rospy.ROSInterruptException:
        pass
