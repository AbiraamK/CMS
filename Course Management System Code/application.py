from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pymysql

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'simple_key'
login_manager = LoginManager(app)

#--------------------------------------------------
# Connects to MySQL database with specified parameters
def connect_to_database():
    return pymysql.connect(
        host="Insert WebHost Here",
        user="Insert Username Here",
        password="Insert Password Here",
        database="Insert Database Here",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# User class for Flask-Login integration
class User(UserMixin):
    def __init__(self, person_id=None, name=None, username=None, password=None, role=None):
        self.person_id = person_id
        self.name = name
        self.username = username
        self.password = password
        self.role = role
    
    # Returns the unique identifier for the user
    def get_id(self):
        return self.person_id

# Executes a query that does not return results (INSERT, UPDATE, DELETE)
def execute_query(query, params=None):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
        connection.commit()
    finally:
        connection.close()

# Loads a user by ID for session management
@login_manager.user_loader
def load_user(user_id):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM person WHERE person_id = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                user = User()
                user.person_id = result['person_id']
                user.name = result['name']
                user.username = result['username']
                user.password = result['password']
                user.role = result['role']
                return user
    finally:
        connection.close()
    return None

# Route for registering students
@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        role = 'student'
        
        # Check if the username already exists
        connection = connect_to_database()
        username_exists = False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM person WHERE username = %s", (username,))
                if cursor.fetchone() is not None:
                    username_exists = True
        finally:
            connection.close()

        if username_exists:
            flash('Username already taken')
            return redirect(url_for('register_student'))
        else:
            execute_query("INSERT INTO person (name, username, password, role) VALUES (%s, %s, %s, %s)", (name, username, password, role))
            flash('Student registered successfully')
            return redirect(url_for('index'))
    return render_template('register_student.html')

# Route for registering teachers
@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        role = 'teacher'
        
        # Check if the username already exists
        connection = connect_to_database()
        username_exists = False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM person WHERE username = %s", (username,))
                if cursor.fetchone() is not None:
                    username_exists = True
        finally:
            connection.close()

        if username_exists:
            flash('Username already taken')
            return redirect(url_for('register_teacher'))
        else:
            execute_query("INSERT INTO person (name, username, password, role) VALUES (%s, %s, %s, %s)", (name, username, password, role))
            flash('Teacher registered successfully')
            return redirect(url_for('index'))
    return render_template('register_teacher.html')

# Route for registering TAs
@app.route('/register_ta', methods=['GET', 'POST'])
def register_ta():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        role = 'ta'
        
        # Check if the username already exists
        connection = connect_to_database()
        username_exists = False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM person WHERE username = %s", (username,))
                if cursor.fetchone() is not None:
                    username_exists = True
        finally:
            connection.close()

        if username_exists:
            flash('Username already taken')
            return redirect(url_for('register_ta'))
        else:
            execute_query("INSERT INTO person (name, username, password, role) VALUES (%s, %s, %s, %s)", (name, username, password, role))
            flash('TA registered successfully')
            return redirect(url_for('index'))
    return render_template('register_ta.html')

# Student course registration route
@app.route('/student/courses', methods=['GET', 'POST'])
@login_required
def student_courses():
    if current_user.role != 'student':
        flash('Access denied')
        return redirect(url_for('index'))

    connection = connect_to_database()
    courses = []

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM course")
            courses = cursor.fetchall()
    finally:
        connection.close()

    if request.method == 'POST':
        course_id = request.form.get('course_id')
        student_id = current_user.person_id

        connection = connect_to_database()
        already_registered = False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM studentcourse WHERE student_id = %s AND course_id = %s", (student_id, course_id))
                if cursor.fetchone() is not None:
                    already_registered = True
        finally:
            connection.close()

        if already_registered:
            flash('You have already registered for this course')
        else:
            execute_query("INSERT INTO studentcourse (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
            flash('Course registered successfully')
        return redirect(url_for('student_courses'))

    return render_template('student_courses.html', courses=courses)

# TA course application route
@app.route('/ta/courses', methods=['GET', 'POST'])
@login_required
def ta_courses():
    if current_user.role != 'ta':
        flash('Access denied')
        return redirect(url_for('index'))

    connection = connect_to_database()
    courses = []

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM course")
            courses = cursor.fetchall()
    finally:
        connection.close()

    if request.method == 'POST':
        course_id = request.form.get('course_id')
        ta_id = current_user.person_id

        connection = connect_to_database()
        already_applied = False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM courseta WHERE ta_id = %s AND course_id = %s", (ta_id, course_id))
                if cursor.fetchone() is not None:
                    already_applied = True
        finally:
            connection.close()

        if already_applied:
            flash('You have already applied to TA this course')
        else:
            execute_query("INSERT INTO courseta (ta_id, course_id) VALUES (%s, %s)", (ta_id, course_id))
            flash('Applied to TA course successfully')
        return redirect(url_for('ta_courses'))

    return render_template('ta_courses.html', courses=courses)

# Teacher course application route
@app.route('/teacher/courses', methods=['GET', 'POST'])
@login_required
def teacher_courses():
    if current_user.role != 'teacher':
        flash('Access denied')
        return redirect(url_for('index'))

    connection = connect_to_database()
    courses = []

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM course")
            courses = cursor.fetchall()
    finally:
        connection.close()

    if request.method == 'POST':
        course_id = request.form.get('course_id')
        teacher_id = current_user.person_id

        connection = connect_to_database()
        already_applied = False
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM courseinstructor WHERE instructor_id = %s AND course_id = %s", (teacher_id, course_id))
                if cursor.fetchone() is not None:
                    already_applied = True
        finally:
            connection.close()

        if already_applied:
            flash('You have already applied to teach this course')
        else:
            execute_query("INSERT INTO courseinstructor (instructor_id, course_id) VALUES (%s, %s)", (teacher_id, course_id))
            flash('Applied to teach course successfully')
        return redirect(url_for('teacher_courses'))

    return render_template('teacher_courses.html', courses=courses)

# Admin association viewing route
@app.route('/admin/associations')
@login_required
def admin_associations():
    if current_user.role != 'admin':
        flash('Access denied')
        return redirect(url_for('index'))

    students = get_students_with_courses()
    tas = get_tas_with_courses()
    teachers = get_teachers_with_courses()

    return render_template('admin_associations.html', students=students, tas=tas, teachers=teachers)

# Helper function to get students and their enrolled courses
def get_students_with_courses():
    connection = connect_to_database()
    students = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT person.*, course.course_id, course.course_name
                              FROM person
                              JOIN studentcourse ON person.person_id = studentcourse.student_id
                              JOIN course ON studentcourse.course_id = course.course_id
                              WHERE person.role = 'student'
                              ORDER BY person.person_id""")
            students = cursor.fetchall()
    finally:
        connection.close()
    return students

# Helper function to get TAs and their teaching courses
def get_tas_with_courses():
    connection = connect_to_database()
    tas = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT person.*, course.course_id, course.course_name
                              FROM person
                              JOIN courseta ON person.person_id = courseta.ta_id
                              JOIN course ON courseta.course_id = course.course_id
                              WHERE person.role = 'ta'
                              ORDER BY person.person_id""")
            tas = cursor.fetchall()
    finally:
        connection.close()
    return tas

# Helper function to get teachers and their teaching courses
def get_teachers_with_courses():
    connection = connect_to_database()
    teachers = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT person.*, course.course_id, course.course_name
                              FROM person
                              JOIN courseinstructor ON person.person_id = courseinstructor.instructor_id
                              JOIN course ON courseinstructor.course_id = course.course_id
                              WHERE person.role = 'teacher'
                              ORDER BY person.person_id""")
            teachers = cursor.fetchall()
    finally:
        connection.close()
    return teachers

# Home route
@app.route('/')
def index():
    user_role = None
    if current_user.is_authenticated:
        user_role = current_user.role
    return render_template('index.html', user_role=user_role)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('index'))
