#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2015 chimera - observatory automation system
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

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

#initial variables setup - This setup is the original setup that was defined at the installation time.
#It is the same for both Commander SK drives.
# If you are planning to change these parameters, see Application Note CTAN#293

ip='127.0.0.1' #change to the corresponding ip number of your network installed commander SK
min_speed='' #Hz parm1
max_speed='' #Hz parm2
acc_rate='' #s/100Hz parm3
dec_rate='' #s/100 Hz parm4
motor_rated_speed=0 #rpm parm7 -attention: the ctsoft original parm is 1800 rpm
motor_rated_voltage=230 #V parm 8
motor_power_factor='' # parm 9 it can be changed for the motors's nameplate value if it is known
#Its is the motor cos() and 0.5<motor_power_factor<0.97.
ramp_mode=2#  parm 30 Standard Std (2) without dynamic braking resistor, If with this resistor, should set to 0 or
# Fast
dynamicVtoF='OFF'# parm 32 - It should not be used when the drive is being used as a soft start to full speed. keep off
voltage_mode_select=2 #parm 41  fixed boost mode(2)
low_freq_voltage_boost=1 #parm 42  0.5< low_freq_voltage_boost<1


__config__={'ip':'127.0.0.1', 'min_speed':0,'max_speed':600,'acc_rate':50,'dec_rate':100,'motor_rated_speed':1800,
          'motor_rated_voltage':230, 'motor_power_factor':85,'ramp_mode':1,'dynamicVtoF':1,'voltage_mode_select':2,
          'low_freq_voltage_boost':10}



def read_parm(parm):
    """
    gets a string in the format 'xx.xx' and converts it to an mapped
    commander sk address and returns its content
    """
    #print "reading parm:",parm
    parm_menu=parm.split('.')[0]
    parm_parm=parm.split('.')[1]
    address=int(parm_menu)*100+int(parm_parm)-1
    #print "mapped address equals:",address
    result = sk.read_holding_registers(address,1)
    #print "address:", address, "value:", result.registers[0]
    print "parameter ",parm,"=",result.registers[0]
    return result.registers[0]

def write_parm(parm, value):
    """
    gets a string in the format 'xx.xx' and converts it to an mapped
    commander sk address and writes the value to this address
    """
    print "parm:",parm
    parm_menu=parm.split('.')[0]
    parm_parm=parm.split('.')[1]
    address=int(parm_menu)*100+int(parm_parm)-1
    print "mapped address equals:",address
    rq = sk.write_register(address,value)
    conf=sk.read_holding_registers(address,1)[0]
    if conf==value:
        return True
    else:
        return False


def check_basic():


    error=[]


    #check parm1

    parm1 = read_parm('00.01')
    min_speed = __config__['min_speed']
    print "min_speed=", min_speed
    if parm1 == min_speed:
        print "parm1 ok"
    else:
        print "parm1 with error"
        error.append('parm1')
    print "*****************************"



    # check parm2

    parm2 = read_parm("00.02")
    max_speed = __config__['max_speed']
    print "max_speed=", max_speed
    if parm2 == max_speed:
        print "parm2 ok"
    else:
        print "parm2 with error"
        error.append('parm2')
    print "*****************************"


    #check parm3

    parm3 = read_parm("00.03")
    acc_rate = __config__['acc_rate']
    print "acc_rate=", acc_rate
    if parm3 == acc_rate:
        print "parm3 ok"
    else:
        print "parm3 with error"
        error.append('parm3')
    print "*****************************"


    #check parm4

    parm4 = read_parm("00.04")
    dec_rate = __config__['dec_rate']
    print "dec_rate=", dec_rate
    if parm4 == dec_rate:
        print "parm4 ok"
    else:
        print "parm4 with error"
        error.append('parm4')
    print "*****************************"

    #check parm7
    parm7 = read_parm("00.07")
    motor_rated_speed = __config__['motor_rated_speed']
    print "motor_rated_speed=", motor_rated_speed
    if parm7 == motor_rated_speed:
        print "parm7 ok"
    else:
        print "parm7 with error"
        error.append('parm7')
    print "*****************************"

    #check parm8
    parm8 = read_parm("00.08")
    motor_rated_voltage = __config__['motor_rated_voltage']
    print "motor_rated_voltage=", motor_rated_voltage
    if parm8 == motor_rated_voltage:
        print "parm8 ok"
    else:
        print "parm8 with error"
        error.append('parm8')
    print "*****************************"

    #check parm9
    parm9 = read_parm("00.09")
    motor_power_factor = __config__['motor_power_factor']
    print "motor_power_factor=", motor_power_factor
    if parm9 == motor_power_factor:
        print "parm9 ok"
    else:
        print "parm9 with error"
        error.append('parm9')
    print "*****************************"


    #check parm30
    parm30 = read_parm("00.30")
    ramp_mode = __config__['ramp_mode']
    print "ramp_mode=", ramp_mode
    if parm30 == ramp_mode:
        print "parm30 ok"
    else:
        print "parm30 with error"
        error.append('parm30')
    print "*****************************"

    #check parm32
    parm32 = read_parm("00.32")
    dynamicVtoF = __config__['dynamicVtoF']
    print "dynamicVtoF=", dynamicVtoF
    if parm32 == dynamicVtoF:
        print "parm32 ok"
    else:
        print "parm32 with error"
        error.append('parm32')
    print "*****************************"

    #check parm41
    parm41 = read_parm("00.41")
    voltage_mode_select = __config__['voltage_mode_select']
    print "voltage_mode_select=", voltage_mode_select
    if parm41 == voltage_mode_select:
        print "parm41 ok"
    else:
        print "parm41 with error"
        error.append('parm41')
    print "*****************************"

      #check parm42
    parm42 = read_parm("00.42")
    low_freq_voltage_boost = __config__['low_freq_voltage_boost']
    print "low_freq_voltage_boost=", low_freq_voltage_boost
    if parm42 == low_freq_voltage_boost:
        print "parm42 ok"
    else:
        print "parm42 with error"
        error.append('parm42')
    print "*****************************"

    return error

#***************** main *****************************

#open connection with sk commander
# default port: 502
# change the ip below to the commander ip of your network
#starting connection
ip='192.168.30.104'
sk=ModbusTcpClient(ip)
if sk.connect():
    print"...connection ok..."
else:
    print "...can't connect to sk..."
    exit()

print "*****************************"

#starts checking to see if the basic parameters are correctly set up
error=check_basic()
if len(error)>0:
    print"errors found:",error
else:
    print"driver basic set up ok"

sk.close()
exit()


