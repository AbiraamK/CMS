# Course Management System - Requirements and Overview

## Required Technologies

- **Flask** v2.3.2
- **Flask-Login** v0.6.3
- **pymysql** v1.0.3
- **Python** v3.7

## Application Overview

### Description
The Course Management System (CMS) is a web-based application that facilitates the management of educational courses. The application allows:
- **Teachers** to manage course content and student progress.
- **Students** to register, track, and manage their courses.
- **Administrators** to oversee system operations and manage users and courses.

### Key Features
- **User Registration:** 
  Allows users to register as either a student, teacher, or teaching assistant (TA) by providing their name, username, and password.

- **User Login:** 
  Registered users can securely log in to access their respective dashboards.

- **Course Enrollment:** 
  - **Students** can enroll in and remove themselves from courses.
  - **Teachers** and **TAs** can apply to teach or assist courses.

- **Role-Based Access Control:** 
  Ensures users access features appropriate to their role (Student, Teacher, TA, or Admin).

- **Privacy and Security:** 
  Secure login system with encryption, role-based access, and session management.

### User Guide

1. **Register a New User:**
   - Select the role (Student, Teacher, or TA) and complete the registration form.
   - Upon successful registration, users are redirected to the homepage.

2. **Login:**
   - Enter the registered username and password to log in.
   - Successful login redirects the user to their dashboard.

3. **Dashboard Access:**
   - **Students:** Can view, enroll in, and remove courses.
   - **Teachers:** Can apply to teach and view assigned courses.
   - **TAs:** Can apply for and view TA assignments.

4. **Logout:**
   - When done, users can log out to end their session securely.

### Admin Access
- **Admin Dashboard:** Administrators can manage courses, users, and system queries.

## Technologies Utilized

- **HTML:** For page structure and content layout.
- **CSS:** For styling and layout.
- **MySQL:** Database management system for backend data storage and manipulation.

## Database Schema

- **Person** (person_id, name, role, username, password) - Users of the system with roles as 'student', 'teacher', 'TA', or 'admin'.
- **Course** (course_id, course_name, description) - Available courses.
- **CourseInstructor** (course_id, person_id) - Teachers assigned to courses.
- **CourseTA** (course_id, ta_id) - TAs assigned to courses.
- **StudentCourse** (person_id, course_id) - Courses that students are enrolled in.

### SQL Queries
Sample queries utilized by the CMS:
- **User Management:** `SELECT * FROM person WHERE person_id = %s`
- **Course Enrollment:** `INSERT INTO studentcourse (student_id, course_id) VALUES (%s, %s)`
- **TA Application:** `INSERT INTO courseta (ta_id, course_id) VALUES (%s, %s)`
- **Teacher Assignment:** `INSERT INTO courseinstructor (instructor_id, course_id) VALUES (%s, %s)`

## Conclusion

The Course Management System provides a streamlined approach to course and user management, allowing educational institutions to efficiently handle course enrollment, administration, and role-based functionality. The CMS enhances productivity and reduces the need for manual course administration.
