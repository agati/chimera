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

def write_parm(parm, value):
        """
        gets a string in the format 'xx.xx' and converts it to an mapped
        commander sk address and writes the value to it
        """
        print "write parameter:", parm,"=",value
        parm_menu = parm.split('.')[0]
        parm_parm = parm.split('.')[1]
        address = int(parm_menu) * 100 + int(parm_parm) - 1
        #print "mapped address equals:", address
        rq = sk.write_register(address, value)
        result = sk.read_holding_registers(address, 1)
        print "check:",result.registers[0]
        if result.registers[0] == value:
            return True
        else:
            return False



ip='192.168.30.105'
sk=ModbusTcpClient(ip)
if sk.connect():
    print"...connection ok..."
else:
    print "...can't connect to sk..."
    exit()

print "*****************************"

#teste de stop
teste=write_parm('06.34',1)

#teste de run
sk.close()

exit()

#teste de run