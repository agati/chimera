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
# This script is intended to be used with the Emerson Commander SK
# order number SKBD200110 - 23/06/2015 - salvadoragati@gmail.com

# from chimera.src.chimera.instruments.sk.skdrv import SKDrv
import os

from skdrv import SKDrv


def controller_menu():
    # -choose controller (ip)
    os.system('cls' if os.name == 'nt' else 'clear')

    print "***************************************"
    print "*** Commander SK Control Manager ******"
    print "***************************************"

    print"Choose the controller number :"
    print""
    print "1-IP:192.168.30.104 - Eastern"
    print "2-IP:192.168.30.105 - Western"
    print "3-Exit"
    key = raw_input("Choice:(1/2/3)")
    if key == '1':
        ip = '192.168.30.104'
        return ip
    if key == '2':
        ip = '192.168.30.105'
        return ip
    if key == '3':
        ip = ''

        return ip


def main_menu(ip):
    os.system('cls' if os.name == 'nt' else 'clear')
    print "***************************************"
    print "*** Commander SK Control Manager ******"
    print "***************************************"
    print " ip: ", ip
    print"Choose command:"
    print""
    print "1-Check rotation"
    print "2-Start"
    print "3-Stop"
    print "4-Timer"
    print "5-Automatic Start by Temperature Treshold"
    print "6-Restart"
    action = raw_input("(1/2/3/4/5/6)")
    return action


# main menu
while 1:
    data = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    ip = controller_menu()
    if ip == '': exit()



    #ip='192.168.30.104'
    #ip='192.168.30.105'
    #ip='127.0.0.1'
    sk = SKDrv()
    sk.host = ip

    try:
        sk.connect()

        #check the basic parameters
        changes = sk.check_basic()
        if len(changes) > 0:
            print "Changes on basic parameters detected!:", changes
            key = raw_input("Continue anyway? (y/n)")

            if key != "y":
                sk.close()
                del sk
                exit()

        #starts the main menu
        action = main_menu(ip)
        print "action=", action
        if action == '1':
            data = sk.check_rotation()
        action = main_menu(ip)


    except Exception:
        print"failed to connect to ip:", ip

    sk.close()
    del sk
    exit()



