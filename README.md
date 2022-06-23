# Count Employee Encounters 

**Using any kind of external library(or import) was avoided in the encounters.py script**
**Testing done with unittest**

## How to run:
1. `git clone https://github.com/rommel-rodriguez/acme_encounters.git /some/path`
2. `cd /some/path`
3. `python3 ./encounters.py`

## Overview

My program prompts the user for an input file name or file path, and outputs
a table that represents the number of encounters/schedule overlaps between two
ACME employees per table row. The rows are sorted using the names of the first
column as key.

## Architecture 

Several OOP concepts have been used, mainly for code isolation and readability.
1. The  main program logic reside in the EmployeeEncountersParser methods
    _parse_schedule_string, _parse_input_file and generate_table.
2. After creation an EmployeeEncountersParser object, the user only needs to call 
    the generate_table method, and this will fill the object's table attribute,
    which is the desired output table.
3. The EmployeeEncountersParser object state attributes are:
    - entry_dict - Dictionary with two-letter keys representing the 7 days of
        the week, the values are list of ScheduleEntry objects
    - file_name
    - table(the desired output)

## Approach
## Methodology

## Rationale of the implementation:
1. point 1 
2. point 2

The program will prompt for a filename, the file must at least
be readable by the user or the program will terminate
