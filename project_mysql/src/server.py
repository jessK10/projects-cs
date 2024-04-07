import os
import mysql.connector
from flask import Flask, render_template
import pymysql

# Initialize Flask app with the correct template folder
app = Flask(__name__)
app.config['DEBUG'] = True
# Function to retrieve data from the database for each year separately
def get_data_from_database():
    print("get_data_from_database() function called")
    # Establish connection to the database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute query to retrieve student count per program and year for 2020
    student_count_query_2020 = """
    SELECT s.student_population_code_ref,
           COUNT(*) AS student_count
    FROM students s
    WHERE s.student_population_year_ref = 2020
    GROUP BY s.student_population_code_ref;
    """
    cursor.execute(student_count_query_2020)
    print("Student count query for 2020 executed")
    student_count_results_2020 = cursor.fetchall()

    # Execute query to calculate attendance percentage per program and year for 2020
    attendance_percentage_query_2020 = """
    SELECT s.student_population_code_ref,
           SUM(a.attendance_presence)*100 / COUNT(*) AS attendance_percentage
    FROM students s
    JOIN attendance a ON s.student_epita_email = a.attendance_student_ref
    WHERE s.student_population_year_ref = 2020
    GROUP BY s.student_population_code_ref;
    """
    cursor.execute(attendance_percentage_query_2020)
    print("Student attend query for 2020 executed")
    attendance_percentage_results_2020 = cursor.fetchall()

    # Execute query to retrieve student count per program and year for 2021
    student_count_query_2021 = """
    SELECT s.student_population_code_ref,
           COUNT(*) AS student_count
    FROM students s
    WHERE s.student_population_year_ref = 2021
    GROUP BY s.student_population_code_ref;
    """
    cursor.execute(student_count_query_2021)
    print("Student count query for 2021 executed")
    student_count_results_2021 = cursor.fetchall()

    # Execute query to calculate attendance percentage per program and year for 2021
    attendance_percentage_query_2021 = """
    SELECT s.student_population_code_ref,
           SUM(a.attendance_presence)*100 / COUNT(*) AS attendance_percentage
    FROM students s
    JOIN attendance a ON s.student_epita_email = a.attendance_student_ref
    WHERE s.student_population_year_ref = 2021
    GROUP BY s.student_population_code_ref;
    """
    cursor.execute(attendance_percentage_query_2021)
    print("Student attend query for 2021 executed")
    attendance_percentage_results_2021 = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    connection.close()

    return (student_count_results_2020, student_count_results_2021), (attendance_percentage_results_2020, attendance_percentage_results_2021)

def get_population_data(program_code,year_code):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )
    cursor = connection.cursor(dictionary=True)

    # Query to retrieve student information
    student_query = f"""
    SELECT 
    c.contact_first_name AS student_first_name,
    c.contact_last_name AS student_last_name,
    s.student_epita_email AS student_email,
    SUM(CASE WHEN g.grade_score >= 10 THEN 1 ELSE 0 END) AS passed_courses
FROM 
    students s
JOIN 
    contacts c ON s.student_contact_ref = c.contact_email
LEFT JOIN 
    grades g ON s.student_epita_email = g.grade_student_epita_email_ref
WHERE 
    s.student_population_code_ref = '{program_code}' AND
    s.student_population_year_ref = '{year_code}'
GROUP BY 
    s.student_epita_email, c.contact_first_name, c.contact_last_name;

    """


    course_query = f"""
    SELECT DISTINCT
        c.course_code,
        c.course_name,
        c.duration
    FROM
        students s
    JOIN
        grades g ON s.student_epita_email = g.grade_student_epita_email_ref
    JOIN
        courses c ON g.grade_course_code_ref = c.course_code
    WHERE
        s.student_population_code_ref = '{program_code}';
    """


    cursor.execute(student_query)
    students = cursor.fetchall()

    cursor.execute(course_query)
    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return students, courses


def get_grade_data(program_code, course_code):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )
    cursor = connection.cursor(dictionary=True)

    # Query to retrieve grades for the specified program, course, and year 2021
    grade_query = """
    SELECT 
    c.contact_first_name AS student_first_name,
    c.contact_last_name AS student_last_name,
    g.grade_score,
    cr.course_name
FROM 
    students s
JOIN 
    contacts c ON s.student_contact_ref = c.contact_email
JOIN 
    grades g ON s.student_epita_email = g.grade_student_epita_email_ref
JOIN 
    courses cr ON g.grade_course_code_ref = cr.course_code
WHERE 
    s.student_population_code_ref = %s AND
    g.grade_course_code_ref = %s AND
    s.student_population_year_ref = 2021;

    """

    cursor.execute(grade_query, (program_code, course_code))
    grades = cursor.fetchall()

    cursor.close()
    connection.close()

    return grades
app = Flask(__name__)
db = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="project"
    )

@app.route("/")
def index():
    cursor = db.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM students WHERE student_population_code_ref = 'AIs' AND student_population_year_ref = '2021';"
    )
    count_ais = cursor.fetchall()

    cursor2 = db.cursor()
    cursor2.execute(
        "SELECT COUNT(*) FROM students WHERE student_population_code_ref = 'CS' AND student_population_year_ref = '2021';"
    )
    count_cs = cursor2.fetchall()

    cursor3 = db.cursor()
    cursor3.execute(
        "SELECT COUNT(*) FROM students WHERE student_population_code_ref = 'DSA' AND student_population_year_ref = '2021';"
    )
    count_dsa = cursor3.fetchall()
    
    cursor4 = db.cursor()
    cursor4.execute(
        "SELECT COUNT(*) FROM students WHERE student_population_code_ref = 'ISM' AND student_population_year_ref = '2021';"
    )
    count_ism = cursor4.fetchall()
    
    cursor5 = db.cursor()
    cursor5.execute(
        "SELECT COUNT(*) FROM students WHERE student_population_code_ref = 'SE' AND student_population_year_ref = '2021';"
    )
    count_se = cursor5.fetchall()

    students = (count_ais, count_cs, count_dsa, count_ism, count_se)

    # ------------ Attendance ------------
    # ----- AIs -----
    cursor6 = db.cursor()
    cursor6.execute("SELECT s.student_population_code_ref,COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences,COUNT(*) AS total_records,ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage FROM students s LEFT JOIN attendance a ON s.student_epita_email = a.attendance_student_ref WHERE s.student_population_code_ref = 'AIs' AND a.attendance_population_year_ref = 2020 GROUP BY s.student_population_code_ref;")
    attendance_ais_2020 = cursor6.fetchall()
    
    # ----- CS -----
    cursor7 = db.cursor()
    cursor7.execute("SELECT s.student_population_code_ref, COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences, COUNT(*) AS total_records, ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage FROM students s LEFT JOIN attendance a ON s.student_epita_email = a.attendance_student_ref WHERE s.student_population_code_ref = 'CS' AND a.attendance_population_year_ref = 2020 GROUP BY s.student_population_code_ref;")
    attendance_cs_2020 = cursor7.fetchall()
    
    # ----- DSA -----
    cursor8 = db.cursor()
    cursor8.execute("SELECT s.student_population_code_ref, COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences, COUNT(*) AS total_records, ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage FROM students s LEFT JOIN attendance a ON s.student_epita_email = a.attendance_student_ref WHERE s.student_population_code_ref = 'DSA' AND a.attendance_population_year_ref = 2020 GROUP BY s.student_population_code_ref;")
    attendance_dsa_2020 = cursor8.fetchall()
    
    # ----- ISM -----
    cursor9 = db.cursor()
    cursor9.execute("SELECT s.student_population_code_ref, COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences, COUNT(*) AS total_records, ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage\
                    FROM\
                        students s\
                    LEFT JOIN\
                        attendance a ON s.student_epita_email = a.attendance_student_ref\
                    WHERE\
                        s.student_population_code_ref = 'ISM'\
                        AND a.attendance_population_year_ref = 2020\
                    GROUP BY\
                        s.student_population_code_ref;")
    attendance_ism_2020 = cursor9.fetchall()
    
    cursor10 = db.cursor()
    cursor10.execute("SELECT s.student_population_code_ref, COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences, COUNT(*) AS total_records, ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage FROM students s LEFT JOIN attendance a ON s.student_epita_email = a.attendance_student_ref WHERE s.student_population_code_ref = 'SE' AND a.attendance_population_year_ref = 2020 GROUP BY s.student_population_code_ref;")
    attendance_se_2020 = cursor10.fetchall()
    cursor11 = db.cursor()
    cursor11.execute("SELECT s.student_population_code_ref,COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences,COUNT(*) AS total_records,ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage FROM students s LEFT JOIN attendance a ON s.student_epita_email = a.attendance_student_ref WHERE s.student_population_code_ref = 'AIs' AND a.attendance_population_year_ref = 2021 GROUP BY s.student_population_code_ref;")
    attendance_ais_2021 = cursor11.fetchall()
    
    # ----- CS -----
    cursor12 = db.cursor()
    cursor12.execute("SELECT s.student_population_code_ref, COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences, COUNT(*) AS total_records, ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage FROM students s LEFT JOIN attendance a ON s.student_epita_email = a.attendance_student_ref WHERE s.student_population_code_ref = 'CS' AND a.attendance_population_year_ref = 2021 GROUP BY s.student_population_code_ref;")
    attendance_cs_2021 = cursor12.fetchall()
    
    # ----- DSA -----
    cursor13 = db.cursor()
    cursor13.execute("SELECT s.student_population_code_ref, COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences, COUNT(*) AS total_records, ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage FROM students s LEFT JOIN attendance a ON s.student_epita_email = a.attendance_student_ref WHERE s.student_population_code_ref = 'DSA' AND a.attendance_population_year_ref = 2021 GROUP BY s.student_population_code_ref;")
    attendance_dsa_2021 = cursor13.fetchall()
    
    # ----- ISM -----
    cursor14 = db.cursor()
    cursor14.execute("SELECT s.student_population_code_ref, COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences, COUNT(*) AS total_records, ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage\
                    FROM\
                        students s\
                    LEFT JOIN\
                        attendance a ON s.student_epita_email = a.attendance_student_ref\
                    WHERE\
                        s.student_population_code_ref = 'ISM'\
                        AND a.attendance_population_year_ref = 2021\
                    GROUP BY\
                        s.student_population_code_ref;")
    attendance_ism_2021 = cursor14.fetchall()
    
    cursor15 = db.cursor()
    cursor15.execute("SELECT s.student_population_code_ref, COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) AS total_presences, COUNT(*) AS total_records, ROUND((COUNT(CASE WHEN a.attendance_presence = 1 THEN 1 END) * 100.0 / COUNT(*)), 2) AS presence_percentage FROM students s LEFT JOIN attendance a ON s.student_epita_email = a.attendance_student_ref WHERE s.student_population_code_ref = 'SE' AND a.attendance_population_year_ref = 2021 GROUP BY s.student_population_code_ref;")
    attendance_se_2021 = cursor15.fetchall()
    
    
    attendance_2020 = (attendance_ais_2020, attendance_cs_2020, attendance_dsa_2020, attendance_ism_2020, attendance_se_2020)
    attendance_2021=(attendance_ais_2021,attendance_cs_2021,attendance_dsa_2021,attendance_ism_2021,attendance_se_2021)
    print(attendance_2020)
    print(attendance_2021)
    return render_template("wel.html", students=students, attendance_2020=attendance_2020,attendance_2021=attendance_2021) 
    

@app.route("/population/<program_code>/<year_code>")
def population_page(program_code,year_code): 
    students, courses = get_population_data(program_code,year_code)
    return render_template('population_page.html', program_code=program_code, students=students, courses=courses,year_code=year_code)

@app.route("/population/<program_code>/course/<course_code>/grades")
def course_grade(program_code,course_code):
    grades_data = get_grade_data(program_code, course_code)
    
    # Render the course grades page template with the grades data
    return render_template('course_grade.html', grades_data=grades_data)


if __name__ == "__main__":
    app.run(debug=True)

