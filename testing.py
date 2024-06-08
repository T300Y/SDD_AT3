import unittest
from main import initialize_domains, ac3, revise, is_consistent, validate, validate_room_capacity, validate_teacher_availability, validate_student_schedule, generate_timetable

def setUpTestData():
    rooms = [('Room1', 30), ('Room2', 20)]
    subjects = ['Math', 'Science']
    time_slots = [('Monday 9AM', 'Math'), ('Monday 10AM', 'Science')]
    teacher_availability = [('Teacher1', 'Monday 9AM'), ('Teacher2', 'Monday 10AM')]
    student_subjects = [('Student1', 'Math'), ('Student2', 'Science')]
    domains = initialize_domains(rooms, subjects, time_slots, teacher_availability, student_subjects)
    return rooms, subjects, time_slots, teacher_availability, student_subjects, domains

class TestFunctions(unittest.TestCase):

    def setUp(self):
        self.rooms, self.subjects, self.time_slots, self.teacher_availability, self.student_subjects, self.domains = setUpTestData()

    def test_initialize_domains(self):
        self.assertTrue(len(self.domains) > 0)
        self.assertIn(('Monday 9AM', 'Math'), self.domains)
        self.assertIn(('Monday 10AM', 'Science'), self.domains)

    def test_ac3(self):
        self.assertTrue(ac3(self.domains))

    def test_revise(self):
        slot1 = ('Monday 9AM', 'Math')
        slot2 = ('Monday 10AM', 'Science')
        self.assertFalse(revise(slot1, slot2, self.domains))

    def test_is_consistent(self):
        value1 = {'room': 'Room1', 'teacher': 'Teacher1', 'students': ['Student1']}
        value2 = {'room': 'Room2', 'teacher': 'Teacher2', 'students': ['Student2']}
        self.assertTrue(is_consistent(value1, value2))

    def test_validate(self):
        schedule = {
            ('Monday 9AM', 'Math'): {'room': 'Room1', 'teacher': 'Teacher1', 'students': ['Student1']},
            ('Monday 10AM', 'Science'): {'room': 'Room2', 'teacher': 'Teacher2', 'students': ['Student2']}
        }
        self.assertTrue(validate(schedule, self.rooms, self.teacher_availability))

    def testvalidate_room_capacity(self):
        schedule = {
            ('Monday 9AM', 'Math'): {'room': 'Room1', 'teacher': 'Teacher1', 'students': ['Student1']}
        }
        self.assertTrue(validate_room_capacity(schedule, self.rooms))

    def testvalidate_teacher_availability(self):
        schedule = {
            ('Monday 9AM', 'Math'): {'room': 'Room1', 'teacher': 'Teacher1', 'students': ['Student1']}
        }
        self.assertTrue(validate_teacher_availability(schedule, self.teacher_availability))

    def testvalidate_student_schedule(self):
        schedule = {
            ('Monday 9AM', 'Math'): {'room': 'Room1', 'teacher': 'Teacher1', 'students': ['Student1']}
        }
        self.assertTrue(validate_student_schedule(schedule))

class TestTimetableGeneration(unittest.TestCase):

    def setUp(self):
        self.rooms, self.subjects, self.time_slots, self.teacher_availability, self.student_subjects, self.domains = setUpTestData()

    def test_generate_timetable(self):
        schedule = generate_timetable(self.domains, self.time_slots, self.rooms, self.teacher_availability)
        self.assertTrue(len(schedule) > 0)
        for slot, details in schedule.items():
            self.assertIn('room', details)
            self.assertIn('teacher', details)
            self.assertIn('students', details)

    def test_generate_timetable_no_solution(self):
        # Modify constraints to make it impossible to find a valid timetable
        self.teacher_availability = [('Teacher1', 'Monday 9AM')]
        self.domains = initialize_domains(self.rooms, self.subjects, self.time_slots, self.teacher_availability, self.student_subjects)
        with self.assertRaises(Exception) as context:
            generate_timetable(self.domains, self.time_slots, self.rooms, self.teacher_availability)
        self.assertTrue('No valid timetable found' in str(context.exception))

if __name__ == '__main__':
    unittest.main()