#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file RobotCarControl.py
 @brief ロボットカー制御
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
robotcarcontrol_spec = ["implementation_id", "RobotCarControl", 
		 "type_name",         "RobotCarControl", 
		 "description",       "ロボットカー制御", 
		 "version",           "1.0.0", 
		 "vendor",            "FSK", 
		 "category",          "Controlle", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class RobotCarControl
# @brief ロボットカー制御
# 
# 
class RobotCarControl(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		#DistanceValue_arg = [None] * ((len(RTC._d_TimedULong) - 4) / 2)
		self._d_DistanceValue = RTC.TimedULong(RTC.Time(0,0),0)
		"""
		"""
		self._DistanceIn = OpenRTM_aist.InPort("Distance", self._d_DistanceValue)
		LEDValue_arg = [None] * ((len(RTC._d_TimedBoolean) - 4) / 2)
		self._d_LEDValue = RTC.TimedBoolean(RTC.Time(0,0),False)
		"""
		"""
		self._LEDOut = OpenRTM_aist.OutPort("LED", self._d_LEDValue)
		#VelValue_arg = [None] * ((len(RTC._d_TimedVelocity2D) - 4) / 2)
		self._d_VelValue = RTC.TimedVelocity2D(RTC.Time(0,0),RTC.Velocity2D(0.0,0.0,0.0))
		"""
		"""
		self._VelOut = OpenRTM_aist.OutPort("Vel", self._d_VelValue)


		


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
		self.addInPort("Distance",self._DistanceIn)
		
		# Set OutPort buffers
		self.addOutPort("LED",self._LEDOut)
		self.addOutPort("Vel",self._VelOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
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
		print "Active"
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
		print "Deactive"
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
		
		if self._DistanceIn.isNew():
			self._d_DistanceValue=self._DistanceIn.read()  # 距離の値を読み込む
			
			if self._d_DistanceValue.data < 10:  # 距離の値を規定値と比較
				# LEDの状態の値(True)を出力
				self._d_LEDValue.data=True
				self._LEDOut.write()
				# ロボットの旋回処理
				# 停止指定
				self._d_VelValue.data = RTC.Velocity2D(0.0, 0.0, 0.0)
				self._VelOut.write()
				# Sleep
				time.sleep(0.5);
				
				# 後退指定
				self._d_VelValue.data = RTC.Velocity2D(-0.2, 0.0, 0.0)
				self._VelOut.write()
				# Sleep
				time.sleep(1);
				
				# 右旋回指定
				self._d_VelValue.data = RTC.Velocity2D(0.0, 0.0, -5)
				self._VelOut.write()
				# Sleep
				time.sleep(1);
		
		# LEDの状態の値(False)を出力
		self._d_LEDValue.data=False
		self._LEDOut.write()
		
		# 前進指定
		self._d_VelValue.data = RTC.Velocity2D(0.2, 0.0, 0.0)
		self._VelOut.write()
		
		
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
	



def RobotCarControlInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=robotcarcontrol_spec)
    manager.registerFactory(profile,
                            RobotCarControl,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    RobotCarControlInit(manager)

    # Create a component
    comp = manager.createComponent("RobotCarControl")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

