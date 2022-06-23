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
# TODO: Disclaimer, not taking into account more than one turn per day of the
# week yet.

def checkfile(file_name):
    """ Check if we can open and read a file named file_name(str) """
    try:
        fh = open(file_name, 'rb')
        fh.close()
    except FileNotFoundError:
        print(f"[ERROR] File '{file_name}' not found in given path")
        return False
    except BaseException as err:
        # TODO: Add a more custom message
        print("Something went wrong!: ")
        print(err)
        return False
    return True


def print_table(result_table):
    """ Prints the result table for the final output
    result_table - a dictionary with a two-element tuple as key
                   and an int as value
    """
    for key, value in sorted(result_table.items()):
        print(f"{key[0]}-{key[1]}:\t{value}")

class BoundaryTime:
    """ Represents a specific time's Hour and Minute
    Must be able to tell if the time is valid military time
    """
    def __init__(self, hour, minute):
        """
        hour - an int type object
        minute - an int type object
        """
        self.hour = hour
        self.minute = minute

    def __ge__(self, other):
        if other.hour > self.hour:
            return False

        if  other.hour < self.hour:
            return True

        return self.minute >= other.minute

    def __le__(self, other):
        if other.hour > self.hour:
            return True

        if  other.hour < self.hour:
            return False

        return self.minute <= other.minute

    def __lt__(self, other):
        if self.hour < other.hour:
            return True

        if self.hour > other.hour:
            return False

        return self.minute < other.minute

    def __eq__(self, other):
        return (self.hour == other.hour and self.minute == other.minute )

    def is_valid_time(self):
        """ Validates that hour and minute is whithin sane boundaries """
        return (self.hour >= 0 and self.hour <= 23
                and self.minute >= 0 and self.minute <= 59)


class Turn:
    """ Represent a working turn, with an start and end hour and minute
    """
    def __init__(self, start_time, end_time):
        """
        start_time - A BoundaryTime Object
        end_time - A BoundaryTime Object
        """
        self.start_time = start_time
        self.end_time = end_time

    def is_overlap(self, other_turn):
        """ Checks if turns overlap based in hour and minute only

        Boundary cases do not count as overlaps, if the end hour and minute
        of a turn coincides exactly with the start hour and minute of another
        turn if does not count as an overlap

        other_turn - A Turn object
        returns False if there is no overlap, and True if there is
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
        if not (self.start_time.is_valid_time()
                and self.end_time.is_valid_time()):
            return False
        return self.start_time <= self.end_time


    def __str__(self):
        # msg = f"{self.start_hour}:{self.start_minute}-{self.end_hour}:{self.end_minute}"
        msg = "{self.start_hour}:{self.start_minute}-{self.end_hour}:{self.end_minute}"
        return  msg.format(self = self)

    def __eq__(self, other):
        return (self.start_time == other.start_time and
                self.end_time == other.end_time)


class Employee():
    """ Represents an ACME Employee
    name - String
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
    """
    def __init__(self, emp, dow, turn):
        """
        emp - A Employee object
        dow - Day of Week as a two-character string
        turn - a Turn object
        """
        self.emp = emp
        self.dow = dow
        self.turn = turn

    def is_encounter(self, sentry):
        """ Checks if there is a schedule overlap(encounter) between employees
        sentry - A ScheduleEntry type object
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
    """
    def __init__(self, file_name):
        """ file_name - str name of a appropiately formate file"""

        self.entry_dict = {'MO':[], 'TU':[],
                           'WE':[], 'TH':[],
                           'FR':[], 'SA':[],
                           'SU':[]}

        self.file_name = file_name
        self.table = {}

    def _parse_schedule_string(self, sched_str):
        """ Parses a string in a know format and outputs a list of tuples

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
                # NOTE: Careful here
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
        with open(self.file_name, 'rb') as sched_file:
            for emp_line in sched_file:
                emp_line = emp_line.strip().decode('utf8')
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
                    start_time = BoundaryTime(*tf[1:3])
                    end_time = BoundaryTime(*tf[3:])
                    emp_turn = Turn(start_time, end_time)
                    if not emp_turn.is_valid_turn():
                        continue
                    entry = ScheduleEntry(emp, dow, emp_turn)
                    self.entry_dict[dow].append(entry)


    def enter_new_file(self, new_file_name):
        """ Takes care of processing more than 1 input file"""
        self.file_name = new_file_name
        self.generate_table()

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
    file_name = input('Enter Employee schedule file: ').strip()

    if checkfile(file_name):
        parser = EmployeeEncountersParser(file_name)
        parser.generate_table()
        print_table(parser.table)
    else:
        print(f"Terminating Process due to problems reading the file: {file_name}")

if __name__ == '__main__':
    main()
