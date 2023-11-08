import sqlite3
import csv
from random import randint

# Defining the variables & setting up DB
db_file_path = "StudentDB.db"
quit = True
connection = sqlite3.connect(db_file_path)
cursor = connection.cursor()
state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
advisorList = ["Rene German", "Elizabeth Stevens", "Erik Linstead", "Jon Humphreys", "Elia Eiroa Lledo"]

#Creating the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Student(
    StudentId INTEGER PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    GPA REAL,
    Major TEXT,
    FacultyAdvisor TEXT,
    Address TEXT,
    City TEXT,
    State TEXT,
    ZipCode TEXT,
    MobilePhoneNumber TEXT,
    isDeleted INTEGER
    );''')

# Function used to open up CSV files
def openFile():
    cursor.execute("SELECT COUNT(*) FROM Student")
    count = cursor.fetchone()[0]
    if count == 0:
        file_name = "students.csv"
        with open(file_name, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
        # Skip the header row
            next(csvreader)
            for row in csvreader:
                index = randint(0,4)
                advisor = advisorList[index]
                cursor.execute('''
                INSERT INTO Student('FirstName','LastName','GPA','Major','FacultyAdvisor','Address','City','State','ZipCode','MobilePhoneNumber','isDeleted')
                VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (row[0], row[1], row[8], row[7], advisor, row[2], row[3], row[4], row[5], row[6], 0))
        connection.commit()
    else:
        pass

# Function to print out the menu
def printMenu():
    menu = '''
    Please select the option you'd like by typing in that number:
    1. Print all entries in database
    2. Insert a new student into the database
    3. Update a student's information
    4. Remove a student from the database
    5. Search for a specific student
    6. Exit
    \n'''
    print(menu)

# Setting up the database initially
openFile()

#While loop for running the application
while quit:
    user = input(printMenu())
    #Option 1: Print out all students in DB
    if user == "1" or user == "1.":
        cursor.execute("SELECT * FROM Student")
        rows = cursor.fetchall()
        # Print the rows
        for row in rows:
            print(row)

    #Option 2: Add in new student into DB
    elif user == "2" or user == "2.": 
        #Check for first name (must be all letters)
        while True:
            first = input("Enter in the first name of the new student: \n")
            if first.isalpha():
                break
            else:
                print("Invalid first name, please enter in the student's first name using only letters")
        #Check for last name (must be all letters)
        while True:
            last = input("Enter in the last name of the new student: \n")
            if last.isalpha():
                break
            else:
                print("Invalid last name, please enter in the student's last name using only letters")
        #Check for GPA (must be float & between 0-5)
        while True:
            gpa = input("Enter in the gpa of the new student: \n")
            try:
                gpa = float(gpa)
                if gpa > 0 and gpa < 5:
                    break
                else:
                    print("Invalid gpa, please enter a gpa that is between 0 and 5")
                    continue
            except ValueError:
                print("Invalid gpa, please enter a gpa that is a number")
        #Check for major, must be either space or letters
        while True:
            major = input("Enter in the major of the student: \n")
            if all(char.isalpha() or char.isspace() for char in major):
                break
            else:
                print("Invalid major, please enter in the student's major using letters & spaces only")
        #Check for faculty advisor, must be either space or letters
        while True:
            FAdvisor = input("Enter in the name of the faculty advisor of the student: \n")
            if all(char.isalpha() or char.isspace() for char in FAdvisor):
                break
            else:
                print("Invalid faculty advisor, please enter in a valid name using only letters and spaces")
        #Checking for the address, address can use either digits, characters, or spaces
        while True:
            Address = input("Enter in the street address of the student: \n")
            if any(c.isalpha() or c.isdigit() or c.isspace() for c in Address):
                break
            else:
                print("Invalid address, please enter in a valid address using only letters, numbers, and spaces")
        #Checking for the city, city can use either spaces, characters, or digits
        while True:
            City = input("Enter the city that student lives in: \n")
            if any(c.isalpha() or c.isdigit() or c.isspace() for c in City):
                break
            else:
                print("Invalid city, please enter in a valid city using only letters, numbers, and spaces")
        #Check for state, the state must be one of the 50 states or US territories
        while True:
            State = input("Enter the state that the student lives in: \n")
            if any(c.isalpha() or c.isspace() for c in State) and State in state_names:
                break
            else:
                print("Invalid state, please enter in a valid state")
        #Check for zipcode, must be 5 digits 
        while True:
            ZipCode = input("Enter the zip code of the area that the student lives in: \n")
            if ZipCode.isdigit() and len(ZipCode) == 5:
                break
            else:
                print("Invalid Zip Code, please enter in a zipcode using only 5 digits")
        #Check for phone number, must be ten digits unless it has a +1 in the front or a extension using "x"
        while True:
            PhoneNum = input("Enter in the phone number of the student: \n")
            cleaned_phone = ''.join(filter(str.isdigit, PhoneNum))

            if cleaned_phone.startswith('1') and 'x' in PhoneNum.lower():
                if len(cleaned_phone) >= 11 and len(cleaned_phone) <= 16:
                    break
            elif cleaned_phone.startswith('1'):
                if len(cleaned_phone) == 11:
                    break
            elif 'x' in PhoneNum:
                parts = cleaned_phone.split('x')
                if len(parts) == 2 and len(parts[0]) == 10 and len(parts[1]) >= 3 and len(parts[1]) <= 5:
                    break
            elif len(cleaned_phone) == 10:
                break
            else:
                print("Invalid input. Please enter a valid phone number.")

        cursor.execute('''
            INSERT INTO Student('FirstName','LastName','GPA','Major','FacultyAdvisor','Address','City','State','ZipCode','MobilePhoneNumber','isDeleted')
            VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (first, last, gpa, major, FAdvisor, Address, City, State, ZipCode, PhoneNum, 0))
        connection.commit()
        print("Added in new Student into the database")
    #Option 3: Updating a student's info
    elif user == "3" or user == "3.": 
        while True:
            studentID = input("Please enter in the ID number of the student you'd like to update: \n")
            cursor.execute("SELECT studentID FROM Student WHERE StudentId = ?",(studentID,))
            result = cursor.fetchone()

            if result:
                break
            else:
                print("Student not found within database, please enter in a valid StudentID")

        while True:
            updateMenu = '''
            1. Update Student's Major
            2. Update Student's Faculty Advisor
            3. Update Student's Phone Number
            '''
            toUpdate = input(updateMenu)
            if toUpdate == "1" or toUpdate == "1.":
                while True:
                    newMajor = input("Enter in the student's new major: \n")
                    if all(char.isalpha() or char.isspace() for char in newMajor):
                        break
                    else:
                        print("Invalid major, please enter in the student's major using letters & spaces only")
                cursor.execute("UPDATE Student SET Major = ? WHERE StudentId = ?", (newMajor,studentID))
                connection.commit()
                break
            elif toUpdate == "2" or toUpdate == "2.":
                while True:
                    newFA = input("Enter in the student's new faculty advisor: \n")
                    if all(char.isalpha() or char.isspace() for char in newFA):
                        break
                    else:
                        print("Invalid faculty advisor, please enter in a valid name using only letters and spaces")
                cursor.execute("UPDATE Student SET FacultyAdvisor = ? WHERE StudentId = ?", (newFA,studentID))
                connection.commit()
                break
            elif toUpdate == "3" or toUpdate == "3.":
                while True:
                    newPN = input("Enter in the phone number of the student: \n")
                    cleaned_phone = ''.join(filter(str.isdigit, newPN))

                    if cleaned_phone.startswith('1') and 'x' in newPN.lower():
                        if len(cleaned_phone) >= 11 and len(cleaned_phone) <= 16:
                            break
                    elif cleaned_phone.startswith('1'):
                        if len(cleaned_phone) == 11:
                            break
                    elif 'x' in newPN:
                        parts = cleaned_phone.split('x')
                        if len(parts) == 2 and len(parts[0]) == 10 and len(parts[1]) >= 3 and len(parts[1]) <= 5:
                            break
                    elif len(cleaned_phone) == 10:
                        break
                    else:
                        print("Invalid input. Please enter a valid phone number.")
                cursor.execute("UPDATE Student SET MobilePhoneNumber = ? WHERE StudentId = ?", (newPN,studentID))
                connection.commit()
                break
            elif toUpdate == "0" or toUpdate == "0.":
                print("Exiting back to main menu")
                break
            else:
                print("Invalid Option. Please enter in one of the valid options or 0 to go back to main menu")
        print("Record Updated")

    #Option 4: Deleting a student from the DB (soft delete)
    elif user == "4" or user == "4.":
        while True:
            studentID = input("Please enter in the ID number of the student you'd like to delete: \n")
            cursor.execute("SELECT studentID FROM Student WHERE StudentId = ?",(studentID,))
            result = cursor.fetchone()

            if result:
                break
            else:
                print("Student not found within database, please enter in a valid StudentID")
        while True:
            response = input("Are you sure you'd like to delete a student? Y/N \n")
            if response == "Y" or response.lower() == "yes":
                cursor.execute("UPDATE Student SET isDeleted = ? WHERE StudentId = ?", (1, studentID))
                connection.commit()
                break
            elif response == "N" or response.lower() == "no":
                print("Okay then, I'll send you back to the main menu...")
                break
            else:
                print("I don't understand that. I'll ask again. \n")

    #Option 5, search the DB based on student's major, GPA, City, State, or Advisor
    elif user == "5" or user == "5.":
        while True:
            searchMenu = '''
            Please enter what attribute you'd like to search by:
            1. Major
            2. GPA
            3. City
            4. State
            5. Faculty Advisor
            '''
            response = input(searchMenu)
            if response == '1' or response == '1.':
                while True:
                    majorSearch = input("Please enter in the major you would like to search by: \n")
                    if all(char.isalpha() or char.isspace() for char in majorSearch):
                        break
                    else:
                        print("Invalid major, please enter in the student's major using letters & spaces only")
                cursor.execute("SELECT * FROM STUDENT WHERE Major = ?",(majorSearch,))
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                break

            elif response == '2' or response == '2.':
                while True:
                    GPASearch = input("Please enter in the GPA you would like to search by: \n")
                    try:
                        GPASearch = float(GPASearch)
                        break
                    except ValueError:
                        print("Invalid gpa, please enter a gpa that is a number")
                cursor.execute("SELECT * FROM STUDENT WHERE GPA = ?",(GPASearch,))
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                break

            elif response == '3' or response == '3.':
                while True:
                    CitySearch = input("Please enter in the city you would like to search by: \n")
                    if any(c.isalpha() or c.isdigit() or c.isspace() for c in CitySearch):
                        break
                    else:
                        print("Invalid city, please enter in a valid city using only letters, numbers, and spaces")
                cursor.execute("SELECT * FROM  Student WHERE City = ?",(CitySearch,))
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                break

            elif response == '4' or response == '4.':
                while True:
                    StateSearch = input("Please enter in the state you would like to search by: \n")
                    if any(c.isalpha() or c.isspace() for c in StateSearch)and State in state_names:
                        break
                    else:
                        print("Invalid state, please enter in a valid state using only letters and spaces")
                cursor.execute("SELECT * FROM  Student WHERE State = ?",(StateSearch,))
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                break

            elif response == '5' or response == '5.':
                while True:
                    FASearch = input("Please enter in the Faculty Advisor you would like to search by: \n")
                    if any(c.isalpha() or c.isspace() for c in FASearch):
                        break
                    else:
                        print("Invalid Faculty Advisor, please enter in a valid name using only letters and spaces")
                cursor.execute("SELECT * FROM  Student WHERE FacultyAdvisor = ?",(FASearch,))
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
                break

            else:
                print("Invalid Option. Please enter in a valid search option")
    #Option 6, Quitting the program
    elif user == "6" or user == "6.":
        print("Exiting Program")
        break

    else:
        print("Invalid Option, please choose a valid option")

connection.close()
