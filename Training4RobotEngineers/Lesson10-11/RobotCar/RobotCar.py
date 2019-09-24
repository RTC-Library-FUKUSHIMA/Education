#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file RobotCar.py
 @brief RobotCar Control
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import smbus  # PythonでI2Cを使用するために必要
import math   # piを計算するため

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
robotcar_spec = ["implementation_id", "RobotCar", 
		 "type_name",         "RobotCar", 
		 "description",       "RobotCar Control", 
		 "version",           "1.0.0", 
		 "vendor",            "FSK", 
		 "category",          "RobotCa", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class RobotCar
# @brief RobotCar Control
# 
# 
class RobotCar(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		VelValue_arg = [None] * ((len(RTC._d_TimedVelocity2D) - 4) / 2)
		self._d_VelValue = RTC.TimedVelocity2D(*VelValue_arg)
		"""
		"""
		self._VelIn = OpenRTM_aist.InPort("Vel", self._d_VelValue)



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
		self.addInPort("Vel",self._VelIn)
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports

		## gearbox
		self.radius = 0.0275  # タイヤの半径
		self.tread = 0.046    # タイヤ間の距離の半分
		self.rpm = 6500       # モータの回転数
		self.gear = 114.7     # ギア比
		self.Maxrpm=int(2*(self.rpm/self.gear))  # 3.0V時の回転数
		self.Minrpm=0*(self.rpm/self.gear)       # 0V時の回転数
		self.out_min = 1                         # 電圧設定最小値
		self.out_max = 38                        # 電圧設定最大値(3V)
		self.in_min = self.Minrpm                # 回転数最小値
		self.in_max = self.Maxrpm                # 回転数最大値
		self.right_sval=0
		self.left_sval =0
		## smbus
		self.bus = smbus.SMBus(1)        # I2Cバス番号
		self.SLAVE_ADDRESS_LEFT = 0x64   # 左モータのアドレス
		self.SLAVE_ADDRESS_RIGHT = 0x63  # 右モータのアドレス
		self.CONTROL = 0x00              # 命令レジスタのアドレス
		self.FORWARD = 0x01              # 正の回転
		self.BACK = 0x02                 # 負の回転
		self.STOP = 0x00                 # 停止
		self.TOWARD = 0x00               # モータの向き
		
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
		# タイヤ停止
		self.bus.write_i2c_block_data(self.SLAVE_ADDRESS_LEFT,self.CONTROL,[0x00])
		self.bus.write_i2c_block_data(self.SLAVE_ADDRESS_RIGHT,self.CONTROL,[0x00])
		
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

		if self._VelIn.isNew():
			# 値を読み込む
			readdata =self._VelIn.read()
			# 前回の値を保存
			old_left_sval=self.left_sval
			old_right_sval=self.right_sval

			# 左タイヤの計算 
			# 左モータの角速度
			omega_l=(readdata.data.vx - self.tread * readdata.data.va)/self.radius

			# モータの回転向き確認
			if omega_l > 0: self.TOWARD = self.FORWARD  # 角速度がプラスならモータの回転は正
			elif omega_l < 0:self.TOWARD=self.BACK      # 角速度がマイナスならモータの回転は負
			else :self.TOWARD=self.STOP                 # 角速度が0ならモータは停止
			omega_l=abs(omega_l)                        # 角速度がマイナスにならないようにする

			# 左モータの回転数
			leftrpm = omega_l*60/(2*math.pi)

			# 左モータの回転数から電圧への変換
			left_VSET  = (leftrpm - self.in_min) * (self.out_max-self.out_min) // (self.in_max-self.in_min) + self.out_min

			# 電圧にモータの回転向きを加える（ブリッジ制御を加える）
			self.left_sval = self.TOWARD |((int(left_VSET) + 5)<<2)

			# 値がおかしくないか確認
			if self.left_sval >= 1 and self.left_sval <= 255  and old_left_sval !=self.left_sval :
				self.bus.write_i2c_block_data(self.SLAVE_ADDRESS_LEFT,self.CONTROL,[self.left_sval])
			else :
				print "DCmotor1 value limite "+str(self.left_sval)
			
			# 右タイヤの計算 

			# 右モータの角速度
			omega_r=(readdata.data.vx + self.tread * readdata.data.va)/self.radius

			# モータの回転向き確認
			if omega_r > 0: self.TOWARD=self.FORWARD  # 角速度がプラスならモータの回転は正
			elif omega_r < 0:self.TOWARD=self.BACK    # 角速度がマイナスならモータの回転は負
			else :self.TOWARD=self.STOP               # 角速度が0ならモータは停止
			omega_r=abs(omega_r)                      # 角速度がマイナスにならないようにする

			# 右モータの回転数
			rightrpm = omega_r*60/(2*math.pi)

			# 右モータの回転数から電圧への変換
			right_VSET =  (rightrpm-self.in_min) * (self.out_max-self.out_min) // (self.in_max-self.in_min) + self.out_min

			# 電圧にモータの回転向きを加える（ブリッジ制御を加える）
			self.right_sval = self.TOWARD |((int(right_VSET) + 5)<<2)

			# 値がおかしくないか確認
			if self.right_sval >= 1 and self.right_sval <= 255 and old_right_sval !=self.right_sval :
				self.bus.write_i2c_block_data(self.SLAVE_ADDRESS_RIGHT,self.CONTROL,[self.right_sval])
			else :
				print "DCmotor2 value limite "+str(self.right_sval)
			
		return RTC.RTC_OK
		
	
		##
		#
		# The aborting action when main logic error occurred.
		# former rtc_aborting_entry()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onAborting(self, ec_id):
		
		return RTC.RTC_OK
	
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
	



def RobotCarInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=robotcar_spec)
    manager.registerFactory(profile,
                            RobotCar,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    RobotCarInit(manager)

    # Create a component
    comp = manager.createComponent("RobotCar")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

