import os
import datetime

def calculate_days_to_goal(gp_data, goal):
    total_gp = sum(sum(data.values()) for data in gp_data.values())
    remaining_gp = goal - total_gp
    if remaining_gp <= 0:
        return 0
    else:
        # Calculate the total number of days with GP data
        days_with_data = len(gp_data)

        # Calculate the average GP earned per day, excluding the current day's GP data
        if days_with_data > 1:
            daily_gp = total_gp / (days_with_data - 1)
        else:
            daily_gp = total_gp

        days_to_goal = remaining_gp / daily_gp
        return int(days_to_goal)

def validate_gp_amount(amount_str):
    try:
        if amount_str[-1] == 'k':
            amount = float(amount_str[:-1]) * 1000
        elif amount_str[-1] == 'm':
            amount = float(amount_str[:-1]) * 1000000
        else:
            amount = float(amount_str)
        return amount
    except ValueError:
        print("Invalid GP amount. Please enter a valid number.")
        return None

def main():
    print("Welcome to the RuneScape GP Tracker!")

    # Prompt the user to choose whether to view a file, edit, enter data, or set a goal
    while True:
        choice = input("Enter '1' to view a file, '2' to enter new GP data, or '3' to exit: ")

        if choice == '1':
            # Prompt the user to enter the filename and check if it exists
            filename = input("Enter the filename to view: ")
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    print(file.read())
                break
            else:
                print("File not found. Please try again.")
        elif choice == '2':
            # Create an empty dictionary to store GP data for each date
            gp_data = {}

            # Prompt the user to enter data for each key
            while True:
                method = input("Enter the method you used to earn GP: ")
                amount_str = input("Enter the amount of GP you earned: ")
                amount = validate_gp_amount(amount_str)
                if amount is None:
                    continue

                # Prompt the user to enter the date and convert it to a datetime object
                date_str = input("Enter the date for this GP data (MM/DD/YYYY): ")
                try:
                    date = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
                except ValueError:
                    print("Invalid date format. Please enter the date in MM/DD/YYYY format.")
                    continue

                # Add the GP data to the dictionary for the corresponding date
                if date in gp_data:
                    gp_data[date].update({method: amount})
                else:
                    gp_data[date] = {method: amount}

                # Ask the user if they want to enter more GP data for the same date
                another_method = input("Enter another method for the same date? (y/n) ")
                if another_method.lower() == 'n':
                    break

            # Prompt the user to enter the date for the GP data
            date_str = input("Enter the date for this GP data (MM/DD/YYYY): ")
            try:
                date = datetime.datetime.strptime(date_str, "%m/%d/%Y").date()
            except ValueError:
                print("Invalid date format. Please enter the date in MM/DD/YYYY format.")
                continue

            # Add the GP data to the dictionary for the corresponding date
            if date in gp_data:
                gp_data[date].update(gp_data[date])
            else:
                if isinstance(gp_data[date], dict):
                    gp_data[date].update({method: amount})
                else:
                    gp_data[date] = {method: amount}

            # Prompt the user to save the GP data to a file
            filename = input("Enter the filename to save the GP data: ")

            # Print the GP data for each date and calculate the total
            print("Here's your GP tracker:")
            with open(filename, 'w') as file:
                # Write the GP data for to the file
                for date, data in gp_data.items():
                    total = sum(data.values())
                    print("Date:", date)
                    print(data)
                    print("Total GP earned:", total)

                    # Write the data as a string
                    file.write(f"Date: {date.strftime('%m/%d/%Y')}\n")
                    for method, amount in data.items():
                        file.write(f"{method}: {amount}\n")
                    file.write(f"Total GP earned: {total}\n\n")

            # Prompt the user if they want to set a GP goal
            set_goal = input("Do you want to set a GP goal? (y/n) ")
            if set_goal.lower() == 'y':
                goal_str = input("Enter your GP goal: ")
                goal = validate_gp_amount(goal_str)
                if goal is None:
                    continue

                total_gp = sum(sum(data.values()) for data in gp_data.values())
                days_to_goal = calculate_days_to_goal(gp_data, goal)
                if days_to_goal == 0:
                    print("Congratulations! You have reached your GP goal.")
                else:
                    print(f"You need to earn {goal - total_gp} GP more to reach your goal.")
                    print(f"At your current rate, you will reach your goal in {days_to_goal} days.")
            if set_goal.lower() == 'n':
                print("Thank you for using the RuneScape GP Tracker!")
                break
        elif choice == '3':
            print("Thank you for using the RuneScape GP Tracker!")
            break

if __name__ == "__main__":
    main()








