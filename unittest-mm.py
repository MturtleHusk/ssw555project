import unittest
import mm

class TestMM(unittest.TestCase):
    def setUp(self):
        pass

    def test_us22_duplicate_individual_ids(self):
        self.assertEqual(
            mm.us22(
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

    def test_us22_duplicate_family_ids(self):
        self.assertEqual(
            mm.us22(
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
    
    def test_us23(self):
        self.assertEqual(
            mm.us23(
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

    def test_us14(self):
        self.assertEqual(
            mm.us14(
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
                            'BIRT': '1 JAN 1980', \
                            'SEX': 'F', \
                            'FAMS': 'F01', \
                        }, \
                        'I03': { \
                            'NAME': 'Joe /Johnson/', \
                            'BIRT': '1 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I04': { \
                            'NAME': 'Bob /Johnson/', \
                            'BIRT': '1 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I05': { \
                            'NAME': 'Steve /Johnson/', \
                            'BIRT': '1 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I06': { \
                            'NAME': 'Will /Johnson/', \
                            'BIRT': '1 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I07': { \
                            'NAME': 'Carl /Johnson/', \
                            'BIRT': '1 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I08': { \
                            'NAME': 'Pete /Johnson/', \
                            'BIRT': '1 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                    }, \
                    'families': { \
                        'F01': { \
                            'MARR': '18 JUL 1977', \
                            'HUSB': 'I01', \
                            'WIFE': 'I02', \
                            'CHIL': 'I03', \
                            'CHIL': 'I04', \
                            'CHIL': 'I05', \
                            'CHIL': 'I06', \
                            'CHIL': 'I07', \
                            'CHIL': 'I08', \
                        } \
                    } \
                } \
            ), \
            ['Anomaly US14: Family F01 contains more than five siblings born on the same day'])

    def test_us15(self):
        self.assertEqual(
            mm.us15(
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
                            'BIRT': '1 JAN 1980', \
                            'SEX': 'F', \
                            'FAMS': 'F01', \
                        }, \
                        'I03': { \
                            'NAME': 'Joe /Johnson/', \
                            'BIRT': '1 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I04': { \
                            'NAME': 'Bob /Johnson/', \
                            'BIRT': '2 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I05': { \
                            'NAME': 'Steve /Johnson/', \
                            'BIRT': '3 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I06': { \
                            'NAME': 'Will /Johnson/', \
                            'BIRT': '4 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I07': { \
                            'NAME': 'Carl /Johnson/', \
                            'BIRT': '5 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I08': { \
                            'NAME': 'Pete /Johnson/', \
                            'BIRT': '6 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I09': { \
                            'NAME': 'Frank /Johnson/', \
                            'BIRT': '7 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I10': { \
                            'NAME': 'Bill /Johnson/', \
                            'BIRT': '8 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I11': { \
                            'NAME': 'Mike /Johnson/', \
                            'BIRT': '9 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I12': { \
                            'NAME': 'Mark /Johnson/', \
                            'BIRT': '10 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I13': { \
                            'NAME': 'Kyle /Johnson/', \
                            'BIRT': '11 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I14': { \
                            'NAME': 'Grant /Johnson/', \
                            'BIRT': '12 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I15': { \
                            'NAME': 'Nick /Johnson/', \
                            'BIRT': '13 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I16': { \
                            'NAME': 'Jeff /Johnson/', \
                            'BIRT': '14 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I17': { \
                            'NAME': 'Walter /Johnson/', \
                            'BIRT': '15 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        }, \
                        'I18': { \
                            'NAME': 'Guy /Johnson/', \
                            'BIRT': '16 JAN 1980', \
                            'SEX': 'M', \
                            'FAMC': 'F01', \
                        } \
                    }, \
                    'families': { \
                        'F01': { \
                            'MARR': '18 JUL 1977', \
                            'HUSB': 'I01', \
                            'WIFE': 'I02', \
                            'CHIL': [ 'I03','I04','I05','I06','I07','I08','I09','I10','I11','I12','I13','I14','I15','I16','I17','I18'] \
                        } \
                    } \
                } \
            ), \
            ['Anomaly US15: Family F01 contains more than 15 siblings'])

if __name__ == '__main__':
    unittest.main()
