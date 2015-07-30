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


import logging
# from chimera.util.dumper import dumpObj

log = logging.getLogger(__name__)

from chimera.src.chimera.core.exceptions import ChimeraException


class SKDrvException(ChimeraException):
    def __init__(self, code, msg=""):
        ChimeraException.__init__(self, msg)
        self.code = code

    def __str__(self):
        return "%s (%d)" % (self.message, self.code)

