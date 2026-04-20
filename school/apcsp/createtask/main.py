# Add libraries and setup console
import os
os.system('clear')

print("Welcome to GPA Calculator.\n")

# Finds out how many courses the user has and saves them, along with a double-check function
def check_courses():
    while True:
        course_amt = int(input("How many courses do you have?: "))
        ap_amt = int(input("How many of those are AP/IB?: "))
        
        if ap_amt > course_amt:
            print("AP/IB count cannot exceed total courses. Try again.")
            continue

        os.system('clear')
        print(f"Total: {course_amt} | AP/IB: {ap_amt} | Regular: {course_amt - ap_amt}")
        user_check = input("Is this correct (y/n): ").lower()
        if user_check == 'y':
            os.system('clear')
            return course_amt, ap_amt
        elif user_check == 'n':
            os.system('clear')
            print("Restarting.\n")
        else:
            os.system('clear')
            print("Invalid input! Restarting.\n")
        

# Takes the return and defines course amounts from the function
course_amount, apib_amount = check_courses()
regular_amount = course_amount - apib_amount

# Sets up the lists needed to store grades and letters
letter_grades = ["a", "b", "c", "d", "f"]
apib_grades = []
regular_grades = []

# Goes through each course, asks the user for the grade, and saves it
i = 1
while i <= apib_amount:
    apib_letter = input(f"What was your letter grade in AP/IB course {i}: ").lower()
    if apib_letter in letter_grades:
        apib_grades.append(apib_letter)
        i += 1
    else:
        print("Invalid grade, try again.")

i = 1
while i <= regular_amount:
    regular_letter = input(f"What was your letter grade in regular course {i}: ").lower()
    if regular_letter in letter_grades:
        regular_grades.append(regular_letter)
        i += 1
    else:
        print("Invalid grade, try again.")

# Uses a dictionary to define the numeric value for each letter grade
gpa_points = {
    "a": 4,
    "b": 3,
    "c": 2,
    "d": 1,
    "f": 0
}

# Takes the letter grades inputted and uses the dictionary to calculate the gpa
def calculate_grades(regulars, apibs, is_weighted):
    total_points = 0
    for grade in regulars:
        total_points += gpa_points[grade]
    
    for grade in apibs:
        points = gpa_points[grade]
        # Statement to add the extra points for AP/IBs
        if is_weighted and grade != "f":
            points += 1
        total_points += points
    
    final_gpa = total_points / course_amount
        
    return final_gpa

# Uses the calculate_grades function to save and print a weighted and unweighted GPA
w_gpa = calculate_grades(regular_grades, apib_grades, True)
uw_gpa = calculate_grades(regular_grades, apib_grades, False)
os.system('clear')
print(f"Your Weighted GPA is: {round(w_gpa, 2)}")
print(f"Your Unweighted GPA is: {round(uw_gpa, 2)}")
