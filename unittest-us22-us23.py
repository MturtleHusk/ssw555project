import unittest
from ged import validate_ged

class TestUS22US23(unittest.TestCase):
    def setUp(self):
        pass

    def test_duplicate_id_individuals(self):
        self.assertEqual(
            validate_ged(
                { \
                    'individuals': { \
                        'I01': { \
                            'NAME': 'Jeff /Johnson/', \
                            'BIRT': '1 JAN 1950', \
                            'SEX': 'M', \
                            'FAMS': 'F01', \
                            'dup': [
                                { \
                                    'NAME': 'Jill /Johnson/', \
                                    'BIRT': '2 FEB 1960', \
                                    'SEX': 'F', \
                                    'FAMS': 'F01' \
                                } \
                            ] \
                        }, \
                    }, \
                    'families': { \
                        'F01': { \
                            'MARR': '18 JUL 1977', \
                            'HUSB': 'I01', \
                            'WIFE': 'I02' \
                        } \
                    } \
                } \
            ), \
            ['Error US22: Duplicate ID I01 in individuals'])

    def test_duplicate_id_families(self):
        self.assertEqual(
            validate_ged(
                { \
                    'individuals': { \
                        'I01': { \
                            'NAME': 'Jeff /Johnson/', \
                            'BIRT': '1 JAN 1950', \
                            'SEX': 'M', \
                            'FAMS': 'F01' \
                        }, \
                        'I02': { \
                            'NAME': 'Jill /Johnson/', \
                            'BIRT': '2 FEB 1960', \
                            'SEX': 'F', \
                            'FAMS': 'F01' \
                        } \
                    }, \
                    'families': { \
                        'F01': { \
                            'MARR': '18 JUL 1977', \
                            'HUSB': 'I01', \
                            'WIFE': 'I02', \
                            'dup': [ { \
                                'MARR': '12 JUN 1984', \
                                'HUSB': 'I01', \
                                'WIFE': 'I02' \
                            } ] \
                        } \
                    } \
                } \
            ), \
            ['Error US22: Duplicate ID F01 in families'])
    
    def test_duplicate_name_birt(self):
        self.assertEqual(
            validate_ged(
                { \
                    'individuals': { \
                        'I01': { \
                            'NAME': 'Jeff /Johnson/', \
                            'BIRT': '1 JAN 1950', \
                            'SEX': 'M', \
                            'FAMS': 'F01', \
                        }, \
                        'I02': { \
                            'NAME': 'Jill /Johnson/', \
                            'BIRT': '8 AUG 1960', \
                            'SEX': 'F', \
                            'FAMS': 'F01', \
                        }, \
                        'I03': { \
                            'NAME': 'Jeff /Johnson/', \
                            'BIRT': '1 JAN 1950', \
                            'SEX': 'M', \
                            'FAMS': 'F01', \
                        } \
                    }, \
                    'families': { \
                        'F01': { \
                            'MARR': '18 JUL 1977', \
                            'HUSB': 'I01', \
                            'WIFE': 'I02' \
                        } \
                    } \
                } \
            ), \
            ['Error US23: Duplicate name/birthday pair (IDs I01 and I03)'])


if __name__ == '__main__':
    unittest.main()
