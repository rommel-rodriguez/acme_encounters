""" Test harness file for functionality in encounters.py
"""
from encounters import *

def test_checkfile():
    """ Sets the filenames to test the checkfile function
    """
    # TODO: Do the appropiate modifications when moving the test
    # harness to its own folder
    f_exists = "./sample_input.txt"
    fnot_exists = "./non_existent.txt"
    assert checkfile(f_exists)
    assert checkfile(fnot_exists)
