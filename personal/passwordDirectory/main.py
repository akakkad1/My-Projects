import json
from prettytable import PrettyTable

data = json.load(open("data.json"))

while True:
    print("1. Add password")
    print("2. View all")
    print("3. Search")
    choice = input("Choose an option:  ")

    if choice == "1":
        website = input("Website: ")
        username = input("Username: ")
        password = input("Password: ")
        data[website] = {"username": username, "password": password}
        json.dump(data, open("data.json", "w"), indent=4)
        print("Saved.\n")
    elif choice == "2":
        table = PrettyTable(["\033[1mWebsite", "\033[1mUsername", "\033[1mPassword"])
        for site, info in data.items():
            table.add_row([site, info["username"], info["password"]])
        print()
        print(table)
        print()
    elif choice == "3":
        website = input("Website to search: ")
        if website in data:
            print(f"{data[website]['username']} : {data[website]['password']}\n")
        else:
            print("Not found.\n")
    else:
        print("Invalid.\n")
