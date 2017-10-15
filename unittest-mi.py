import unittest
import mi
import ged

class miTest(unittest.TestCase):

    def test_us06(self):
        self.assertEqual(mi.us06(
            ged.parse_ged(ged.read_ged("testfiles/test-us06.ged").split("\n"))
        ),
        ['Error US06: Divorce date of jason /Wong/ (I01) occurs after Death date'])

    def test_us09(self):
        self.assertEqual(mi.us09(
            ged.parse_ged(ged.read_ged("testfiles/test-us09.ged").split("\n"))
        ),
        ['Error US09: Death date of Alex /Jones/ (3 JAN 1938) occurs before birth date'])
