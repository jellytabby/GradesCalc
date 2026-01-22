from datetime import datetime
import sqlite3
import os
import json

def getDatabaseConnection():
    filePath = os.path.abspath(__file__)
    directory = os.path.dirname(filePath)
    conn = sqlite3.connect(directory + '/exams.db')
    return conn,conn.cursor()

def createdatabase():
    conn,cursor = getDatabaseConnection()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subjects (
            name TEXT PRIMARY KEY
        )
    ''')
    conn.commit()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            date TEXT NOT NULL,
            points_per_exercise TEXT NOT NULL,
            achieved_points REAL NOT NULL,
            max_points INTEGER NOT NULL,
            percentage REAL NOT NULL,
            grade REAL NOT NULL,
            FOREIGN KEY (subject_name) REFERENCES subjects(name)
        )
    ''')

def list_all():
    conn, cursor = getDatabaseConnection()
    cursor.execute('SELECT subjects.name, exams.name, exams.date, exams.percentage, exams.grade  FROM subjects JOIN exams on subjects.name = exams.subject_name')
    result = cursor.fetchall()


    print(f"| {'Subject':<10} | {'Exam Name':<15} | {'Date':<19} | {'Percentage':<10} | {'Grade':<5} |")
    print("-" * 75)

    for row in result:
        print(f"| {row[0]:<10} | {row[1]:<15} | {row[2]:<19} | {row[3]:<10.2f} | {row[4]:<5.2f} |")

    conn.commit()
    conn.close()

def saveToDatabase(pointsArray, totalAchievedPoints, maximumPossiblePoints):
    if input("Would you like to save this exam to the database? \n")[0].lower() != 'y':
        exit(0)

    conn, cursor = getDatabaseConnection()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject_name = input("Please enter the subject shorthand: \n").lower()
    cursor.execute('SELECT name FROM subjects WHERE name = ?', (subject_name,))
    result = cursor.fetchone()

    # If the subject doesn't exist, insert it
    if result is None:
        if input(f"The subject {subject_name} doesn't exist yet, would you like to create it? \n")[0].lower() != 'y':
            exit(-1)
        cursor.execute('INSERT INTO subjects (name) VALUES (?)', (subject_name,))
        conn.commit()

    exam_name = input("Please enter an exam name: \n")
    percentage = totalAchievedPoints / int(maximumPossiblePoints) * 100
    grade = totalAchievedPoints / int(maximumPossiblePoints) * 5 + 1

    cursor.execute('''
            INSERT INTO exams (name, subject_name, date, points_per_exercise, achieved_points,max_points, percentage, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (exam_name, subject_name, date, json.dumps(pointsArray), totalAchievedPoints,  maximumPossiblePoints, percentage, grade))
    conn.commit()
    conn.close()
