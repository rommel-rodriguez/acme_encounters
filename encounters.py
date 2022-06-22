#!/usr/bin/env python3

"""
"""
# TODO: Disclaimer, not taking into account more than one turn per day of the
# week yet.


class Turn:
    """
    """
    def __init__(self, start_hour, start_minute, end_hour, end_minute):
        self.start_hour= start_hour
        self.start_minute = start_minute
        self.end_hour= end_hour
        self.end_minute = end_minute

    def is_overlap(self, other_turn):
        """ Checks if turns overlap based in hour and minute only
        other_turn - A Turn object
        """
        pass
        

# TODO: Should I include the employee name in ScheduleEntry and do away with
# Employee and encounters classes?  
class ScheduleEntry:
    """ Represents the day and time period a user checked in
    """
    def __init__(self, dow, turn):
        """
        dow - Day of Week
        turn - a turn object
        """
        self.dow = dow
        self.turn = turn

    def is_encounter(self, sentry):
        """
        sentry - A ScheduleEntry type object
        """
        # TODO: Needs to handle military time and consider boundary cases like:
        # 00:00 or not as the cross from one day to the other.
        # TODO Handle repeated entries from the same employee?
        # Need to include the employee's name in this class to do so
        return (self.dow == sentry.dow) and self.turn.is_overlap(sentry.turn)

# class EmployeeSchedule():
#     """ Per-employee Weekly Schedule
#     """
#     def __init__(self, name):
#         self.name = name
#         self.schedule = []
# 
#     def register_entry(self, entry):
#         """
#         entry - ScheduleEntry object
#         """
#         pass


class EmployeeScheduleList():
    """ Contains all schedules of all employees 
    """
    def __init__(self, name):
        self.name = name
        # TODO: WARNING: This structure is incompatible with the rest of the design
        # re-think and find a consensus
        self.schedule_list = {'MO':[], 'TU':[],
                              'WE':[], 'TH':[], 'FR':[], 'SA':[], 'SU':[]}

    def register_entry(self, entry):
        """
        entry - ScheduleEntry object
        """
        pass

class Employee():
    """
    """
    def __init__(self,name):
        self.name = name


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
        print(f"[ERROR] File '{file_name}' not found in given path")
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
    file_name = input('Enter Employee schedule file: ')

    if checkfile(file_name):
        pass
    else:
        print(f"Terminating Process due to problems reading the file: {file_name}")

if __name__ == '__main__':
    # TODO: Consider adding some input test here
    main()
