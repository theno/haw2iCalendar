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

