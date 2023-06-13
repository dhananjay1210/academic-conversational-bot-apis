from flask import Flask, request, jsonify
from flask_cors import CORS

from db import get_all_courses, get_course_by_professor, get_course_by_classroom, get_course_by_name, \
    get_course_by_code, get_student_courses, get_student_courses_info, add_a_course, get_student_by_id, drop_a_course

import json
import re

app = Flask(__name__)
CORS(app)


def normalize_code(input_str):
    # Remove non-alphanumeric characters and convert to lowercase
    normalized_str = re.sub(r'[^a-zA-Z0-9]', '', input_str.lower())
    return normalized_str.strip()


def normalize_professor(name):
    # remove professor, prof, dr., etc from name
    name = re.sub(r'professor', '', name.lower())
    name = re.sub(r'prof.', '', name.lower())
    name = re.sub(r'prof', '', name.lower())
    name = re.sub(r'dr.', '', name.lower())
    name = re.sub(r'dr', '', name.lower())
    return name.strip()


def format_course_info(course_details):
    return f"Code: {course_details['code']}\n" \
           f"Name: {course_details['name']}\n" \
           f"Professor: {course_details['professor']}\n" \
           f"Time: {course_details['time']}\n" \
           f"Classroom: {course_details['classroom']}"


def format_list_to_string(list_obj):
    return '\n'.join(list_obj)


@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello World!'})


# one version with query parameters
@app.route('/api/hello', methods=['GET'])
def hello2():
    name = request.args.get('name')
    return jsonify({'message': f'Hello {name}!'})


@app.route('/all-courses', methods=['GET'])
def all_courses():
    # get data from database
    courses = get_all_courses()
    return jsonify({"message": courses})


# create a webhook server to receive the data from the dialogflow
@app.route('/course-by-code', methods=['POST'])
def course_info():
    course_code = request.json.get('course_code')
    course_code = normalize_code(course_code)
    # get data from database
    courses = get_course_by_code(course_code)
    if len(courses) == 0:
        return jsonify({"message": "No course found"})
    return jsonify({"message": format_course_info(courses[0])})


# get course by professor
@app.route('/course-by-professor', methods=['POST'])
def by_professor():
    professor = request.json.get('professor')
    professor = normalize_professor(professor)
    courses = get_course_by_professor(professor)
    if len(courses) == 0:
        return jsonify({"message": "No professor found"})
    return jsonify({"message": format_course_info(courses[0])})


# get course by classroom
@app.route('/course-by-classroom', methods=['POST'])
def by_classroom():
    classroom = request.json.get('classroom')
    # get data from database
    courses = get_course_by_classroom(classroom)
    if len(courses) == 0:
        return jsonify({"message": "No classroom found"})
    return jsonify({"message": format_course_info(courses[0])})


# get course by name
@app.route('/course-by-name', methods=['POST'])
def by_name():
    course_name = request.json.get('course_name')
    # get data from database
    courses = get_course_by_name(course_name)
    if len(courses) == 0:
        return jsonify({"message": "No course found"})
    return jsonify({"message": format_course_info(courses[0])})


# who's this course's professor
@app.route('/who-is-the-prof-of-the-course', methods=['POST'])
def course_professor():
    course_code = request.json.get('course_code')
    course_code = normalize_code(course_code)
    # get data from database
    courses = get_course_by_code(course_code)
    if len(courses) == 0:
        return jsonify({"message": "No professor found for this course"})
    return jsonify({"message": format_list_to_string(["professor " + course['professor'] for course in courses])})


# professor's course
@app.route('/what-does-he-teach', methods=['POST'])
def professor_course():
    professor = request.json.get('professor')
    professor = normalize_professor(professor)
    # get data from database
    courses = get_course_by_professor(professor)
    if len(courses) == 0:
        return jsonify({"message": "No courses found for this professor"})
    return jsonify({"message": format_list_to_string([course['name'] for course in courses])})


# where is the location of the course
@app.route('/where-is-the-course', methods=['POST'])
def course_location():
    course_code = request.json.get('course_code')
    course_code = normalize_code(course_code)
    # get data from database
    courses = get_course_by_code(course_code)
    if len(courses) == 0:
        return jsonify({"message": "No course found"})
    return jsonify({"message": course_code + " happens at " + courses[0]['classroom']})


# student courses
@app.route('/student-courses', methods=['POST'])
def student_courses():
    student_id = request.json.get('student_id')
    # get data from database
    courses = get_student_courses(student_id)
    if len(courses) == 0:
        return jsonify({"message": "No courses found for this student"})
    return jsonify({"message": courses[0]})


# joint student courses version
@app.route('/student-courses-joint', methods=['POST'])
def student_courses_joint():
    student_id = request.json.get('student_id')
    # get data from database
    courses = get_student_courses_info(student_id)
    if len(courses) == 0:
        return jsonify({"message": "No courses found for this student"})
    return jsonify({"message": courses[0]})


# add a course to student courses
def student_exists(student_id):
    student = get_student_by_id(student_id)
    return len(student) > 0


@app.route('/enroll-course', methods=['POST'])
def enroll_course():
    student_id = request.json.get('student_id')
    course_code = request.json.get('course_code')
    course_code = normalize_code(course_code)
    # get data from database
    courses = get_course_by_code(course_code)
    if len(courses) == 0:
        return jsonify({"message": "Course doesn't exist"})
    course_code = courses[0]['code']

    # check if student exists
    if not student_exists(student_id):
        return jsonify({"message": "Student does not exist"})

    # get student courses
    stu_courses = get_student_courses(student_id)[0]
    # add if not already in the list
    if course_code in stu_courses:
        return jsonify({"message": "Course already added"})
    stu_courses.append(course_code)
    add_a_course(student_id, course_code)
    return jsonify({"message": "Course added"})


# drop a course from student courses
@app.route('/drop-course', methods=['POST'])
def drop_course():
    student_id = request.json.get('student_id')
    course_code = request.json.get('course_code')
    course_code = normalize_code(course_code)
    # get data from database
    courses = get_course_by_code(course_code)
    if len(courses) == 0:
        return jsonify({"message": "Course doesn't exist"})
    course_code = courses[0]['code']

    # check if student exists
    if not student_exists(student_id):
        return jsonify({"message": "Student does not exist"})

    # get student courses
    stu_courses = get_student_courses(student_id)[0]
    # remove if in the list
    if course_code not in stu_courses:
        return jsonify({"message": "Course not added"})
    stu_courses.remove(course_code)
    drop_a_course(student_id, course_code)
    return jsonify({"message": "Course dropped"})



# gunicorn app:app -c gunicorn_config.py --reload
