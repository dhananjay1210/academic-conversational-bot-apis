import psycopg2

# Connection details
connection_details = {
    'host': 'app-16564b8c-0bce-4a0f-b03e-8bdcbfb60c4d-do-user-14204294-0.b.db.ondigitalocean.com',
    'port': '25060',
    'user': 'ucscdb',
    'password': 'AVNS_woazzncMXeL8z1nE7w-',
    'database': 'ucscdb',
    'sslmode': 'require'
}

# Establish a connection to the database
conn = psycopg2.connect(**connection_details)

# Create a cursor object to interact with the database
cur = conn.cursor()


# "name": "<class name>",
# "professor": "<professor>",
# "time": "<time>"
# "classroom": "<classroom>",
# "code": "<code>"

def get_all_courses():
    cur.execute("SELECT * FROM courses")
    rows = cur.fetchall()

    courses = []
    for row in rows:
        course = {
            "name": row[1],
            "professor": row[2],
            "time": row[3],
            "classroom": row[4],
            "code": row[5]
        }
        courses.append(course)
    return courses


# get course by code
def get_course_by_code(course_code):
    cur.execute("SELECT * FROM courses WHERE code ILIKE %s", ('%' + course_code + '%',))
    rows = cur.fetchall()

    courses = []
    for row in rows:
        course = {
            "name": row[1],
            "professor": row[2],
            "time": row[3],
            "classroom": row[4],
            "code": row[5]
        }
        courses.append(course)
    return courses


# get course by professor
def get_course_by_professor(professor):
    cur.execute("SELECT * FROM courses WHERE professor ILIKE %s", (professor,))
    rows = cur.fetchall()

    courses = []
    for row in rows:
        course = {
            "name": row[1],
            "professor": row[2],
            "time": row[3],
            "classroom": row[4],
            "code": row[5]
        }
        courses.append(course)
    return courses


# get course by classroom
def get_course_by_classroom(classroom):
    cur.execute("SELECT * FROM courses WHERE classroom ILIKE %s", (classroom,))
    rows = cur.fetchall()

    courses = []
    for row in rows:
        course = {
            "name": row[1],
            "professor": row[2],
            "time": row[3],
            "classroom": row[4],
            "code": row[5]
        }
        courses.append(course)
    return courses


# get course by name
def get_course_by_name(course_name):
    # select if part of the name is in the course name
    cur.execute("SELECT * FROM courses WHERE name ILIKE %s", ('%' + course_name + '%',))
    rows = cur.fetchall()

    courses = []
    for row in rows:
        course = {
            "name": row[1],
            "professor": row[2],
            "time": row[3],
            "classroom": row[4],
            "code": row[5]
        }
        courses.append(course)
    return courses


def get_course_code_by_professor(professor):
    cur.execute("SELECT code FROM courses WHERE professor ILIKE %s", (professor,))
    rows = cur.fetchall()

    courses = []
    for row in rows:
        courses.append(row[0])
    return courses


def get_student_courses(student_id):
    cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    rows = cur.fetchall()

    courses = []
    for row in rows:
        courses.append(row[1])
    return courses


# joint table for student and courses
def get_student_courses_info(student_id):
    cur.execute(
        "SELECT * FROM student_course JOIN courses ON student_course.course_id = courses.code WHERE student_id = %s",
        (student_id,))
    rows = cur.fetchall()

    courses = []
    for row in rows:
        course = {
            "student_id": row[0],
            "name": row[3],
            "code": row[7]
        }
        courses.append(course)
    return courses


# update students table courses column
def add_a_course(student_id, course_code):
    cur.execute("UPDATE students SET courses = array_append(courses, %s) WHERE student_id = %s",
                (course_code, student_id))
    conn.commit()


# remove course from students table courses column
def drop_a_course(student_id, course_code):
    cur.execute("UPDATE students SET courses = array_remove(courses, %s) WHERE student_id = %s",
                (course_code, student_id))
    conn.commit()


# get student by id
def get_student_by_id(student_id):
    cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))
    rows = cur.fetchall()
    students = []
    for row in rows:
        student = {
            "student_id": row[0],
            "name": row[1],
            "courses": row[2]
        }
        students.append(student)
    return students
