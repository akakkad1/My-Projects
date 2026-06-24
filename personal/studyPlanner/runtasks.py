from datetime import datetime
import csv, os

FILE = "tasks.csv"

def get_int(prompt, lo=1, hi=None):
    while True:
        try:
            x = int(input(prompt))
            if (hi is None or lo <= x <= hi):
                return x
        except:
            pass
        print("Invalid input.")

def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE) as f:
        return list(csv.reader(f))

def save_tasks(tasks):
    with open(FILE, "w", newline="") as f:
        csv.writer(f).writerows(tasks)

while True:
    print("\nWelcome to your study planner!")
    choice = input("(A) Study plan or (B) Add task? ").strip().lower()

    # ---------------- ADD TASK ----------------
    if choice == "b":
        subject = input("Subject: ")
        name = input("Task name: ")

        while True:
            due = input("Due date (MM/DD/YYYY): ")
            try:
                datetime.strptime(due, "%m/%d/%Y")
                break
            except:
                print("Invalid date.")

        comp = get_int("Minutes to complete: ")
        priority = get_int("Priority (1-5): ", 1, 5)

        tasks = load_tasks()
        tasks.append([subject, name, due, str(comp), str(priority)])
        tasks.sort(key=lambda x: datetime.strptime(x[2], "%m/%d/%Y"))
        save_tasks(tasks)

        print("Task added!")

    # ---------------- STUDY PLAN ----------------
    elif choice == "a":
        tasks = load_tasks()
        if not tasks:
            print("No tasks available.")
            continue

        time_left = get_int("Minutes you can study today: ")

        tasks.sort(key=lambda x: (-int(x[4]), datetime.strptime(x[2], "%m/%d/%Y")))
        updated = []

        print("\nToday's Study Plan")
        print("-" * 30)

        for t in tasks:
            subject, name, due, comp, priority = t
            comp = int(comp)

            if time_left > 0:
                studied = min(comp, time_left)
                time_left -= studied
                comp -= studied
                print(f"{subject} — {name}: studied {studied} min (remaining {comp})")

            if comp > 0:
                updated.append([subject, name, due, str(comp), priority])

        save_tasks(updated)
        print("Progress saved!")

    else:
        print("Invalid choice.")

    if input("\nReturn to menu? (y/n): ").lower() != "y":
        print("Good luck studying 📚")
        break
