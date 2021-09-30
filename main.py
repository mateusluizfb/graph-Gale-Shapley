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
                MAP_OF_PROJECTS[project] = MAP_OF_PROJECTS[project] + [student]
                MAP_OF_STUDENTS[student] = MAP_OF_STUDENTS[student] + [project]

        count += 1



def main():
    read_file_and_create_sets()


main()
# project = find_project_by_id('P1')
# print(project)
# print(len(MAP_OF_PROJECTS[project]))
# for student in MAP_OF_PROJECTS[project]:
#     print(student.id)
#     for value in MAP_OF_STUDENTS[student]:
#         if value.id == 'P1':
#             print(value.id)
