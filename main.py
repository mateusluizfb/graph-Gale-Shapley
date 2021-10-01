from functools import cmp_to_key

MAP_OF_PROJECTS = {};
MAP_OF_STUDENTS = {};

class Project(object):

    def __init__(self, id, seats, minimum_grade):
        self.id = id
        self.seats = seats
        self.minimum_grade = minimum_grade

class Student(object):

    def __init__(self, id, grade):
        self.id = id
        self.grade = grade

def find_project_by_id(id):
    matches = (project for project in MAP_OF_PROJECTS.keys() if project.id == id)
    return next(matches)

def find_student_by_id(id):
    matches = (student for student in MAP_OF_STUDENTS.keys() if student.id == id)
    return next(matches)

def read_file_and_create_sets():
    data_file = open('entradaProj2TAG.txt', 'r')
    Lines = data_file.readlines()

    count = 0
    PROJECTS_START_LINE = 0
    PROJECTS_END_LINE = 49

    STUDENTS_START_LINE = 51
    STUDENTS_END_LINE = 250

    for line in Lines:
        # Create projects
        if PROJECTS_START_LINE <= count and count <= PROJECTS_END_LINE:
            project_data = line.strip().split()
            project = Project(project_data[0], project_data[1], project_data[2])
            MAP_OF_PROJECTS[project] = []

        # Create students
        if STUDENTS_START_LINE <= count and count <= STUDENTS_END_LINE:
            student_data = line.strip().split()
            student = Student(student_data[0], student_data[4])
            student_projects_ids = [student_data[1], student_data[2], student_data[3]]
            MAP_OF_STUDENTS[student] = []

            for student_project_id in student_projects_ids:
                matches = (project for project in MAP_OF_PROJECTS.keys() if project.id == student_project_id)
                project = next(matches)
                MAP_OF_STUDENTS[student] = MAP_OF_STUDENTS[student] + [project]

        count += 1

def student_key(item):
    return int(item.grade)

def addStudent(student, project):
    removed_student = MAP_OF_PROJECTS[project][-1]
    MAP_OF_PROJECTS[project] = MAP_OF_PROJECTS[project][:-1]
    MAP_OF_PROJECTS[project] = MAP_OF_PROJECTS[project] + [student]
    MAP_OF_PROJECTS[project] = sorted(MAP_OF_PROJECTS[project], key=student_key)
    return removed_student

def studentMoreSuitable(student, project):
    # if student had a better grade than everyone else returns true
    # if not, returns false
    return False

def run():
    students_available = MAP_OF_STUDENTS.keys()
    projects_available = MAP_OF_STUDENTS

    while len(students_available) != 0:
        for student in MAP_OF_STUDENTS.keys():
            project = MAP_OF_STUDENTS[student][0]

            if len(MAP_OF_PROJECTS[project]) == 0:
                if project.minimum_grade <= student.grade:
                    MAP_OF_PROJECTS[project] = [student]
                    students_available = list(filter(lambda s: s == student, students_available))
            else:
                if studentMoreSuitable(student, project):
                    removed_student = addStudent(student, project)
                    students_available = list(filter(lambda s: s == student, students_available)) + [removed_student]
                else:
                    print('nop')

            MAP_OF_STUDENTS[student] = list(filter(lambda p: p == project, MAP_OF_STUDENTS[student]))


def print_students(students):
    if len(students) == 0:
        return []

    students_ids = []
    for student in students:
        students_ids.append(student.id)

    return students_ids


def main():
    read_file_and_create_sets()
    run()

    for key in MAP_OF_PROJECTS.keys():
        print(f"{key.id} : {print_students(MAP_OF_PROJECTS[key])}")


main()
# project = find_project_by_id('P1')
# print(project)
# print(len(MAP_OF_PROJECTS[project]))
# for student in MAP_OF_PROJECTS[project]:
#     print(student.id)
#     for value in MAP_OF_STUDENTS[student]:
#         if value.id == 'P1':
#             print(value.id)
