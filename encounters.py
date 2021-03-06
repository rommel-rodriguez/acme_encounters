#!/usr/bin/env python3

""" Counter of encounters of pairs of employees in the office

Prompts the user for input from the standard input and prints the table
of number of encounters by each pair of employees.
The file must conform to the format:
    RENE=MO10:15-12:00,TU10:00-12:00,TH13:00-13:15,SA14:00-18:00,SU20:00-21:00
where the first field is the name delimited by a =, followed by at most
seven time ranges identified by the day of week first 2 letters and the format
of the hours must follow the military style(e.g. 18:00 instead of 6p.m.).
"""

import argparse
import sys
from datetime import time

def parse_cmd():
    """Takes care of parsing command line arguments
    """
    desc = "Counter of encounters of pairs of employees in the office"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', '--filename',
                        type=str,
                        help="Input file with the Employee schedules")

    args = parser.parse_args()

    return args.filename

def checkfile(file_name):
    """ Check if we can open and read a file named file_name(str)
    file_name : str
    """
    try:
        fh = open(file_name, 'rb')
        fh.close()
    except FileNotFoundError:
        print(f"[ERROR] File '{file_name}' not found in given path")
        return False
    except IsADirectoryError:
        print(f"[ERROR] '{file_name}' is a directory not a file")
        return False
    except BaseException as err:
        print("Something went wrong!: ")
        print(err)
        return False
    return True

def print_table(result_table):
    """ Prints the result table for the final output
    result_table : dictionary with a two-element tuple as key
                   and an int as value
    """
    for key, value in sorted(result_table.items()):
        print(f"{key[0]}-{key[1]}:\t{value}")

class Turn:
    """ Represent a working turn, with an start and end hour and minute
    Attributes
    ----------
    start_time : datetime.time
        Represents the  tarting time
    end_time :  datetime.time
        Represents the end of the turn

    Methods
    -------
    is_overlap()
        Checks if turns overlap based in hour and minute only
    is_valid_turn()
        Checks whether the start time is lower or equal to end time
    """
    def __init__(self, start_time, end_time):
        """
        Parameters
        ----------
        start_time :  datetime.time
            Represents the  tarting time
        end_time : datetime.time
            Represents the end of the turn
        """
        self.start_time = start_time
        self.end_time = end_time

    def is_overlap(self, other_turn):
        """ Checks if turns overlap based in hour and minute only

        other_turn : Turn object
        returns False if there is no overlap, and True if there is

        Boundary cases do not count as overlaps, if the end hour and minute
        of a turn coincides exactly with the start hour and minute of another
        turn if does not count as an overlap

        """

        if (self.start_time >= other_turn.end_time or
            self.end_time <= other_turn.start_time):
            return False

        return True

    def is_valid_turn(self):
        """ Checks whether the start time is lower or equal to end time """
        # NOTE: If the start and end times are equal, it is assumed that there
        # was an input error when writing the records, but is stil accepted
        # as is useful for logging, but out-of-bounds times are not accepted

        return self.start_time <= self.end_time


    def __str__(self):
        msg = "{self.start_hour}:{self.start_minute}-{self.end_hour}:{self.end_minute}"
        return  msg.format(self = self)

    def __eq__(self, other):
        return (self.start_time == other.start_time and
                self.end_time == other.end_time)


class Employee():
    """ Represents an ACME Employee
    Attributes
    ----------
    name : str
        Employee's name
    """
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class ScheduleEntry:
    """ Represents a single employee's turn in a week
    Characterized by an employee object, day of the week and the time frame
    in which he/she was at the office
    Attributes
    ----------
    emp : Employee
        Represents the owner of this entry
    dow : str
        Day of Week as a two-character string
    turn : Turn
        Represents the time frame of this entry

    Methods
    -------
    is_encounter()
        Checks if there is a schedule overlap(encounter) between employees
    """
    def __init__(self, emp, dow, turn):
        """
        Parameters
        ----------
        emp : Employee
            Represents the owner of this entry
        dow : str
            Day of Week as a two-character string
        turn : Turn
            Represents the time frame of this entry
        """
        self.emp = emp
        self.dow = dow
        self.turn = turn

    def is_encounter(self, sentry):
        """ Checks if there is a schedule overlap(encounter) between employees
        sentry : ScheduleEntry type
            Another  ScheduleEntry object to compare with
        """
        if self.emp == sentry.emp:
            return False

        return self.dow == sentry.dow and self.turn.is_overlap(sentry.turn)

    def __str__(self):
        return "{self.emp}={self.dow}{self.turn}".format(self = self)

    def __eq__(self, other):
        return (self.emp  == other.emp and
                self.dow == other.dow and
                self.turn == other.turn)


class EmployeeEncountersParser():
    """ Contains all schedules of all employees
    Attributes
    ----------
    entry_dict : dict
        Keys are 2-letter string and values and list of ScheduleEntry
        objects
    file_name : str
        Input file name or path
    table : dict
        Keys are 2-element tuples representing employee names, the values
        are the number of schedule overlaps between the 2

    Methods
    -------
    _parse_schedule_string(str)
        Parses a string in a know format and outputs a list of tuples
    _parse_input_file()
        Takes care of the initial parsing of the input file
    generate_table()
        Generates the output table and assigns it to attribute table
    """
    def __init__(self, file_name):
        """ file_name : str, name of a appropiately formate file"""

        self.entry_dict = {'MO':[], 'TU':[],
                           'WE':[], 'TH':[],
                           'FR':[], 'SA':[],
                           'SU':[]}

        self.file_name = file_name
        self.table = {}

    def _parse_schedule_string(self, sched_str):
        """ Parses a string in a know format and outputs a list of tuples
        sched_str : str
            Represents an input line with the username and = sign removed
        Returns a list of tuples, each with five elements representing
         (dow, start_hour, start_minute, end_hour, end_minute ) ->
         (str, int, int, int ,int)
        """
        sched_list = []
        turns_list = sched_str.strip().split(',')
        # At most 7 iterations here
        for t in turns_list:
            tup = tuple()
            try:
                dow = t[:2]
                tup += (dow, )
                hours_list = t[2:].strip().split('-')
                start_list, end_list = (h.strip().split(':') for h in hours_list)
                tup += (int(start_list[0]), int(start_list[1]))
                tup += (int(end_list[0]), int(end_list[1]))
                sched_list.append(tup)
            except BaseException as err:
                # print(f"[ERROR] Malformed Turn string :{t}")
                # print(err)
                continue

        return sched_list


    def _parse_input_file(self):
        """ Takes care of the initial parsing of the input file
        Already assumes that the file exists and is readable
        """
        with open(self.file_name, 'r', encoding='utf-8') as sched_file:
            for emp_line in sched_file:
                emp_line = emp_line.strip()
                if not emp_line:
                    continue
                try:
                    emp_name, sched_str = emp_line.split('=')
                except ValueError:
                    continue

                emp_name = emp_name.upper()
                emp = Employee(emp_name)
                sched_list  = self._parse_schedule_string(sched_str)
                # At most 7 loops
                for tf in sched_list:
                    dow = tf[0]
                    try:
                        start_time = time(*tf[1:3])
                        end_time = time(*tf[3:])
                    except ValueError:
                        continue
                    emp_turn = Turn(start_time, end_time)
                    if not emp_turn.is_valid_turn():
                        continue
                    entry = ScheduleEntry(emp, dow, emp_turn)
                    self.entry_dict[dow].append(entry)

    def generate_table(self):
        """ Generates the output table and assigns it to attribute table """
        self._parse_input_file()
        for dow,dow_elist in self.entry_dict.items():
            dl = len(dow_elist)
            for i in range(dl-1) :
                cur_ent = dow_elist[i]
                for j in range(i+1, dl):
                    test_ent = dow_elist[j]
                    if cur_ent.is_encounter(test_ent):
                        pair_list = [cur_ent.emp.name, test_ent.emp.name]
                        pair_list.sort()
                        pair_key = tuple(pair_list)
                        self.table[pair_key] = self.table.get(pair_key, 0) + 1


def main():
    """ Function to execute when script is called as __main__ """
    # file_name = input('Enter Employee schedule file: ').strip()
    file_name = parse_cmd()
    if not file_name:
        print("encounters.py needs an argument:")
        print("\tencounters.py -f FILENAME")
        sys.exit(1)

    file_name = file_name.strip()
    if checkfile(file_name):
        sched_parser = EmployeeEncountersParser(file_name)
        sched_parser.generate_table()
        print_table(sched_parser.table)
    else:
        print(f"Terminating Process due to problems reading the file: {file_name}")
        sys.exit(1)

if __name__ == '__main__':
    main()
