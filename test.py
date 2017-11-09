import unittest
import ged
import yl


class TestUS17(unittest.TestCase):

    def setUp(self):
        self.ged = ged.parse_ged(ged.read_ged("testfiles/test-us17.ged").split("\n"))
        self.result = yl.us17(self.ged)

    def test_equal(self):
        self.assertEqual(1, len(self.result))

    def test_true(self):
        self.assertTrue(isinstance(self.result, list))

    def test_not_none(self):
        self.assertIsNotNone(self.result)

    def test_in(self):
        self.assertIn("Jennifer", self.result[0])

    def test_regex(self):
        self.assertRegex(self.result[0], "\s*Jennifer\s*")
