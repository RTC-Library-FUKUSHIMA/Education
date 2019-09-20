# -*- coding: UTF-8 -*-
import smbus  # I2Cを使用するためのモジュール
import time   # sleepを使用するためのモジュール


bus = smbus.SMBus(1)       # I2Cを使用するための宣言
SLAVE_ADDRESS_LEFT  = 0x64 # 左モータ用DRV8830のアドレス
SLAVE_ADDRESS_RIGHT = 0x63 # 右モータ用DRV8830のアドレス
CONTROL = 0x00             # 出力の設定
STOP = 0x00                # モータ停止の値

# 前進
left_sval  = 93 # 左モータへの出力の値
right_sval = 93 # 右モータへの出力の値
# 左モータ用DRV8830に前進の値を入力
bus.write_i2c_block_data(SLAVE_ADDRESS_LEFT,CONTROL,[left_sval])
# 右モータ用DRV8830に前進の値を入力
bus.write_i2c_block_data(SLAVE_ADDRESS_RIGHT,CONTROL,[right_sval])
time.sleep(2.5)

# 後退
left_sval  = 94  # 左モータへの出力の値
right_sval = 94  # 右モータへの出力の値
# 左モータ用DRV8830に後退の値を入力
bus.write_i2c_block_data(SLAVE_ADDRESS_LEFT,CONTROL,[left_sval])
# 右モータ用DRV8830に後退の値を入力
bus.write_i2c_block_data(SLAVE_ADDRESS_RIGHT,CONTROL,[right_sval])
time.sleep(2.5)

# 停止
# 左モータ用DRV8830に停止の値を入力
bus.write_i2c_block_data(SLAVE_ADDRESS_LEFT,CONTROL,[STOP])
# 右モータ用DRV8830に停止の値を入力
bus.write_i2c_block_data(SLAVE_ADDRESS_RIGHT,CONTROL,[STOP])

