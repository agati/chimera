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

import sys

from chimera.core.cli import ChimeraCLI


class ChimeraWheater(ChimeraCLI):
    print"comecando.."

    def __init__(self):
        ChimeraCLI.__init__(self, "chimera-wheater", "Chimera Wheater Controller", 0.1, port=9005)

        self.addHelpGroup(self, "WHEATER", "Wheater conditions info")

        self.addInstrument(name="wheaterstation",
                           cls="WheaterStation",
                           help="Wheater instrument to be used.",
                           helpGroup="WHEATER", required=True)

        self.addParameters(dict(name="humidity",
                                short="i",
                                type="int",
                                default=1,
                                helpGroup="WHEATER",
                                help="External humidity in %"),
                           dict(name="temperature",
                                short="t",
                                type="int",
                                default=1,
                                helpGroup="WHEATER",
                                help="External temperature in Celsius degrees"),
                           )


def main():
    cli = ChimeraWheater()
    cli.run(sys.argv)
    cli.wait()


if __name__ == '__main__':
    main()
