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
    for key, value in result_table.items():
        print(f"{key[0]}-{key[1]}:\t{value}")


class Turn:
    """ Represent a working turn, with an start and end hour and minute
    """
    def __init__(self, start_hour, start_minute, end_hour, end_minute):
        """
        start_hour - An integer number between 0 and 23
        start_minute - An integer number between 0 and 59
        end_hour - An integer number between 0 and 23
        end_minute - An integer number between 0 and 59
        """
        # TODO: Add testing for invalid hours
        self.start_hour= start_hour
        self.start_minute = start_minute
        self.end_hour= end_hour
        self.end_minute = end_minute

    def is_overlap(self, other_turn):
        """ Checks if turns overlap based in hour and minute only

        Boundary cases do not count as overlaps, if the end hour and minute
        of a turn coincides exactly with the start hour and minute of another
        turn if does not count as an overlap

        other_turn - A Turn object
        returns False if there is no overlap, and True if there is
        """
        # TODO: Not taking into account ilogical time frames like a case in
        # and employee checks-in and -out immediately
        # Note: if's logic separated into 2 to improve readability
        if (self.start_hour >= other_turn.end_hour and
            self.start_minute >= other_turn.end_minute):
            return False
        if (self.end_hour <= other_turn.start_hour and
            self.end_minute <= other_turn.start_minute):
            return False
        return True

    def __str__(self):
        # msg = f"{self.start_hour}:{self.start_minute}-{self.end_hour}:{self.end_minute}"
        msg = "{self.start_hour}:{self.start_minute}-{self.end_hour}:{self.end_minute}"
        return  msg.format(self = self)

    def __eq__(self, other):
        return (self.start_hour == other.start_hour and
                self.start_minute == other.start_minute and
                self.end_hour == other.end_hour and
                self.end_minute == other.end_minute )


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

# TODO: Should I include the employee name in ScheduleEntry and do away with
# Employee and encounters classes?
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
        """
        sentry - A ScheduleEntry type object
        """
        # TODO: Needs to handle military time and consider boundary cases like:
        # 00:00 or not as the cross from one day to the other.
        # TODO Handle repeated entries from the same employee?
        # Need to include the employee's name in this class to do so
        if self.emp == sentry.emp:
            return False
        # TODO: Depending on the logic consider removing the dow to dow test
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
        # TODO: WARNING: This structure is incompatible with the rest of the design
        # re-think and find a consensus
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
        # At most 7 loops here
        for t in turns_list:
            tup = tuple()
            dow = t[:2]
            tup += (dow, )
            hours_list = t[2:].strip().split('-')
            # TODO: Careful here
            start_list, end_list = (h.strip().split(':') for h in hours_list)
            # TODO: Handle Exceptions in case h can not be casted
            # TODO: Add control to skip out-of-bound hour and minute
            tup += (int(start_list[0]), int(start_list[1]))
            tup += (int(end_list[0]), int(end_list[1]))
            # TODO: Test which one is more efficient
            sched_list.append(tup)

        return sched_list


    def _parse_input_file(self):
        """ Takes care of the initial parsing of the input file
        Already assumes that the file exists and is readable
        """
        with open(self.file_name, 'rb') as sched_file:
            for emp_line in sched_file: 
                emp_line = emp_line.strip().decode('utf8')
                emp_name, sched_str = emp_line.split('=')
                emp_name = emp_name.upper()
                emp = Employee(emp_name)
                sched_list  = self._parse_schedule_string(sched_str)
                # At most 7 loops
                for tf in sched_list:
                    dow = tf[0]
                    emp_turn = Turn(*tf[1:])
                    entry = ScheduleEntry(emp, dow, emp_turn)
                    self.entry_dict[dow].append(entry)


    def enter_new_file(self, new_file_name):
        """ Takes care of processing more than 1 input file"""
        self.file_name = new_file_name
        self.generate_table()

    def generate_table(self):
        """ Generates the output table and assigns it to attribute table """
        # TODO: Must support already existing table
        # TODO: Consider prepending _ to the parse_input_file method
        self._parse_input_file()
        # TODO: WARNING: This is the problem, this loop is at worst
        # of order n, making the total O(n^2)
        # TODO: First Compare with entries in same day, the append
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
    file_name = input('Enter Employee schedule file: ').strip()

    if checkfile(file_name):
        parser = EmployeeEncountersParser(file_name)
        parser.generate_table()
        print_table(parser.table)
    else:
        print(f"Terminating Process due to problems reading the file: {file_name}")

if __name__ == '__main__':
    # TODO: Consider adding some input test here
    main()
