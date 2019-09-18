# coding: utf-8
import spidev  # spiを使用するためのモジュール
import time    # sleepを使用するためのモジュール
# 初期化
spi = spidev.SpiDev() # spiの初期宣言
spi.open(0, 0)        # spiのデバイスへの接続
DISTANCE_PIN = 0      # A0コネクタにDistanceを接続
SPI_SPEED = 1000000
spi.max_speed_hz =SPI_SPEED

try:
	while True:
		# 指定したチャンネルから値を受け取る
		adc = spi.xfer2([1, (8+DISTANCE_PIN)<<4, 0])
		# 受け取った値をアナログ値に変換
		data = ((adc[1]&3) << 8) + adc[2]
		# アナログ値を距離に変換
		if data<=17:
			data = 18
		distance=5461/(data-17) -2
		print("data : {:3},distance : {:3} ".format(data,distance))
		time.sleep(0.05)
except :
	spi.close()  # 終了処理
