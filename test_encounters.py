""" Test harness file for functionality in encounters.py
"""
import unittest
import encounters

class EncountersTestCase(unittest.TestCase):
    def setUp(self):
       self.en = encounters

    def test_checkfile(self):
        """ Sets the filenames to test the checkfile function
        """
        # TODO: Do the appropiate modifications when moving the test
        # harness to its own folder
        # TODO: If appropiate create a shell script to setup 
        # the files that must exists and files with restricted read
        # permissons

        f_exists = "./sample_input1.txt"
        fnot_exists = "./non_existent.txt"
        self.assertTrue(self.en.checkfile(f_exists))
        self.assertFalse(self.en.checkfile(fnot_exists))


if __name__ == '__main__':
    unittest.main()
