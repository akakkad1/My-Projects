from datetime import datetime
import csv

print("Welcome to your study planner!")

start=input("Do you want a study plan (A) or to add tasks (B)? ")

if start == "B" or "b":
    subject = input("Subject Name: ")
    name = input("Task Name: ")
    due = input("Due date in MM/DD/YYYY format: ")
    datetime.strptime(due, "%m/%d/%Y")
    comp = int(input("Estimated time of completion (in minutes): "))
    priority = int(input("Priority Level (1-5): "))

    with open("tasks.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([subject, name, due, comp, priority])

    tasks = []
    with open("tasks.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            tasks.append(row)

    tasks.sort(key=lambda x: datetime.strptime(x[2], "%m/%d/%Y"))

    with open("tasks.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(tasks)