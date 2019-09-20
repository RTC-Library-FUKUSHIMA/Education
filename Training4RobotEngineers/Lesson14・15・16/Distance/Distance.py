#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Distance.py
 @brief 距離センサー用コンポーネント
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import spidev #spiを使用するためのモジュール

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
distance_spec = ["implementation_id", "Distance", 
		 "type_name",         "Distance", 
		 "description",       "距離センサー用コンポーネント", 
		 "version",           "1.0.0", 
		 "vendor",            "FSK", 
		 "category",          "Sencer", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class Distance
# @brief 距離センサー用コンポーネント
# 
# 
class Distance(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		DistanceValue_arg = [None] * ((len(RTC._d_TimedULong) - 4) / 2)
		#self._d_DistanceValue = RTC.TimedULong(*DistanceValue_arg)
		self._d_DistanceValue = RTC.TimedULong(RTC.Time(0,0),0)
		"""
		"""
		self._DistanceOut = OpenRTM_aist.OutPort("Distance", self._d_DistanceValue)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		
		# Set OutPort buffers
		self.addOutPort("Distance",self._DistanceOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		self.DISTANCE_PIN = 0  # A0コネクタにDistanceを接続
		self.spi = spidev.SpiDev()  # spiの初期宣言
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
		SPI_SPEED = 1000000
		self.spi.open(0, 0)  # デバイスを接続
		self.spi.max_speed_hz =SPI_SPEED
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
		self.spi.close()  # デバイスを切断
		return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
		# 指定したチャンネルから値を受け取る
		adc = self.spi.xfer2([1, (8+self.DISTANCE_PIN)<<4, 0])
		# 受け取った値をアナログ値に変換
		data = data = ((adc[1]&3) << 8) + adc[2]
		if data<=17:  # 値が17だと値がおかしくなるので18に変更
			data = 18
		distance=5461/(data-17) -2  # 距離に変換の式
		print("data : {:3},distance : {:3}".format(data,distance))
		if distance < 0 :  # 距離が0以下の場合は0にする。
			distance=0
		self._d_DistanceValue.data =int(distance)
		# 値を出力
		self._DistanceOut.write()

		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The error action in ERROR state
		# former rtc_error_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onError(self, ec_id):
	
		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def DistanceInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=distance_spec)
    manager.registerFactory(profile,
                            Distance,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    DistanceInit(manager)

    # Create a component
    comp = manager.createComponent("Distance")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

