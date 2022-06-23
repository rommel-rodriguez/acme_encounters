""" Test harness file for functionality in encounters.py
"""
import unittest
import encounters

class EncountersTestCase(unittest.TestCase):
    # maxDiff = None
    def setUp(self):
        emp_name1='CHARLES'
        emp_name2='MARIAN'
        emp_name3='EDWARD'
        emp_name4='WENDY'
        self.en = encounters
        self.a_turn = self.en.Turn(20,30,21,45)
        self.b_turn = self.en.Turn(20,25,20,30)
        self.c_turn = self.en.Turn(21,30,22,30)
        self.d_turn = self.en.Turn(20,30,21,45)
        self.e_turn = self.en.Turn(18,30,19,00)
        self.emp1 = self.en.Employee(emp_name1)
        self.emp2 = self.en.Employee(emp_name2)
        self.emp3 = self.en.Employee(emp_name3)
        self.entry1 = self.en.ScheduleEntry(self.emp1, 'MO', self.a_turn)
        self.entry2 = self.en.ScheduleEntry(self.emp1, 'TU', self.b_turn)
        self.entry3 = self.en.ScheduleEntry(self.emp2, 'MO', self.b_turn)
        self.entry4 = self.en.ScheduleEntry(self.emp3, 'MO', self.c_turn)
        self.sched_string1 = 'TU10:30-11:45,TH01:30-02:00,SU21:30-23:59'
        self.sched_string2 = 'MO9:30-10:00,TH05:30-06:00,SU21:30-23:59'
        self.expected_list1 = [('TU', 10, 30, 11, 45),('TH', 1,30,2,0),
                               ('SU',21,30,23,59)]
        self.expected_list2 = [('MO', 9, 30, 10, 0),('TH', 5,30,6,0),
                               ('SU',21,30,23,59)]
        self.expected_dict1 = {'MO':[self.entry1, self.entry3, self.entry4],
                               'TU':[self.entry2],
                               'WE':[], 'TH':[],
                               'FR':[], 'SA':[],
                               'SU':[]}

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

    def test_is_overlap(self):
        """ Tests the Turn.is_overlap method """
        self.assertFalse(self.a_turn.is_overlap(self.b_turn))
        self.assertTrue(self.a_turn.is_overlap(self.c_turn))
        self.assertTrue(self.a_turn.is_overlap(self.d_turn))
        self.assertFalse(self.a_turn.is_overlap(self.e_turn))

    def test_is_encounter(self):
        """ Tests the ScheduleEntry.is_encounter method"""
        self.assertFalse(self.entry1.is_encounter(self.entry2))
        self.assertFalse(self.entry1.is_encounter(self.entry3))
        self.assertTrue(self.entry1.is_encounter(self.entry4))

    def test_parse_schedule_string(self):
        """ Tests the EmployeeeEncounterParser.test_parse_schedule_string method
        """
        parser = self.en.EmployeeEncountersParser('dummy_file.txt')
        self.assertListEqual(self.expected_list1,
                             parser._parse_schedule_string(self.sched_string1))
        self.assertListEqual(self.expected_list2,
                             parser._parse_schedule_string(self.sched_string2))

    def test_parse_input_file(self):
        """ Tests the EmployeeeEncounterParser.test_parse_input_file """
        parser1 = self.en.EmployeeEncountersParser('dummy_input1.txt')
        parser1._parse_input_file()
        # parser2 = self.en.EmployeeEncountersParser('dummy_input2.txt')
        for key,elist in parser1.entry_dict.items(): 
            for e in elist:
                # if key=='MO' and e.emp.name=='CHARLES':
                #     print(e.emp.name)
                print(e)
        print('#####################################')
        for key,elist in self.expected_dict1.items(): 
            for e in elist:
                print(e)
        self.assertDictEqual(self.expected_dict1, parser1.entry_dict)

    def test_generate_table(self):
        """ """
        pass


if __name__ == '__main__':
    unittest.main()
