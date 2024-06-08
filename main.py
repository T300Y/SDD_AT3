def initialize_domains(rooms, subjects, time_slots, teacher_availability, student_subjects):
    # Initialize domains for each variable (time slot)
    domains = {}
    for slot in time_slots:
        domains[slot] = []
        for room in rooms:
            for teacher in get_available_teachers(slot, teacher_availability):
                students = get_students_for_subject(slot[1], student_subjects)
                if len(students) <= room[1]:
                    domains[slot].append({'room': room[0], 'teacher': teacher, 'students': students})
    return domains

def ac3(domains):
    """Maintains arc consistency on domains using AC-3"""
    arc_queue = [(slot1, slot2) for slot1 in domains for slot2 in domains if slot1 != slot2] # Creates a queue of all arcs needing processing
    while arc_queue:
        # Pops first arc from queue
        slot1, slot2 = arc_queue.pop(0)
        # Revises domain of slot1 to ensure consistency with slot2
        if revise(slot1, slot2, domains):
            if not domains[slot1]:
                return False
            # Adds all arcs back to the queue to recheck consistency
            for slot3 in (domains.keys() - {slot2}):
                arc_queue.append((slot3, slot1))
    return True

def revise(slot1, slot2, domains):
    """Will revise the domains of slot1 to ensure arc consistency with slot2"""
    revised = False
    for value1 in domains[slot1][:]:  # Create a copy of the domain list to avoid modifying it during iteration
        # Check if there's no value in slot2 that is consistent with value1
        if not any(is_consistent(value1, value2) for value2 in domains[slot2]):
            print("test1")
            # Remove value1 from the domain of slot1 as it is inconsistent
            domains[slot1].remove(value1)
            revised = True
    return revised
    
def is_consistent(value1, value2):
    # Check if two assignments are consistent
    return not (value1['teacher'] == value2['teacher'] or value1['room'] == value2['room'])

def get_available_teachers(slot, teacher_availability):
    return [teacher for teacher, available_slot in teacher_availability if available_slot == slot]

def get_students_for_subject(subject, student_subjects):
    return [student for student, student_subject in student_subjects if student_subject == subject]
    
def validate(schedule, rooms, teacher_availability):
    """Ensures the current timetable adheres to all constraints"""
    return (validate_room_capacity(schedule, rooms) and
            validate_teacher_availability(schedule, teacher_availability) and
            validate_student_schedule(schedule))
    
def validate_room_capacity(schedule, rooms):
    for slot, details in schedule.items():
        room = details['room']
        num_students = len(details['students'])
        room_capacity = next(r[1] for r in rooms if r[0] == room)
        if num_students > room_capacity:
            return False
    return True
    
def validate_teacher_availability(schedule, teacher_availability):
    for slot, details in schedule.items():
        teacher = details['teacher']
        slot_time = slot[0]  # Extract the time slot part
        if (teacher, slot_time) not in teacher_availability:
            return False
    return True
    
def validate_student_schedule(schedule):
    student_schedule = {student: [] for student in set(sum((details['students'] for details in schedule.values()), []))}
    for slot, details in schedule.items():
        for student in details['students']:
            if slot in student_schedule[student]:
                return False
            student_schedule[student].append(slot)
    return True

def generate_timetable(domains, time_slots, rooms, teacher_availability):
    '''Generates a valid timetable using constraint satisfaction algo AC-3'''
    # Apply AC-3 algorithm to enforce arc consistency
    if not ac3(domains):
        raise Exception("No valid timetable found after applying AC-3")
    schedule = {}
    # Start backtracking#
    if helper(schedule, domains, time_slots, rooms, teacher_availability, 0):
        return schedule
    else:
        raise Exception("No valid timetable found")
def helper(schedule, domains, time_slots, rooms, teacher_availability, slot_index):
    """Recursive backtracking algorithm"""
    # Base case 
    if slot_index >= len(time_slots):
        return True

    # Get the current time slot to be assigned
    current_slot = time_slots[slot_index]

    # Try each possible assignment 
    for assignment in domains[current_slot]:
        schedule[current_slot] = assignment

        # Validate Schedule
        if validate(schedule, rooms, teacher_availability):
            if helper(schedule, domains, time_slots, rooms, teacher_availability, slot_index + 1):
                return True
        del schedule[current_slot]
    
    return False