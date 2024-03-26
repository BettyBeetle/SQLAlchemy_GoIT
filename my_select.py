from sqlalchemy import func, desc

from models import Student, Grade, Subject, Lecturer, StudentGroup
from connect_db import session



# Query 1: Top 5 students with highest average grades.
def select_1():
    top_students = session.query(Student.student_name, func.avg(Grade.grade).label('avg_grade')) \
        .join(Grade) \
        .group_by(Student.student_name) \
        .order_by(func.avg(Grade.grade).desc()) \
        .limit(5) \
        .all()

    return top_students


# Query 2: Student with the highest average grades for subject.
def select_2(subject_id):
    top_student = session.query(Student.student_name, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade, Student.student_id == Grade.student_id) \
        .filter(Grade.subject_id == subject_id) \
        .group_by(Student.student_name) \
        .order_by(func.avg(Grade.grade).desc()) \
        .first()
    return top_student


# Query_3: Average grades for groups with specific subject
def select_3(subject_id):
    average_grades_by_group = session.query(StudentGroup.group_name,
                                            func.avg(Grade.grade).label('average_grade')) \
        .join(Subject, Subject.group_id == StudentGroup.group_id) \
        .join(Grade, Grade.subject_id == Subject.subject_id) \
        .filter(Subject.subject_id == subject_id) \
        .group_by(StudentGroup.group_name) \
        .all()
    return average_grades_by_group


# Query 4: Average grades for groups
def select_4():
    avg_grades_for_groups = session.query(StudentGroup.group_name,
                                             func.avg(Grade.grade).label('average_grade')) \
        .join(Subject, Subject.group_id == StudentGroup.group_id) \
        .join(Grade, Grade.subject_id == Subject.subject_id) \
        .group_by(StudentGroup.group_name) \
        .all()
    return avg_grades_for_groups


# Query 5: Subjects of specific lecturer
def select_5(lecturer_id):
    lecturer_subjects = session.query(Subject.subject_name) \
        .join(Lecturer, Subject.lecturer_id == Lecturer.lecturer_id) \
        .filter(Lecturer.lecturer_id == lecturer_id) \
        .all()
    return lecturer_subjects


# Query 6: List of students of specific group:")
def select_6(student_group_id):
    list_of_students = session.query(Student.student_name) \
        .filter(Student.student_group_id == student_group_id) \
        .all()
    return list_of_students

# Query 7: Students grades of specific group with specific subject")
def select_7(student_group_id, subject_id):
    grades_in_group = session.query(Student.student_name, Grade.grade) \
                            .join(Grade, Student.student_id == Grade.student_id) \
                            .filter(Student.student_group_id == student_group_id, Grade.subject_id == subject_id).all()
    return grades_in_group

# Query 8: Average grade given by specific lecturer in specific subject
def select_8(lecturer_id, subject_id):
    avg_grade_by_lecturer = session.query(func.avg(Grade.grade).label('average_grade')) \
                                    .join(Subject, Subject.subject_id == Grade.subject_id) \
                                    .filter(Subject.lecturer_id == lecturer_id, Subject.subject_id == subject_id) \
                                    .first()
    return avg_grade_by_lecturer


# Query 9: Passed subjects for specific student
# Courses attended by the specific student
def select_9(student_id, passing_grade):
    passed_subjects = [subject[0] for subject in session.query(Subject.subject_name)
                    .join(Grade, Subject.subject_id == Grade.subject_id)
                    .filter(Grade.student_id == student_id, Grade.grade >= passing_grade)
                    .distinct()
                    .all()]

    all_subjects = [subject[0] for subject in session.query(Subject.subject_name)
                    .distinct()
                    .all()]
    return passed_subjects, all_subjects


def select_10(lecturer_id, student_id):
    courses = session.query(Subject.subject_name) \
        .join(Lecturer, Subject.lecturer_id == Lecturer.lecturer_id) \
        .join(Grade, Subject.subject_id == Grade.subject_id) \
        .filter(Lecturer.lecturer_id == lecturer_id, Grade.student_id == student_id) \
        .distinct() \
        .all()

    return courses

# def find_lecturer_name_by_id(lecturer_id):
#     lecturer_name = session.query(Lecturer.lecturer_name).filter(Lecturer.lecturer_id == lecturer_id).scalar()
#     return lecturer_name



if __name__ == "__main__":
    # Query 1
    top_students = select_1()
    if top_students:
        print(f"\nQuery_1: Top 5 students with highest average grades:")
        for student in top_students:
            print(f"Student Name: {student[0]}, Average Grade: {student[1]:.2f}")
    else:
        print("No data found.")

    # Query 2
    subject_id = 1  # Identyfikator przedmiotu, dla którego chcemy znaleźć najlepszego studenta
    top_student = select_2(subject_id)
    if top_student:
        print(f"\nQuery_2: Student with the highest average grades for subject with ID {subject_id}:")
        print(f"Student Name: {top_student[0]}, Average Grade: {top_student[1]:.2f}")
    else:
        print("No data found for the specified subject ID.")

    # Query 3
    subject_id = 1  # Zmień na właściwy identyfikator przedmiotu
    average_grades_by_group = select_3(subject_id)
    print(f"\nQuery_3: Average grades by group for subject with ID {subject_id}:")
    for group_id, average_grade in average_grades_by_group:
        print(f"Group Name: {group_id}, Average Grade: {average_grade:.2f}")

   # Query 4
    print(f"\nQuery_4: Average grades for groups: ")
    for group_name, average_grade in select_4():
        print(f"Group Name: {group_name}, Average Grade: {average_grade:.2f}")

    # Query 5
    lecturer_id= 1
    print(f"\nQuery_5:Subjects of lecturer with ID {lecturer_id}: ")
    for row in select_5(lecturer_id):
        print(f"Subject: {row.subject_name}")


    # Query 6:
    student_group_id= 1
    print(f"\nQuery_6: List of students of group with ID: {student_group_id}")
    for row in select_6(student_group_id):
        print(f"Student: {row.student_name}")


    # Query 7:
    student_group_id= 1
    subject_id= 1
    print(f"\nQuery_7: Students grades of group with ID {student_group_id} with subject with ID {subject_id}: ")
    for student_name, grade in select_7(student_group_id, subject_id):
        print(f"Student Name: {student_name}, Grades: {grade}")

    # Query 8:
    lecturer_id = 1
    subject_id = 1
    average_grade = select_8(lecturer_id, subject_id)
    print(f"\nQuery_8: Average grade given by lecturer with ID {lecturer_id} in subject with ID {subject_id}: {average_grade}")

    # Query_9:
    student_id = 1  # Identyfikator studenta, dla którego chcemy znaleźć zaliczone przedmioty
    passing_grade = 3.0  # Minimalna ocena wymagana do zaliczenia przedmiotu

    passed_subjects, all_subjects = select_9(student_id, passing_grade)

    print(f"\nQuery_9: Passed subjects for student with ID {student_id}:")
    for subject_id in passed_subjects:
       print(f"Passed subject: {subject_id}")

    print(f"\nAll subjects participated by the student with ID {student_id}:")
    for subject in all_subjects:
       print(f"Subject: {subject}")


    # Query_10
    lecturer_id = 1  # Identyfikator wykładowcy
    student_id = 1  # Identyfikator studenta

    courses = select_10(lecturer_id, student_id)
    # lecturer_name = find_lecturer_name_by_id(lecturer_id)

    if courses:
       print(f"\nQuery_10:Courses led by a lecturer with ID {lecturer_id} for student with o ID {student_id}:")
       for course in courses:
           print(f"Subject: {course[0]}")
