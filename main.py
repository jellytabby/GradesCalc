import argparse
import db


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



def parse_args():
    parser = argparse.ArgumentParser(prog="grades",)
    parser.add_argument('-l', '--list', action='store_true', help='list all saved exams in the database')
    return parser.parse_args();


if __name__ == '__main__':
    db.createdatabase()
    args = parse_args();
    if args.list:
        db.list_all()
        exit(0)

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
    db.saveToDatabase(pointsArray, totalAchievedPoints, maximumPossiblePoints)


