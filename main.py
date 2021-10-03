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

def all_project_students():
    students = []
    for project in MAP_OF_PROJECTS.keys():
        students = students + MAP_OF_PROJECTS[project]

    return students
    
def run():

    students_waitlist = []
    students_without_project = []

    while len(students_waitlist) < len(MAP_OF_STUDENTS.keys()):
        for student in MAP_OF_STUDENTS.keys():
            if student not in students_waitlist:
                if len(MAP_OF_STUDENTS[student]) == 0:
                    students_without_project = students_without_project + [student]
                    continue

                project = MAP_OF_STUDENTS[student][0]
                MAP_OF_PROJECTS[project] = MAP_OF_PROJECTS[project] + [student]

        projects_with_more_student = list(filter(lambda p: int(p.seats) < len(MAP_OF_PROJECTS[p]), MAP_OF_PROJECTS.keys()))

        for project in projects_with_more_student:
            # escolhe so os melhores pro projeto
            MAP_OF_PROJECTS[project] = sorted(MAP_OF_PROJECTS[project], key=student_key)
            MAP_OF_PROJECTS[project] = list(filter(lambda s: project.minimum_grade <= s.grade, MAP_OF_PROJECTS[project]))

            new_students_list = MAP_OF_PROJECTS[project]
            students_to_remove = []
            for i in range(len(MAP_OF_PROJECTS[project]) - int(project.seats)):
                students_to_remove = students_to_remove + [new_students_list.pop()]
            MAP_OF_PROJECTS[project] = new_students_list

            # remove o projeto da lista de projetos para propor
            for student in students_to_remove:
                new_projects = []
                first_removed = False
                for project_to_validate in MAP_OF_STUDENTS[student]:
                    if project_to_validate == project and first_removed == False:
                        first_removed = True
                    else:
                        new_projects = new_projects + [project_to_validate]

                MAP_OF_STUDENTS[student] = new_projects

        students_waitlist = students_without_project + all_project_students()


def print_students(students):
    if len(students) == 0:
        return []

    students_ids = []
    for student in students:
        students_ids.append(student.id)

    return students_ids

def print_projects(projects):
    if len(projects) == 0:
        return []

    project_ids = []
    for project in projects:
        project_ids.append(project.id)

    return project_ids

def print_all():
    for key in MAP_OF_PROJECTS.keys():
        print(f"{key.id} : {print_students(MAP_OF_PROJECTS[key])}")

def main():
    read_file_and_create_sets()
    run()
    print_all()

main()
# project = find_project_by_id('P1')
# print(project)
# print(len(MAP_OF_PROJECTS[project]))
# for student in MAP_OF_PROJECTS[project]:
#     print(student.id)
#     for value in MAP_OF_STUDENTS[student]:
#         if value.id == 'P1':
#             print(value.id)
