#!/usr/bin/env python3

"""
"""

INPUT_FILE = ''

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

class Employee():
    """
    """
    def __init__(self,name):
        pass




if __name__ == '__main__':
    pass
