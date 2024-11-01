import json


# Person class
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}, Age: {self.age}, Address: {self.address}")


# Student class, inheriting from Person
class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def enroll_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def display_student_info(self):
        self.display_person_info()
        print(f"ID: {self.student_id}")
        print("Courses Enrolled:", ", ".join(self.courses))
        print("Grades:", self.grades)


# Course class
class Course:
    def __init__(self, course_name, course_code, instructor):
        self.course_name = course_name
        self.course_code = course_code
        self.instructor = instructor
        self.students = []

    def add_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def display_course_info(self):
        print(f"Course Name: {self.course_name}, Code: {self.course_code}, Instructor: {self.instructor}")
        print("Enrolled Students:", ", ".join([student.name for student in self.students]))


# Functions for system
students = {}
courses = {}


def add_student():
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    address = input("Enter Address: ")
    student_id = input("Enter Student ID: ")
    students[student_id] = Student(name, age, address, student_id)
    print(f"Student {name} (ID: {student_id}) added successfully.")


def add_course():
    course_name = input("Enter Course Name: ")
    course_code = input("Enter Course Code: ")
    instructor = input("Enter Instructor Name: ")
    courses[course_code] = Course(course_name, course_code, instructor)
    print(f"Course {course_name} (Code: {course_code}) created with instructor {instructor}.")


def enroll_student_in_course():
    student_id = input("Enter Student ID: ")
    course_code = input("Enter Course Code: ")

    if student_id in students and course_code in courses:
        student = students[student_id]
        course = courses[course_code]
        student.enroll_course(course.course_name)
        course.add_student(student)
        print(f"Student {student.name} (ID: {student_id}) enrolled in {course.course_name} (Code: {course_code}).")
    else:
        print("Invalid student ID or course code.")


def add_grade():
    student_id = input("Enter Student ID: ")
    course_code = input("Enter Course Code: ")
    grade = input("Enter Grade: ")

    if student_id in students and course_code in courses:
        student = students[student_id]
        course = courses[course_code]
        if course.course_name in student.courses:
            student.add_grade(course.course_name, grade)
            print(f"Grade {grade} added for {student.name} in {course.course_name}.")
        else:
            print("Student is not enrolled in this course.")
    else:
        print("Invalid student ID or course code.")


def display_student_details():
    student_id = input("Enter Student ID: ")
    if student_id in students:
        students[student_id].display_student_info()
    else:
        print("Student not found.")


def display_course_details():
    course_code = input("Enter Course Code: ")
    if course_code in courses:
        courses[course_code].display_course_info()
    else:
        print("Course not found.")


def save_data():
    data = {
        "students": [
            {"name": student.name, "age": student.age, "address": student.address,
             "student_id": student.student_id, "grades": student.grades, "courses": student.courses}
            for student in students.values()
        ],
        "courses": [
            {"course_name": course.course_name, "course_code": course.course_code,
             "instructor": course.instructor, "students": [s.student_id for s in course.students]}
            for course in courses.values()
        ]
    }
    with open('student_management_data.json', 'w') as file:
        json.dump(data, file)
    print("Data saved successfully.")


def load_data():
    global students, courses
    try:
        with open('student_management_data.json', 'r') as file:
            data = json.load(file)
        students = {s['student_id']: Student(s['name'], s['age'], s['address'], s['student_id']) for s in
                    data['students']}
        courses = {c['course_code']: Course(c['course_name'], c['course_code'], c['instructor']) for c in
                   data['courses']}

        # Rebuild relationships
        for s_data in data['students']:
            student = students[s_data['student_id']]
            student.grades = s_data['grades']
            student.courses = s_data['courses']
        for c_data in data['courses']:
            course = courses[c_data['course_code']]
            course.students = [students[s_id] for s_id in c_data['students'] if s_id in students]
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("No saved data found.")


# Main menu for the system
def main():
    while True:
        print("\n==== Student Management System ====")
        print("1. Add New Student")
        print("2. Add New Course")
        print("3. Enroll Student in Course")
        print("4. Add Grade for Student")
        print("5. Display Student Details")
        print("6. Display Course Details")
        print("7. Save Data to File")
        print("8. Load Data from File")
        print("0. Exit")
        choice = input("Select Option: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            add_course()
        elif choice == '3':
            enroll_student_in_course()
        elif choice == '4':
            add_grade()
        elif choice == '5':
            display_student_details()
        elif choice == '6':
            display_course_details()
        elif choice == '7':
            save_data()
        elif choice == '8':
            load_data()
        elif choice == '0':
            print("Exiting Student Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


# Run the program
if __name__ == "__main__":
    main()
