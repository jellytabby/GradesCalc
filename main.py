import sqlite3
import os
from datetime import datetime
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
            subject_name INTEGER NOT NULL,
            date TEXT NOT NULL,
            points_per_exercise TEXT NOT NULL,
            achieved_points INTEGER NOT NULL,
            max_points INTEGER NOT NULL,
            percentage REAL NOT NULL,
            grade REAL NOT NULL,
            FOREIGN KEY (subject_name) REFERENCES subjects(name)
        )
    ''')
def prettyprinting(pointsArray, totalAchievedPoints, maximumPossiblePoints):
    percent = totalAchievedPoints / int(maximumPossiblePoints) * 100
    grade = totalAchievedPoints / int(maximumPossiblePoints) * 5 + 1

    out = "| "
    for i in range(len(pointsArray)):
        out += (str(pointsArray[i]) + " | ")
    print("-" * len(out))
    print(out)
    print("-" * len(out))
    print("Total points: " + str(maximumPossiblePoints) + " | ", end="")
    print("Achieved points: " + str(totalAchievedPoints))
    print("Percent: " + str(round(percent, 2)) + "%")
    print("Grade: " + str(round(grade, 2)))
    print()


def saveToDatabase(pointsArray, totalAchievedPoints, maximumPossiblePoints):
    if input("Would you like to save this exam to the database? \n")[0].lower() != 'y':
        exit(0)

    conn, cursor = getDatabaseConnection()

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject_name = input("Please enter the subject shorthand: \n").lower()
    cursor.execute('SELECT id FROM subjects WHERE name = ?', (subject_name,))
    result = cursor.fetchone()

    # If the subject doesn't exist, insert it
    if result is None:
        if input(f"The subject {subject_name} doesn't exist yet, would you like to create it? \n")[0].lower() != 'y':
            exit(-1)
        cursor.execute('INSERT INTO subjects (name) VALUES (?)', (subject_name,))
        conn.commit()
        subject_name = cursor.lastrowid
    else:
        subject_name = result[0]

    exam_name = input("Please enter an exam name: \n")
    percentage = totalAchievedPoints / int(maximumPossiblePoints) * 100
    grade = totalAchievedPoints / int(maximumPossiblePoints) * 5 + 1

    cursor.execute('''
            INSERT INTO exams (name, subject_name, date, points_per_exercise, achieved_points,max_points, percentage, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (exam_name, subject_name, date, json.dumps(pointsArray), totalAchievedPoints,  maximumPossiblePoints, percentage, grade))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    createdatabase()
    inputMaxPoints = input("Total number of points: \n")
    if inputMaxPoints != "" and isinstance(eval(inputMaxPoints), (int, float)):
        maximumPossiblePoints = eval(inputMaxPoints)
    else:
        print("Invalid input!")
        exit(-1)
    pointsArray = []
    totalAchievedPoints = 0

    pointsOfOneExercise = 0
    while True:
        pointsOfOneExercise = (input("Exercise points: \n"))

        if pointsOfOneExercise == "":
            break
        else:
            pointsOfOneExercise = eval(pointsOfOneExercise)
            if (not isinstance(pointsOfOneExercise, (float, int))) or (pointsOfOneExercise < 0):
                print("Invalid input!")
                continue
            pointsArray.append(pointsOfOneExercise)
            totalAchievedPoints += pointsOfOneExercise

            if totalAchievedPoints > maximumPossiblePoints:
                print("Total number of points exceeded!")
                ans = input("Do you want to reenter the last value? \n")
                if ans.lower()[0] == "y":
                    totalAchievedPoints -= pointsOfOneExercise
                    pointsArray.pop(-1)
                else:
                    exit(-1)
    prettyprinting(pointsArray, totalAchievedPoints, maximumPossiblePoints)
    saveToDatabase(pointsArray, totalAchievedPoints, maximumPossiblePoints)


