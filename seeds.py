from datetime import datetime
import faker
import random
from connect_db import session
from models import Student, Lecturer, StudentGroup, Subject, Grade

NUMBER_STUDENTS = 50
NUMBER_LECTURERS = 5
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 8
NUMBER_GRADES = 20

def generate_fake_data(number_students, number_lecturers, number_groups, number_subjects, number_grades):
    fake_students = []
    fake_lecturers = []
    fake_groups = []
    fake_subjects = []
    fake_data_for_grades = []

    fake_data = faker.Faker()

    for _ in range(random.randint(30, number_students + 1)):
        fake_students.append(fake_data.name())
        fake_groups.append(random.randint(1, number_groups))

    for _ in range(3, number_lecturers + 1):
        fake_lecturers.append(fake_data.name())

    for _ in range(random.randint(5, number_subjects + 1)):
        fake_subjects.append(
            (
                fake_data.catch_phrase(),  # generuje od 5 do NUMBER_SUBJECTS losowych przedmiotów
                random.choice(fake_lecturers),  # wybiera losowego wykładowcę z fake_lecturers
            )
        )

    for student_id in range(1, len(fake_students) + 1):

        student_subjects = set()
        for _ in range(random.randint(15, 20)):  # generuje od 15 do 20 ocen dla każdego studenta
            fake_grades = []
            for subject in fake_subjects:
                subject_name = subject[0]

                if subject_name not in student_subjects:
                    student_subjects.add(subject_name)
                    fake_grades.append(float(fake_data.random_int(2, 5)))
                    grade_date = datetime(2023, 10,
                                          random.randint(1, 31)).date()  # generuje loswą datę z października 2023
                    fake_data_for_grades.append(  # przekazuje informacje związane z oceną
                        (
                            student_id,
                            fake_grades[-1],
                            grade_date,
                            subject_name,
                        )
                    )

    return (
        fake_students,
        fake_lecturers,
        fake_groups,
        fake_subjects,
        fake_data_for_grades,
    )


def insert_data_to_db(students, lecturers, student_group, subjects, grades):
    # Dodajemy grupy studenckie, ale tylko jeśli nie istnieją jeszcze w bazie danych
    existing_groups = session.query(StudentGroup.group_id).all()
    existing_group_ids = [group.group_id for group in existing_groups]

    for group_id in set(student_group):
        if group_id not in existing_group_ids:
            group = StudentGroup(group_id=group_id, group_name=f"Group {group_id}")
            session.add(group)
    session.commit()

    # Dodajemy wykładowców
    for lecturer_name in lecturers:
        lecturer = Lecturer(lecturer_name=lecturer_name)
        session.add(lecturer)
    session.commit()

    # Dodajemy studentów i przypisujemy ich do odpowiednich grup
    for student_name, group_id in zip(students, student_group):
        student = Student(student_name=student_name, student_group_id=group_id)
        session.add(student)
    session.commit()

    # Dodajemy przedmioty
    for subject_name, lecturer_name in subjects:
        lecturer = session.query(Lecturer).filter_by(lecturer_name=lecturer_name).first()
        # Sprawdzamy, czy student_group nie jest pusty przed wyborem losowego elementu
        if student_group and len(student_group) > 0:
            group_id = random.choice(list(set(student_group)))
        else:
            # Jeśli student_group jest puste, tworzymy nową grupę dla przedmiotu
            new_group = StudentGroup(group_name="New Group")
            session.add(new_group)
            session.commit()
            group_id = new_group.group_id
        subject = Subject(subject_name=subject_name, lecturer=lecturer, group_id=group_id)
        session.add(subject)
    session.commit()

    # Dodajemy oceny i przypisujemy je do odpowiednich studentów i przedmiotów
    for student_id, grade, grade_date, subject_name in grades:
        student = session.query(Student).filter_by(student_id=student_id).first()
        subject = session.query(Subject).filter_by(subject_name=subject_name).first()
        if student and subject:
            new_grade = Grade(grade=grade, created=grade_date, student=student, subject=subject)
            session.add(new_grade)
    session.commit()


if __name__ == "__main__":
    students, lecturers, student_group, subjects, grades = generate_fake_data(
        NUMBER_STUDENTS, NUMBER_LECTURERS, NUMBER_GROUPS, NUMBER_SUBJECTS, NUMBER_GRADES
    )
    insert_data_to_db(students, lecturers, student_group, subjects, grades)
    print(f"\nStudents: {students}\n")
    print(f"Lecturers: {lecturers}\n")
    print(f"Student_group: {student_group}\n")
    print(f"Subjects: {subjects}\n")
    print(f"Grades: {grades}")
