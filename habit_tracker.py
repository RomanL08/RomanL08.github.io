habits = []
completed = []

try:
    with open("habits.txt", "r") as file:
        for line in file:
            habits.append(line.strip())
except FileNotFoundError:
    pass

while True:
    print("\nHabit Tracker")
    print("1. Add Habit")
    print("2. View Habits")
    print("3. Complete Habit")
    print("4. Delete Habit")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        habit = input("Enter a habit: ")
        habits.append(habit)
        print("Habit added!")

    elif choice == "2":
        print("\nYour Habits:")

        if len(habits) == 0:
            print("No habits added yet.")
        else:
            for habit in habits:
                if habit in completed:
                    print("[x]", habit)
                else:
                    print("[ ]", habit)

    elif choice == "3":
        if len(habits) == 0:
            print("No habits to complete yet.")
        else:
            print("\nYour Habits:")
            for i, habit in enumerate(habits):
                print(f"{i + 1}. {habit}")

            number = int(input("Which habit did you complete? "))

            if number < 1 or number > len(habits):
                print("Invalid habit number.")
            else:
                completed.append(habits[number - 1])
                print("Habit completed!")

    elif choice == "4":
        if len(habits) == 0:
            print("No habits to delete.")
        else:
            print("\nYour Habits:")
            for i, habit in enumerate(habits):
                print(f"{i + 1}. {habit}")

            number = int(input("Which habit do you want to delete? "))

            if number < 1 or number > len(habits):
                print("Invalid habit number.")
            else:
                deleted_habit = habits.pop(number - 1)

                if deleted_habit in completed:
                    completed.remove(deleted_habit)

                    print("Habit deleted!")

    elif choice == "5":
        with open("habits.txt", "w") as file:
            for habit in habits:
                file.write(habit + "\n")

        print("Habits saved!")
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")