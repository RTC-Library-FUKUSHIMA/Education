# coding: utf-8
import RPi.GPIO as GPIO         # GPOIを使用するためのモジュール
import time                     # sleepを使用するためのモジュール
# Init
LEDPIN = 4                      # 使用するGPIOの数字（FaBo接続時の数字）
GPIO.setmode( GPIO.BCM )        # GPIOピンの設定の仕方 (GPIOの数字で指定)
GPIO.setup( LEDPIN, GPIO.OUT )  # GPIO4を出力として使用
# Program Start
GPIO.output( LEDPIN, True )     # LEDをONにする
time.sleep( 2.0 )               # 2秒間停止する
GPIO.output( LEDPIN, False )    # LEDをOFFにする
time.sleep( 2.0 )               # 2秒間停止する

GPIO.cleanup()                  # GPIOの使用を終了
