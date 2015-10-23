#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
# chimera - observatory automation system
# Copyright (C) 2006-2015  P. Henrique Silva <henrique@astro.ufsc.br>
# Copyright (C) 2015  Salvador Sergi Agati <salvadoragati@gmail.com>
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
# ****************************************************************
# Copyright (C) 2015 Salvador S. Agati <salvadoragati@gmail.com> *
# #grant #2015/06983-1, São Paulo Research Foundation (FAPESP).  *
# Opinions, assumptions and conclusions or recommendations       *
# expressed in this material by Salvador Sergi Agati are his     *
# responsibility and do not necessarily reflect the              *
# views of FAPESP.                                               *
# *****************************************************************
# *******************************************************************
# This driver is intended to be used with the Emerson Commander SK  *
# order number SKBD200110 -  salvadoragati@gmail.com                *
# start:15/06/2015 - last update: 07/10/2015                        *
# ********************************************************************


import time

from pymodbus.client.sync import ModbusTcpClient


class SKDrv(ModbusTcpClient):
    #initial variables setup - This setup is the original setup that was defined at the installation time.
    #It is the same for both Commander SK drives.
    # If you are planning to change these parameters, see Application Note CTAN#293
    #At the moment, no chimera object added to this class. It must be checked if as a driver, it is needed.
    # You have to have Pymodbus module previously installed to this driver work properly.

    ip = ''  #change to the corresponding ip number of your network installed commander SK
    min_speed = ''  #Hz parm1
    max_speed = ''  #Hz parm2
    acc_rate = ''  #s/100Hz parm3
    dec_rate = ''  #s/100 Hz parm4
    motor_rated_speed = 0  #rpm parm7 -attention: the ctsoft original parm is 1800 rpm
    motor_rated_voltage = 230  #V parm 8
    motor_power_factor = ''  # parm 9 it can be changed for the motor's nameplate value if it is known
    #It is the motor cos() and 0.5<motor_power_factor<0.97.
    ramp_mode = 2  #  parm 30 Standard Std (2) without dynamic braking resistor, If with this resistor, should set to 0 or
    # Fast
    dynamicVtoF = 'OFF'  # parm 32 - It should not be used when the drive is being used as a soft start to full speed. keep off
    voltage_mode_select = 2  #parm 41  fixed boost mode(2)
    low_freq_voltage_boost = 1  #parm 42  0.5< low_freq_voltage_boost<1

    order_number = 'SKBD200110'

    __config__ = {'ip': '127.0.0.1', 'min_speed': 0, 'max_speed': 600, 'acc_rate': 50, 'dec_rate': 100,
                  'motor_rated_speed': 1800,
                  'motor_rated_voltage': 230, 'motor_power_factor': 85, 'ramp_mode': 1, 'dynamicVtoF': 1,
                  'voltage_mode_select': 2,
                  'low_freq_voltage_boost': 10}

    def get_order_number(self):
        return self.order_number


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

    def get_ip(self):
        ip = str(self.read_parm('15.10')) + '.' + str(self.read_parm('15.11')) + '.' + str(
            self.read_parm('15.12')) + '.' + str(
            self.read_parm('15.13'))
        return ip


    def check_basic(self):

        parm_change = []

        #check parm1
        parm1 = self.read_parm('00.01')
        min_speed = self.__config__['min_speed']
        if parm1 != min_speed:
            parm_change.append('00.01:min_speed')

        # check parm2
        parm2 = self.read_parm("00.02")
        max_speed = self.__config__['max_speed']
        if parm2 != max_speed:
            parm_change.append('00.02:max_speed')

        #check parm3
        parm3 = self.read_parm("00.03")
        acc_rate = self.__config__['acc_rate']
        if parm3 != acc_rate:
            parm_change.append('00.03:acc_rate')

        #check parm4
        parm4 = self.read_parm("00.04")
        dec_rate = self.__config__['dec_rate']
        if parm4 != dec_rate:
            parm_change.append('00.04:dec_rate')

        #check parm7
        parm7 = self.read_parm("00.07")
        motor_rated_speed = self.__config__['motor_rated_speed']
        if parm7 != motor_rated_speed:
            parm_change.append('00.07:motor_rated_speed')

        #check parm8
        parm8 = self.read_parm("00.08")
        motor_rated_voltage = self.__config__['motor_rated_voltage']
        if parm8 != motor_rated_voltage:
            parm_change.append('00.08:motor_rated_voltage')

        #check parm9
        parm9 = self.read_parm("00.09")
        motor_power_factor = self.__config__['motor_power_factor']
        if parm9 != motor_power_factor:
            parm_change.append('00.09:motor_power_factor')

        #check parm30
        parm30 = self.read_parm("00.30")
        ramp_mode = self.__config__['ramp_mode']
        if parm30 != ramp_mode:
            parm_change.append('00.30:ramp_mode')

        #check parm32
        parm32 = self.read_parm("00.32")
        dynamicVtoF = self.__config__['dynamicVtoF']
        if parm32 != dynamicVtoF:
            parm_change.append('00.32:dynamicVtoF')

        #check parm41
        parm41 = self.read_parm("00.41")
        voltage_mode_select = self.__config__['voltage_mode_select']
        if parm41 != voltage_mode_select:
            parm_change.append('00.41:voltage_mode_select')

        #check parm42
        parm42 = self.read_parm("00.42")
        low_freq_voltage_boost = self.__config__['low_freq_voltage_boost']
        if parm42 != low_freq_voltage_boost:
            parm_change.append('00.42:low_freq_voltage_boost')

        return parm_change


    def setup(self):
        """
        Defines some controller's presets and assures that the minimal remote control parameters are defined.

        self.write_parm('01.21',10)#preset1= 10 Hz - adjust this to the desired nominal working speed
        self.write_parm('01.15',1)#presets speed selector to 1
        self.write_parm('01.14',3)#changes reference selector to preset
        self.write_parm('06.40',0)#enables sequence latcher=off
        self.write_parm('06.43',1)#enables control word

        """

        if self.write_parm('01.21', 10) and self.write_parm('01.15', 1) and self.write_parm('01.14',
                                                                                            3) and self.write_parm(
                '06.40', 0) and self.write_parm('06.43', 1):
            return True

        return False


    def check_rotation(self):

        """
        reads the motor rotation in rpm
        """

        rotation = self.read_parm('05.04')  # motor speed in rpm
        return rotation



    def forward(self):
        """
        runs the motor fan forward
        """

        if self.write_parm('06.42', 131):  # run forward
            return True

        return False


    def stop(self):
        """
        stops de motor fan
        """
        if self.write_parm('06.42', 129):  # stop
            return True

        return False

    def reverse(self):
        """
        runs reverse the motor fan

        """
        if self.write_parm('06.42', 137):  # run reverse
            return True

        return False


    def reset(self):
        """
        remotely resets the controller
        """
        if self.write_parm('10.33', 1):  # drive reset
            time.sleep(1)  # necessary delay to force logical reset level high during 1 second
            if self.write_parm('10.33', 0):
                return True
            else:
                return False

        return False

    def enableCW(self):
        """
        enables Control Word usage
        """
        if not self.write_parm('06.43', 1):  # enables CW
            return False
        if not self.write_parm('06.42', 128):  # mantains it in auto mode
            return False

        return True


    def disableCW(self):
        """
        disables Control Word usage
        """
        if not self.write_parm('06.42', 129):  # stops the motor fan
            return False
        if not self.write_parm('06.42', 128):  # mantain its in auto
            return False
        if not self.write_parm('06.43', 0):  # disables CW
            return False

        return True


    def save(self):
        """
        saves the data and resets the controller
        :return:
        """
        if self.write_parm('11.00', 1000):  # saves the data
            if self.reset():  # resets the drive
                return True
            else:
                return False

        return False


