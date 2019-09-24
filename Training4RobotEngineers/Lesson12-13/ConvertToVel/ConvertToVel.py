#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ConvertToVel.py
 @brief ConvertValue component
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
converttovel_spec = ["implementation_id", "ConvertToVel", 
		 "type_name",         "ConvertToVel", 
		 "description",       "ConvertValue component", 
		 "version",           "1.0.0", 
		 "vendor",            "fsk", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class ConvertToVel
# @brief ConvertValue component
# 
# 
class ConvertToVel(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		inValue_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		#self._d_inValue = RTC.TimedFloatSeq(*inValue_arg)
		self._d_inValue = RTC.TimedFloatSeq(RTC.Time(0,0),[])
		"""
		"""
		self._VelInIn = OpenRTM_aist.InPort("VelIn", self._d_inValue)
		outValue_arg = [None] * ((len(RTC._d_TimedVelocity2D) - 4) / 2)
		#self._d_outValue = RTC.TimedVelocity2D(*outValue_arg)
		self._d_outValue = RTC.TimedVelocity2D(RTC.Time(0,0),RTC.Velocity2D(0.0, 0.0, 0.0))

		"""
		"""
		self._VelOutOut = OpenRTM_aist.OutPort("VelOut", self._d_outValue)


		


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
		self.addInPort("VelIn",self._VelInIn)
		
		# Set OutPort buffers
		self.addOutPort("VelOut",self._VelOutOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		self.tread = 0.046
		
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
		print"Activated"
	
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
		print"Deactivated"
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

		if self._VelInIn.isNew():
			# 値を読み込む
			data = self._VelInIn.read()
			print data.data
			# 左車輪と右車輪の値から速度と角速度を求める
			# 中央の速度を求める
			Vx=(data.data[1]+data.data[0])/2
			# 角速度を求める
			omega=(data.data[1]-data.data[0])/(2*self.tread)
			# 値が大きすぎるので1000分の1します。
			self._d_outValue.data.vx =Vx/1000
			self._d_outValue.data.vy =0.0
			self._d_outValue.data.va =omega/1000
			print"Vx*:"+str(Vx)
			print"Va*:"+str(omega)
			#  出力する。
			self._VelOutOut.write()
	
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
	



def ConvertToVelInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=converttovel_spec)
    manager.registerFactory(profile,
                            ConvertToVel,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ConvertToVelInit(manager)

    # Create a component
    comp = manager.createComponent("ConvertToVel")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

