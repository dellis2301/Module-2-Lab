# Author: Derrick Ellis
# File Name: student_gpa_checker.py
# Description: This program accepts student names and GPAs, then determines
#              if they qualify for the Dean's List (GPA ≥ 3.5) or the Honor Roll (GPA ≥ 3.25).
#              The program stops when the user enters 'ZZZ' as the last name.

while True:
    # Ask for the student's last name
    last_name = input("Enter student's last name (or 'ZZZ' to quit): ")
    
    # Quit if the last name is 'ZZZ'
    if last_name.upper() == 'ZZZ':
        print("\nExiting program. All records processed.")
        break

    # Ask for the student's first name
    first_name = input("Enter student's first name: ")

    # Ask for the student's GPA
    try:
        gpa = float(input("Enter student's GPA: "))
    except ValueError:
        print("Invalid input. GPA must be a number. Please try again.\n")
        continue

    # Check for Dean's List and Honor Roll
    if gpa >= 3.5:
        print(f"{first_name} {last_name} has made the Dean's List!\n")
    elif gpa >= 3.25:
        print(f"{first_name} {last_name} has made the Honor Roll!\n")
    else:
        print(f"{first_name} {last_name} does not qualify for Dean's List or Honor Roll.\n")
