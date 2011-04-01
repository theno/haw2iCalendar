
###########################################################################
#  Copyright 2011 Theodor Nolte                                           #
#                                                                         #
#  This file is part of haw2iCalendar.                                    #
#                                                                         #
#  haw2iCalendar is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  haw2iCalendar is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with haw2iCalendar.  If not, see <http://www.gnu.org/licenses/>. #
###########################################################################

import unittest

from veranstaltungenParser import VeranstaltungParser
from veranstaltungenDispatchProcessor import VeranstaltungDispatchProcessor
from veranstaltungenParserTest import tokenTestData

class TestDispatcher(unittest.TestCase):
    def testDeclaration(self):

        testData = tokenTestData["veranstaltung"]

        for testDatum in testData:
            success, children, nextcharacter = VeranstaltungParser.parse(testDatum, processor=VeranstaltungDispatchProcessor())
            def errStr():
                return children
            assert success and nextcharacter==len(testDatum), errStr()

if __name__ == "__main__":
    unittest.main()

