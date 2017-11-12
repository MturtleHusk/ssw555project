import unittest
import ged
import mf

class TestMF(unittest.TestCase):
    def test_us03(self):
        self.assertEqual(mf.US03(
            ged.parse_ged(ged.read_ged("testfiles/test-us03.ged").split("\n"))
        ),
            ['Error US03: Users [ I01 ] have died before being born']

        )

    def test_us30(self):
        self.assertEqual(mf.US30_list(
            ged.parse_ged(ged.read_ged("testfiles/test-us30.ged").split("\n"))
        ),
            ['US30: list of married couples:', [['I26', 'I27']]]
        )

    def test_us35(self):
        self.assertEqual(mf.US35(
            ged.parse_ged(ged.read_ged("testfiles/test-us35.ged").split("\n"))
        ),
            ['US35: no recent births']

        )


    #this text is time limited, will fail in 29 days
    def test_us36(self):
        self.assertEqual(mf.US36(
            ged.parse_ged(ged.read_ged("testfiles/test-us36.ged").split("\n"))
        ),
            ['US36: recent deaths - I01 ']
        )

    # this text is time limited, will fail in 29 days
    def test_us38(self):
        self.assertEqual(mf.US38(
            ged.parse_ged(ged.read_ged("testfiles/test-us38.ged").split("\n"))
        ),
            ['US38: no upcoming birthdays']
        )

    # this text is time limited, will fail in 29 days
    def test_us39(self):
        self.assertEqual(mf.US39(
            ged.parse_ged(ged.read_ged("testfiles/test-us39.ged").split("\n"))
        ),
            ['US39: no upcoming anniversaries']
        )

    def test_us42(self):
        self.assertEqual(mf.US42_list(
            ged.parse_ged(ged.read_ged("testfiles/test-us42.ged").split("\n"))
        ),
            ['US42: Invalid dates:', [['I01', '32 JUL 1960'], ['I19', '112 FEB 1981']], [['F24', '45 AUG 2004']]]
        )

    def test_us41(self):
        self.assertEqual(mf.US41_list(
            ged.parse_ged(ged.read_ged("testfiles/test-us41.ged").split("\n"))
        ),
            ['US41: All Dates Made Valid:', [['I02', '10 SEP 1960'], ['I01', '10 JAN 2017']], [['F23', '10 JAN 1980']]]
        )



if __name__ == '__main__':
    unittest.main()
#    print(mf.US41_list(ged.parse_ged(ged.read_ged("testfiles/test-us41.ged").split("\n"))))