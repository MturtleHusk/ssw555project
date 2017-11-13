import unittest
import mi
import ged
from ged import parse_ged

class miTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_us06(self):
        with open ("testfiles/test-us06.ged") as f:
            parsed = parse_ged(f.read().split('\n'))
            self.assertEqual(mi.us06(parsed),
                             ['Error US06: Divorce date of jason /Wong/ (I01) occurs after Death date'])

    def test_us09(self):
        with open ("testfiles/test-us09.ged") as f:
            parsed = parse_ged(f.read().split('\n'))
            self.assertEqual(mi.us09(parsed),
                             ['Error US09: Death date of Alex /Jones/ (3 JAN 1938) occurs before birth date'])

    def test_us12(self):
        with open ("testfiles/test-us12.ged") as f:
            parsed = parse_ged(f.read().split('\n'))
            self.assertEqual(mi.us12(parsed),
                             ['Anomaly US12: Father Alex /Jones/ (I01) is at least 80 years older than his child'])

    def test_us21(self):
        with open ("testfiles/test-us21.ged") as f:
            parsed = parse_ged(f.read().split('\n'))
            self.assertEqual(mi.us21(parsed),
                             ['Anomaly US21: Gender of Alex /Jones/ (I01) does not match family role', 'Anomaly US21: Gender of Lacy /jones/ (I07) does not match family role'])       



    def test_us29(self):
        with open ("testfiles/test-us29.ged") as f:
            parsed = parse_ged(f.read().split('\n'))
            self.assertEqual(mi.us29_list(parsed),
                             ['US29: List of deceased individuals:', ['Alex /Jones/ (I01)', 'Lacy /jones/ (I07)']])

    def test_us34(self):
        with open ("testfiles/test-us34.ged") as f:
            parsed = parse_ged(f.read().split('\n'))
            self.assertEqual(mi.us34_list(parsed),
                             ['US34: List couples married with one spouse twice the age of the other:', ['Alex /Jones/ and Lacy /jones/ (F23)']])
if __name__ == '__main__':
    unittest.main()
