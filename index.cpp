//
//
// Mateus Luiz Freitas Barros - 150140801
//
//

#include <vector>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <algorithm>
#include <sstream>
#include <list>

class Project {
    public:

    std::string id;
    int seats;
    int minimum_grade;

    void print(){
      printf("DATA: \n");
      printf("%s ", &id);
      printf("%d ", seats);
      printf("%d\n", minimum_grade);
    }
};

class Student {
    public:

    std::string id;
    int grade;
    std::vector<Project> projects;

    void print(){
      printf("%s ", &id);
      printf("%d\n", grade);
    }
};

std::vector<Project> LIST_OF_PROJECTS;
std::vector<Student> LIST_OF_STUDENTS;

// Create a list of projects instances
void create_projects(char const argv[]) {
  std::ifstream data_file(argv);

  int PROJECTS_START_LINE = 2;
  int PROJECTS_END_LINE = 52;

  int current_line = 0;
  std::string line;

  while(getline(data_file, line)) {
    if(current_line <= PROJECTS_START_LINE || PROJECTS_END_LINE <= current_line ){
      current_line++;
      continue;
    }

    std::string project = line.c_str();
    project.erase(std::remove(project.begin(), project.end(), ','), project.end());
    project.erase(std::remove(project.begin(), project.end(), '('), project.end());
    project.erase(std::remove(project.begin(), project.end(), ')'), project.end());

    std::string buf;
    std::stringstream ss(project);
    std::vector<std::string> tokens;

    while (ss >> buf)
      tokens.push_back(buf);

    Project project_instance;
    project_instance.id = tokens[0].c_str();
    project_instance.seats = std::stoi(tokens[1].c_str());
    project_instance.minimum_grade = std::stoi(tokens[2].c_str());

    LIST_OF_PROJECTS.push_back(project_instance);

    current_line++;
  }
}

void create_students(char const argv[]) {
  std::ifstream data_file(argv);

  int STUDENTS_START_LINE = 56;

  int current_line = 0;
  std::string line;

  while(getline(data_file, line)) {
    if(current_line < STUDENTS_START_LINE){
      current_line++;
      continue;
    }

    std::string student = line.c_str();
    student.erase(std::remove(student.begin(), student.end(), ','), student.end());
    student.erase(std::remove(student.begin(), student.end(), '('), student.end());
    student.erase(std::remove(student.begin(), student.end(), ')'), student.end());
    std::replace(student.begin(), student.end(), ':', ' ');


    std::string buf;
    std::stringstream ss(student);
    std::vector<std::string> tokens;

    while (ss >> buf)
      tokens.push_back(buf);

    Student student_instance;
    student_instance.id = tokens[0].c_str();
    // Find project and add here
    // student_instance.projects.push_back(tokens[1]);
    // student_instance.projects.push_back(tokens[1]);
    student_instance.grade = std::stoi(tokens[4].c_str());

    // LIST_OF_STUDENTS.push_back(student_instance);

    current_line++;
  }
}

int main(int argc, char const *argv[]) {
  std::map< int, std::set<int> > graph;

  int state = 0;
  create_projects(argv[1]);
  create_students(argv[1]);

  return 0;
}
