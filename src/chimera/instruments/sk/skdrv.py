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
# *******************************************************************
# This driver is intended to be used with the Emerson Commander SK
# order number SKBD200110 - 15/06/2015 - salvadoragati@gmail.com


from pymodbus.client.sync import ModbusTcpClient


class SKDrv(ModbusTcpClient):
    #initial variables setup - This setup is the original setup that was defined at the installation time.
    #It is the same for both Commander SK drives.
    # If you are planning to change these parameters, see Application Note CTAN#293

    ip = ''  #change to the corresponding ip number of your network installed commander SK
    min_speed = ''  #Hz parm1
    max_speed = ''  #Hz parm2
    acc_rate = ''  #s/100Hz parm3
    dec_rate = ''  #s/100 Hz parm4
    motor_rated_speed = 0  #rpm parm7 -attention: the ctsoft original parm is 1800 rpm
    motor_rated_voltage = 230  #V parm 8
    motor_power_factor = ''  # parm 9 it can be changed for the motors's nameplate value if it is known
    #Its is the motor cos() and 0.5<motor_power_factor<0.97.
    ramp_mode = 2  #  parm 30 Standard Std (2) without dynamic braking resistor, If with this resistor, should set to 0 or
    # Fast
    dynamicVtoF = 'OFF'  # parm 32 - It should not be used when the drive is being used as a soft start to full speed. keep off
    voltage_mode_select = 2  #parm 41  fixed boost mode(2)
    low_freq_voltage_boost = 1  #parm 42  0.5< low_freq_voltage_boost<1

    __config__ = {'ip': '127.0.0.1', 'min_speed': 0, 'max_speed': 600, 'acc_rate': 50, 'dec_rate': 100,
                  'motor_rated_speed': 1800,
                  'motor_rated_voltage': 230, 'motor_power_factor': 85, 'ramp_mode': 1, 'dynamicVtoF': 1,
                  'voltage_mode_select': 2,
                  'low_freq_voltage_boost': 10}


    def read_parm(self, parm):
        """
        gets a string in the format 'xx.xx' and converts it to an mapped
        commander sk address and returns its contents
        """

        parm_menu = parm.split('.')[0]
        parm_parm = parm.split('.')[1]
        address = int(parm_menu) * 100 + int(parm_parm) - 1
        result = self.read_holding_registers(address, 1)
        return result.registers[0]

    def write_parm(self, parm, value):
        """
        gets a string in the format 'xx.xx' and converts it to an mapped
        commander sk address and writes the value to it
        """
        parm_menu = parm.split('.')[0]
        parm_parm = parm.split('.')[1]
        address = int(parm_menu) * 100 + int(parm_parm) - 1
        rq = self.write_register(address, value)
        result = self.read_holding_registers(address, 1)
        if result.registers[0] == value:
            return True
        else:
            return False


    def check_basic(self):

        parm_change = []


        #check parm1

        parm1 = self.read_parm('00.01')
        print "parm1=", parm1
        min_speed = self.__config__['min_speed']
        print "min_speed=", min_speed
        if parm1 == min_speed:
            print "parm1 ok"
        else:
            print "parm1 changed"
            parm_change.append('parm1')
        print "*****************************"

        # check parm2

        parm2 = self.read_parm("00.02")
        print "parm2=", parm2
        max_speed = self.__config__['max_speed']
        print "max_speed=", max_speed
        if parm2 == max_speed:
            print "parm2 ok"
        else:
            print "parm2 changed"
            parm_change.append('parm2')
        print "*****************************"


        #check parm3

        parm3 = self.read_parm("00.03")
        print "parm3=", parm3
        acc_rate = self.__config__['acc_rate']
        print "acc_rate=", acc_rate
        if parm3 == acc_rate:
            print "parm3 ok"
        else:
            print "parm3 changed"
            parm_change.append('parm3')
        print "*****************************"


        #check parm4

        parm4 = self.read_parm("00.04")
        print "parm4=", parm4
        dec_rate = self.__config__['dec_rate']
        print "dec_rate=", dec_rate
        if parm4 == dec_rate:
            print "parm4 ok"
        else:
            print "parm4 changed"
            parm_change.append('parm4')
        print "*****************************"

        #check parm7
        parm7 = self.read_parm("00.07")
        print "parm7=", parm7
        motor_rated_speed = self.__config__['motor_rated_speed']
        print "motor_rated_speed=", motor_rated_speed
        if parm7 == motor_rated_speed:
            print "parm7 ok"
        else:
            print "parm7 changed"
            parm_change.append('parm7')
        print "*****************************"

        #check parm8
        parm8 = self.read_parm("00.08")
        print "parm8=", parm8
        motor_rated_voltage = self.__config__['motor_rated_voltage']
        print "motor_rated_voltage=", motor_rated_voltage
        if parm8 == motor_rated_voltage:
            print "parm8 ok"
        else:
            print "parm8 changed"
            parm_change.append('parm8')
        print "*****************************"

        #check parm9
        parm9 = self.read_parm("00.09")
        print "parm9=", parm9
        motor_power_factor = self.__config__['motor_power_factor']
        print "motor_power_factor=", motor_power_factor
        if parm9 == motor_power_factor:
            print "parm9 ok"
        else:
            print "parm9 changed"
            parm_change.append('parm9')
        print "*****************************"


        #check parm30
        parm30 = self.read_parm("00.30")
        print "parm30=", parm30
        ramp_mode = self.__config__['ramp_mode']
        print "ramp_mode=", ramp_mode
        if parm30 == ramp_mode:
            print "parm30 ok"
        else:
            print "parm30 changed"
            parm_change.append('parm30')
        print "*****************************"

        #check parm32
        parm32 = self.read_parm("00.32")
        print "parm32=", parm32
        dynamicVtoF = self.__config__['dynamicVtoF']
        print "dynamicVtoF=", dynamicVtoF
        if parm32 == dynamicVtoF:
            print "parm32 ok"
        else:
            print "parm32 changed"
            parm_change.append('parm32')
        print "*****************************"

        #check parm41
        parm41 = self.read_parm("00.41")
        print "parm41=", parm41
        voltage_mode_select = self.__config__['voltage_mode_select']
        print "voltage_mode_select=", voltage_mode_select
        if parm41 == voltage_mode_select:
            print "parm41 ok"
        else:
            print "parm41 changed"
            parm_change.append('parm41')
        print "*****************************"

        #check parm42
        parm42 = self.read_parm("00.42")
        print "parm42=", parm42
        low_freq_voltage_boost = self.__config__['low_freq_voltage_boost']
        print "low_freq_voltage_boost=", low_freq_voltage_boost
        if parm42 == low_freq_voltage_boost:
            print "parm42 ok"
        else:
            print "parm42 changed"
            parm_change.append('parm42')
        print "*****************************"
        any_key = raw_input("Press [ENTER] to continue...")

        return parm_change

    def check_rotation(self):

        """
        read the motor rotation in rpm
        """
        print"checking rotation..."
        rotation = self.read_parm('05.04')  # motor speed in rpm
        print "rotation is:", rotation
        if rotation > 0:
            print"The motor fan is on , running at", rotation, "rpm"
        else:
            print"The motor fan is off"
            any_key = raw_input("Press [ENTER] to continue...")

        return


    def start(ip):
        """
        choose a direction and starts the motor fan indicated by its IP
        :return:
        """

    def stop(ip):
        """
        stops de motor fan indicated by its IP
        :param ip:
        TODO
        :return:
        """

    def set_timer(self):
        """
        defines an interval of time to mantain the motor running
        TODO
        :return:
        """

    def check_timer(self):
        """
        check the timer values
        TODO
        :return:
        """
