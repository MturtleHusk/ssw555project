import unittest
import ged
import yl


class TestYL(unittest.TestCase):

    def test_us07(self):
        self.assertEqual(yl.us07(
            ged.parse_ged(ged.read_ged("testfiles/test-us07.ged").split("\n"))
        ),
        ["Anomaly US07: John Smith (I28) is more than 150 years old."])

    def test_us08(self):
        self.assertEqual(yl.us08(
            ged.parse_ged(ged.read_ged("testfiles/test-us08.ged").split("\n"))
        ),
            ["Anomaly US08: Dick /Smith/ (I19) was born before marriage of parents.",
             "Anomaly US08: Jane /Smith/ (I26) was born after more than 9 months of divorce of parents."]
        )

    def test_us16(self):
        self.assertEqual(yl.us16(
            ged.parse_ged(ged.read_ged("testfiles/test-us16.ged").split("\n"))
        ),
            ["Anomaly US16: Not all male members of family F23 have the same last name."]
        )

    def test_us20(self):
        self.assertEqual(yl.us20(
            ged.parse_ged(ged.read_ged("testfiles/test-us20.ged").split("\n"))
        ),
            ["Anomaly US20: Alex /Smith/ (I31) marries his nieces Jane /Smith/ (I18)"]
        )

    def test_us19(self):
        self.assertEqual(yl.us19(
            ged.parse_ged(ged.read_ged("testfiles/test-us19.ged").split("\n"))
        ),
            ["Anomaly US19: Dick /Smith/ (I17) marries his first cousin Jane /Smith/ (I18)."]
        )

    def test_us28(self):
        self.assertEqual(yl.us28_list(
            ged.parse_ged(ged.read_ged("testfiles/test-us28.ged").split("\n"))
        ),
            ["US28: List siblings in families by decreasing age:",
             [["F23", ["I19", "Dick /Smith/", "13 FEB 1981"], ["I26", "Jane /Smith/", "2 JUN 1983"]]]
             ]
        )
