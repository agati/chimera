#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

# chimera - observatory automation system
# Copyright (C) 2006-2007  P. Henrique Silva <henrique@astro.ufsc.br>

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


from chimera.core.interface import Interface
from pymodbus.client.sync import ModbusTcpClient

# this interface configures a TCP/IP ModeBus controller address and defines basic read/write functions


class ModBusCtl(Interface):
    def setup_client(ip):
        """

        :param example ip: 192.168.10.100
        :return:True
        """

        return True


    def readRegister(start_address, size):
        """
        reads 16bit-controller neighbour registers
        :param start_address: first 16bit-register address
        :param size: number of registers to be read
        :return:a dictionary/list of multiples 16-bit registers
        in the format {register1:value1, register2:value2,...}
        """
        return


    def writeRegister(start_address, size):
        """

        :param start_address: first 16bit-register address
        :param size: number of registers to be written
        :return:True
        """
        return











