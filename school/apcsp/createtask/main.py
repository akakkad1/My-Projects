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
        apib_grades.append(apib_letter)
        i += 1
    else:
        print("Invalid grade, this grade will not be counted.")

i = 1
while i <= regular_amount:
    regular_letter = input(f"What was your letter grade in regular course {i}: ")
    if regular_letter in letter_grades:
        regular_grades.append(regular_letter)
        i += 1
    else:
        print("Invalid grade, this grade will not be counted.")