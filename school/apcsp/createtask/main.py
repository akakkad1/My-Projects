import os
os.system('clear')

print("Welcome to GPA Calculator.\n")

def check_courses():
    global course_amount
    global apib_amount
    global regular_amount
    course_amount = int(input("How many courses do you have?: "))
    apib_amount = int(input("How many of those courses are AP/IB classes?: "))
    regular_amount = course_amount - apib_amount

    while apib_amount > course_amount:
        apib_amount = int(input("Too many AP/IB classes, please try again: "))
    
    course_double_check = input(f"""
    You have: 
    {course_amount - apib_amount} regular classes.
    {apib_amount} AP/IB classes. 
    Is this correct? (y/n): """)

    if course_double_check == "y":
        os.system('clear')
    elif course_double_check == "n":
        os.system('clear')
        check_courses()
    else:
        print("Invalid option, restarting.\n")
        check_courses()

check_courses()
os.system('clear')

letter_grades = ["A","B","C","D","F"]
apib_grades = []
regular_grades = []

i = 1
while i <= apib_amount:
    apib_letter = input(f"What was your letter grade in AP/IB course {i}: ")
    if apib_letter in letter_grades:
        apib_grades.append(apib_letter.lower())
        i += 1
    else:
        print("Invalid grade, this grade will not be counted.")

i = 1
while i <= regular_amount:
    regular_letter = input(f"What was your letter grade in regular course {i}: ")
    if regular_letter in letter_grades:
        regular_grades.append(regular_letter.lower())
        i += 1
    else:
        print("Invalid grade, this grade will not be counted.")

for i, vals in enumerate(apib_grades):
    if vals == "a":
        apib_grades[i] = "z"
    elif vals == "b":
        apib_grades[i] = "a"
    elif vals == "c":
        apib_grades[i] = "b"
    elif vals == "d":
        apib_grades[i] = "c"
    elif vals == "f":
        apib_grades[i] = "d"


def calculate_grades(regulars,apibs):
    gpa_calc = 0
    all_grades = regulars + apibs
    for grade in all_grades:
        if grade == "z":
            gpa_calc += 5
        elif grade == "a":
            gpa_calc += 4
        elif grade == "b":
            gpa_calc += 3
        elif grade == "c":
            gpa_calc += 2
        elif grade == "d":
            gpa_calc += 1
        elif grade == "f":
            gpa_calc += 0
    return gpa_calc

gpa_sum = calculate_grades(regular_grades,apib_grades)
print(gpa_sum)
final_gpa = gpa_sum/course_amount
print(final_gpa)
