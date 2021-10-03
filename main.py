from functools import cmp_to_key

PROJECTS_STUDENTS_MAP = {};
STUDENTS_PREFERRED_PROJECT_MAP = {};

class Project(object):
    def __init__(self, id, seats, minimum_grade):
        self.id = id
        self.seats = seats
        self.minimum_grade = minimum_grade

class Student(object):
    def __init__(self, id, grade):
        self.id = id
        self.grade = grade

# le o arquivo e cria os estudantes e projetos em memoria
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
            PROJECTS_STUDENTS_MAP[project] = []

        # Create students
        if STUDENTS_START_LINE <= count and count <= STUDENTS_END_LINE:
            student_data = line.strip().split()
            student = Student(student_data[0], student_data[4])
            student_projects_ids = [student_data[1], student_data[2], student_data[3]]
            STUDENTS_PREFERRED_PROJECT_MAP[student] = []

            for student_project_id in student_projects_ids:
                matches = (project for project in PROJECTS_STUDENTS_MAP.keys() if project.id == student_project_id)
                project = next(matches)
                STUDENTS_PREFERRED_PROJECT_MAP[student] = STUDENTS_PREFERRED_PROJECT_MAP[student] + [project]

        count += 1

# usado para ordenar a lista de estudantes
def student_key(item):
    return int(item.grade)

# busca todos os alunos que já tem um projeto definido
def all_project_students():
    students = []
    for project in PROJECTS_STUDENTS_MAP.keys():
        students = students + PROJECTS_STUDENTS_MAP[project]

    return students

# remove o estudante e remove o projeto ta lista de projetos que estão disponiveis
def remove_student(students_to_remove, project):
    # remove o projeto da lista de projetos para propor
    for student in students_to_remove:
        new_projects = []
        first_removed = False
        for project_to_validate in STUDENTS_PREFERRED_PROJECT_MAP[student]:
            if project_to_validate == project and first_removed == False:
                first_removed = True
            else:
                new_projects = new_projects + [project_to_validate]

        STUDENTS_PREFERRED_PROJECT_MAP[student] = new_projects

# execução do algoritmo
def run():
    students_waitlist = []
    students_without_project = []
    count = 0

    while len(students_waitlist) < len(STUDENTS_PREFERRED_PROJECT_MAP.keys()):
        print('--------------------------------------')
        print(f'---- INICIO DA ITERAÇÃ0 {count} (PROJETO: LISTA DE ALUNOS): ----')

        print_all()

        for student in STUDENTS_PREFERRED_PROJECT_MAP.keys():
            if student not in students_waitlist:
                if len(STUDENTS_PREFERRED_PROJECT_MAP[student]) == 0:
                    students_without_project = students_without_project + [student]
                    continue

                project = STUDENTS_PREFERRED_PROJECT_MAP[student][0]
                PROJECTS_STUDENTS_MAP[project] = PROJECTS_STUDENTS_MAP[project] + [student]

        # remove os alunos que não tem nota para o projeto
        for project in PROJECTS_STUDENTS_MAP.keys():
            list_of_students = PROJECTS_STUDENTS_MAP[project]
            fitered_students = list(filter(lambda s: project.minimum_grade <= s.grade, PROJECTS_STUDENTS_MAP[project]))
            PROJECTS_STUDENTS_MAP[project] = sorted(fitered_students, key=student_key)
            remove_student(list(set(list_of_students) - set(fitered_students)), project)

        projects_with_more_student = list(filter(lambda p: int(p.seats) < len(PROJECTS_STUDENTS_MAP[p]), PROJECTS_STUDENTS_MAP.keys()))

        # remove os alunos excedentes do projeto
        for project in projects_with_more_student:
            students_to_remove = []
            new_students_list = PROJECTS_STUDENTS_MAP[project]
            for i in range(len(PROJECTS_STUDENTS_MAP[project]) - int(project.seats)):
                students_to_remove = students_to_remove + [new_students_list.pop(0)]
            PROJECTS_STUDENTS_MAP[project] = new_students_list
            remove_student(students_to_remove, project)

        students_waitlist = students_without_project + all_project_students()

        print(f'---- RESUTADO DA ITERAÇÃ0 {count} (PROJETO: LISTA DE ALUNOS): ----')
        print_all()

        count += 1


# retorna a lista de ids dos estudantes
def list_students(students):
    if len(students) == 0:
        return []

    students_ids = []
    for student in students:
        students_ids.append(student.id)

    return students_ids

def print_all():
    for key in PROJECTS_STUDENTS_MAP.keys():
        print(f"{key.id} : {list_students(PROJECTS_STUDENTS_MAP[key])}")

def main():
    read_file_and_create_sets()
    run()
    print('|')
    print(f'---- ITERAÇÃ0 FINAL (PROJETO: LISTA DE ALUNOS) ----')
    print('|')
    print_all()

main()
