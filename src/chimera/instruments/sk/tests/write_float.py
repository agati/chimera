#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2015 chimera - observatory automation system
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#*******************************************************************
#This driver is intended to be used with the Emerson Commander SK
#order number SKBD200110 - 15/06/2015 - salvadoragati@gmail.com


from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder



#initial setup variables - If you are planning to change these parameters, see Application Note CTAN#293

ip='127.0.0.1' #change to the corresponding ip number of your network installed commander SK
min_speed=0.1 #Hz parm1
max_speed=60.0 #Hz parm2
acc_rate=33.0 #s/100Hz parm3
dec_rate=33.0 #s/100 Hz parm4
motor_rated_speed=0 #rpm parm7 -attention: the ctsoft original parm is 1800 rpm
motor_rated_voltage=230 #V parm 8
motor_power_factor=0.85 # parm 9 it can be changed for the motors's nameplate value if it is known
#Its is the motor cos? and 0.5<motor_power_factor<0.97.
ramp_mode=2#  parm 30 Standard Std (2) without dynamic braking resistor, If with this resistor, should set to 0 or
# Fast
dynamicVtoF='OFF'# parm 32 - It should not be used when the drive is being used as a soft start to full speed. keep off
voltage_mode_select=2 #parm 41  fixed boost mode(2)
low_freq_voltage_boost=1 #%   0.5< low_freq_voltage_boost<1

__config__={ip:'127.0.0.1',min_speed:0.1,max_speed:60.0,acc_rate:33.0,dec_rate:33.0,motor_rated_speed:0,
          motor_rated_voltage:230,motor_power_factor:0.85,ramp_mode:2,dynamicVtoF:'OFF', voltage_mode_select:2,
          low_freq_voltage_boost:1}


#open connection with sk commander
# default port: 502
# change the ip below to the commander ip of your network
#starting connection

sk=ModbusTcpClient(ip)
if sk.connect():
    builder = BinaryPayloadBuilder(endian=Endian.Little)
    builder.add_32bit_float(321.57)
    payload = builder.build()
    result  = sk.write_registers(4005, payload, skip_encode=True)



    sk.close()

exit()

