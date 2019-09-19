#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ConsoleConvert.py
 @brief ConsoleConvert component
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
consoleconvert_spec = ["implementation_id", "ConsoleConvert", 
		 "type_name",         "ConsoleConvert", 
		 "description",       "ConsoleConvert component", 
		 "version",           "1.0.0", 
		 "vendor",            "VenderName", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.Treadwidth", "0.046",
		 "conf.default.radius", "0.0275",

		 "conf.__widget__.Treadwidth", "text",
		 "conf.__widget__.radius", "text",

         "conf.__type__.Treadwidth", "float",
         "conf.__type__.radius", "float",

		 ""]
# </rtc-template>

##
# @class ConsoleConvert
# @brief ConsoleConvert component
# 
# 
class ConsoleConvert(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		InValue_arg = [None] * ((len(RTC._d_TimedVelocity2D) - 4) / 2)
		#self._d_InValue = RTC.TimedVelocity2D(*InValue_arg)
		self._d_InValue = RTC.TimedVelocity2D(RTC.Time(0,0),RTC.Velocity2D(0.0, 0.0, 0.0))
		"""
		"""
		self._InVelIn = OpenRTM_aist.InPort("InVel", self._d_InValue)
		OutValue_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		#self._d_OutValue = RTC.TimedFloatSeq(*OutValue_arg)
		self._d_OutValue = RTC.TimedFloatSeq(RTC.Time(0,0),[])
		"""
		"""
		self._OutAngularVelOut = OpenRTM_aist.OutPort("OutAngularVel", self._d_OutValue)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  width
		 - DefaultValue: 0.046
		"""
		self._width = [0.046]
		"""
		
		 - Name:  radius
		 - DefaultValue: 0.0275
		"""
		self._radius = [0.0275]
		
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
		self.bindParameter("Treadwidth", self._width, "0.046")
		self.bindParameter("radius", self._radius, "0.0275")
		
		# Set InPort buffers
		self.addInPort("InVel",self._InVelIn)
		
		# Set OutPort buffers
		self.addOutPort("OutAngularVel",self._OutAngularVelOut)
		
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
		print "onActivated"
		self._d_OutValue.data=[0.0,0.0]  #初期化
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
		print "onDeactivated"
		
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
		if self._InVelIn.isNew():  # 新しい値を受信しているか確認
			vel =self._InVelIn.read()  # 新しい値を読み込む
			# InPortからの値を使い各タイヤの角速度を計算
			Wl =  (vel.data.vx - vel.data.va * self._width[0] )/self._radius[0]
			Wr = (vel.data.vx + vel.data.va * self._width[0])/self._radius[0]
			print "Wl:" + str(Wl) + ",Wr:" + str(Wr)
			# タイヤの角速度をOutPortの変数に入力後出力
			self._d_OutValue.data[0]=Wl
			self._d_OutValue.data[1]=Wr
			self._OutAngularVelOut.write()
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
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
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
	



def ConsoleConvertInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=consoleconvert_spec)
    manager.registerFactory(profile,
                            ConsoleConvert,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ConsoleConvertInit(manager)

    # Create a component
    comp = manager.createComponent("ConsoleConvert")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

