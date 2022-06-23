# Count Employee Encounters 

**Using any kind of external library(or import) was avoided in the encounters.py script**

**Testing done with unittest**

## How to run on Linux:
1. `git clone https://github.com/rommel-rodriguez/acme_encounters.git /some/path`
2. `cd /some/path`
3. `python3 encounters.py`

## How to test
1. `python3 ./test_encounters.py`

To test encounters.py automatically with all the files under test_files there 
is a bash and expect scripts called test.sh and test.exp respectively. The script
needs the expect command/package to be installed. Runs test_encounters.py first.
On Ubuntu derivatives:

1. `apt install expect`
1. `bash test.sh`


## Overview

The program prompts the user for an input file name or file path, and outputs
a table that represents the number of encounters/schedule overlaps between two
ACME employees per table row. The rows are sorted using the names of the first
column as key.

## Architecture 

Several OOP concepts have been used, mainly for code isolation and readability.
1. In BoundaryTime we find all the logic and sanity checks when dealing with
    a time boundary(the edge of a hour and minute of an schedule)

2. Turn is composed of 2 BoundaryTime time attributes an takes care to check
    that a turn is actually valid (e.g. that the lower boundary is lower or equal
    than the upper boundary)

3. The Employee class was created for optimization, all the ScheduleEntry
    objects for a particular employee will point to the same Employee object.

4. The ScheduleEntry object is composed of
    - emp - a Employee object
    - dow - str object standing for a two-letter representation of day of the week 
    - turn - A Turn object that represents the time frame
   In this class we define the method is_encounter, which compares the current
   object with another ScheduleEntry tells whether there is an overlap or not.

5. The  main program logic reside in the EmployeeEncountersParser class, which
    is composed as follows:
    Attributes:
    - entry_dict - Dictionary with two-letter keys representing the 7 days of
        the week, the values are list of ScheduleEntry objects
    - file_name - str representing the name of the input file 
    - table(the desired output) - A dictionary with two-element(employee names)
        tuples as keys and positive integers as values
    Methods:
    - _parse_schedule_string - Parses the week's schedule string after the
    employee's name has been removed
    - _parse_input_file - Loops through the file line by line and fills the 
    entry_dict dictionary, calls _parse_schedule_string.
    - generate_table - First calls  _parse_input_file then iterates through
    entry_dict and then each entry per day-of-week list, looking and registering
    encounters/schedule overlaps between pairs of employees and storing them in
    the table attribute.

6. After creation an EmployeeEncountersParser object, the user only needs to call 
    the generate_table method, and this will fill the object's table attribute,
    which is the desired output table.

## Approach
It was decided to store the ScheduleEntry objects inside the entry_dic, each
in a list exclusive to that day, so that finding overlaps was more efficient,
as we no longer have to compare entries from different days.

The functionality in the EmployeeEncountersParser.generate_table method could
have been included in the EmployeeEncountersParser._parse_input_file method,
but doing so only helps the performance a little and the complexity is not 
changed. On the other hand breaking the code this way, makes it easier to follow.

Some basic assumptions were made and some common error were handled:

### Assumptions:

    - The input file follows the same format that the provided
    - There will not be repeated entries in the file for the same user 
    - When an Employee's turn has the exact start and end time, it is considered
      an error while recording in the database/file, but it is still processed
### Handling of common errors:

    - Input-file-related errors were somewhat handled, specific handling of 
      FileNotFound, skipped specific handling of permission related error,
      though they are still reported to the user and terminate the program. 
    - Skip processing of lines of input file that are blank 
    - Skip addition of entries that raise any kind of exception while processing

## Methodology
- Agile practices were used when developing this program, with focus on testing
by providing a test harness with a test skeleton of the expected functionality of
initial prototype functions.

- Documentation has been provided by means of Python doc-strings and this
README file.

- The GIT program was used for source control, always with a 'dev' branch that was
forked when needed for feature-specific development, when ready they were merged
back to dev, then dev was merged back to main. Only the main branch and version
tags were pushed to the remote.

- Specific-feature branches were rebased as needed when other feature branches
were successfully merged to dev.

- The code was refactored a few times to improve maintainability and readability

- The code refactored code was then tested after the feature-branch merge

- The program was continuously tested after merges from feature branches using
the test harness as well as the sample and dummy files.
