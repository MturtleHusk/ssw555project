import unittest
import mi
import ged

class miTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_us06(self):
        self.assertEqual(mi.us06("testfiles/test-us06.ged"),
        	['Error US06: Divorce date of jason /Wong/ (I01) occurs after Death date'])

    def test_us09(self):
        self.assertEqual(mi.us09("testfiles/test-us09.ged"),
        	['Error US09: Death date of Alex /Jones/ (3 JAN 1938) occurs before birth date'])

    def test_us12(self):
        self.assertEqual(mi.us12("testfiles/test-us12.ged"),
        	['Error US12: Father Alex /Jones/ (I01) is at least 80 years older than his child'])

    def test_us21(self):
        self.assertEqual(mi.us21("testfiles/test-us12.ged"),
        	['Error US21: Gender of Alex /Jones/ (I01) does not match family role', 'Error US21: Gender of Lacy /jones/ (I07) does not match family role'])       



if __name__ == '__main__':
    unittest.main()
