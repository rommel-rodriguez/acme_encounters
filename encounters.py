#!/usr/bin/env python3

"""
"""

INPUT_FILE = ''

class Employee():
    """
    """
    def __init__(self,name):
        pass

class Encounters():
    """ Keeps track of multiple user coincidences in the office
    Must implement an efficient algorithm to add to the value of existing keys
    and to add new keys if necessary 

    meetings - a dictionary in which the keys are pairs of strings representing
               a pair of user names
    """
    pass

def checkfile(file_name):
    """ Check if we can open and read a file named file_name """
    try:
        # TODO: Test that 'rb' works on windows as well
        fh = open(file_name, 'rb')
        fh.close()
    except FileNotFoundError:
        print(f"[ERROR] File {file_name} not found in given path")
        return False
    # TODO: Add more specific exceptions for common errors like
    # errors for lack of Permission to read the file
    except BaseException as e:
        # TODO: Add a more custom message 
        print("Something went wrong!: ")
        print(e)
        return False
    return True

def main():
    # TODO: Consider making INPUT_FILE local to main
    INPUT_FILE = input('Enter Employee schedule file: ')

if __name__ == '__main__':
    # TODO: Consider adding some input test here
    main()
