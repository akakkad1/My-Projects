import os
os.system('clear')

print("Welcome to GPA Calculator.\n")

def check_courses():
    global course_amount 
    global apib_amount
    course_amount = int(input("How many courses do you have?: "))
    apib_amount = int(input("How many of those courses are AP/IB classes?: "))

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
