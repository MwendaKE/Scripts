# A class-based application that manages student records using MongoDB as the database backend.
# · The StudentManager class handles all database operations
# · It connects to MongoDB running on localhost:27017 (type "mongod" on terminal to start the server)
# · It uses a database named tumaini with a collection named students

from pymongo import MongoClient
import sys


class StudentManager:
    """A class to manage student records in a MongoDB database"""
    
    def __init__(self):
        """Initialize the database connection"""
        try:
            self.client = MongoClient('localhost', 27017)
            self.db = self.client.tumaini
            self.student_collection = self.db.students
            print("Database connection established successfully.")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)
    
    def add_student(self, name, adm, gender, yob, dorm):
        """Add a new student to the database"""
        # Check if student with this admission number already exists
        if self.student_collection.find_one({"adm": adm}):
            return False, f"Student with admission number {adm} already exists."
        
        # Create student data dictionary
        student_data = {
            "adm": adm,
            "name": name,
            "gender": gender,
            "yob": yob,
            "dorm": dorm
        }
        
        # Insert the student into the database
        result = self.student_collection.insert_one(student_data)
        
        if result.inserted_id:
            return True, f"Student {name} added successfully with admission number {adm}."
        else:
            return False, "Failed to add student."
    
    def find_student(self, adm):
        """Find a student by admission number"""
        student = self.student_collection.find_one({"adm": adm})
        return student
    
    def update_student(self, adm, name, gender, yob, dorm):
        """Update a student's information"""
        result = self.student_collection.update_one(
            {"adm": adm}, 
            {"$set": {"name": name, "gender": gender, "yob": yob, "dorm": dorm}}
        )
        
        if result.modified_count > 0:
            return True, "Student information updated successfully."
        else:
            return False, "No changes made or student not found."
    
    def delete_student(self, adm):
        """Delete a student from the database"""
        result = self.student_collection.delete_one({"adm": adm})
        
        if result.deleted_count > 0:
            return True, "Student deleted successfully."
        else:
            return False, "Student not found."
    
    def get_all_students(self):
        """Retrieve all students from the database"""
        return self.student_collection.find()
    
    def close_connection(self):
        """Close the database connection"""
        self.client.close()
        print("Database connection closed.")


class StudentManagementSystem:
    """A class to handle the user interface for student management"""
    
    def __init__(self):
        """Initialize the student manager"""
        self.manager = StudentManager()
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*40)
        print("STUDENT MANAGEMENT SYSTEM")
        print("="*40)
        print("1. Add Student")
        print("2. Find Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Display All Students")
        print("6. Exit")
        print("="*40)
    
    def add_student_ui(self):
        """User interface for adding a student"""
        print("\n--- Add New Student ---")
        
        # Get student details from user
        name = input("Enter student name: ").strip()
        adm = input("Enter admission number: ").strip()
        gender = input("Enter gender (M/F): ").strip().upper()
        yob = input("Enter year of birth (yyyy): ").strip()
        dorm = input("Enter dorm/hostel: ").strip()
        
        # Validate input
        if not all([name, adm, gender, yob, dorm]):
            print("Error: All fields are required!")
            return
        
        if gender not in ['M', 'F']:
            print("Error: Gender must be M or F!")
            return
        
        if len(yob) != 4 or not yob.isdigit():
            print("Error: Year of birth must be a 4-digit number!")
            return
        
        # Add student to database
        success, message = self.manager.add_student(name, adm, gender, yob, dorm)
        print(message)
    
    def find_student_ui(self):
        """User interface for finding a student"""
        print("\n--- Find Student ---")
        adm = input("Enter admission number to search: ").strip()
        
        if not adm:
            print("Error: Admission number is required!")
            return
        
        student = self.manager.find_student(adm)
        
        if student:
            print("\nStudent Found:")
            print("-" * 20)
            for key, value in student.items():
                if key != "_id":  # Skip MongoDB's internal ID
                    print(f"{key.capitalize()}: {value}")
        else:
            print(f"No student found with admission number {adm}")
    
    def update_student_ui(self):
        """User interface for updating a student"""
        print("\n--- Update Student ---")
        adm = input("Enter admission number to update: ").strip()
        
        if not adm:
            print("Error: Admission number is required!")
            return
        
        # First find the student
        student = self.manager.find_student(adm)
        
        if not student:
            print(f"No student found with admission number {adm}")
            return
        
        print(f"\nCurrent details for {student['name']}:")
        for key, value in student.items():
            if key != "_id":  # Skip MongoDB's internal ID
                print(f"{key.capitalize()}: {value}")
        
        print("\nEnter new details (press Enter to keep current value):")
        name = input(f"Name [{student['name']}]: ").strip() or student['name']
        gender = input(f"Gender (M/F) [{student['gender']}]: ").strip().upper() or student['gender']
        yob = input(f"Year of Birth [{student['yob']}]: ").strip() or student['yob']
        dorm = input(f"Dorm/Hostel [{student['dorm']}]: ").strip() or student['dorm']
        
        # Validate input
        if gender not in ['M', 'F']:
            print("Error: Gender must be M or F!")
            return
        
        if len(yob) != 4 or not yob.isdigit():
            print("Error: Year of birth must be a 4-digit number!")
            return
        
        # Update student
        success, message = self.manager.update_student(adm, name, gender, yob, dorm)
        print(message)
    
    def delete_student_ui(self):
        """User interface for deleting a student"""
        print("\n--- Delete Student ---")
        adm = input("Enter admission number to delete: ").strip()
        
        if not adm:
            print("Error: Admission number is required!")
            return
        
        # First find the student
        student = self.manager.find_student(adm)
        
        if not student:
            print(f"No student found with admission number {adm}")
            return
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete {student['name']}? (y/n): ").strip().lower()
        if confirm == 'y':
            success, message = self.manager.delete_student(adm)
            print(message)
        else:
            print("Deletion cancelled.")
    
    def display_all_students_ui(self):
        """User interface for displaying all students"""
        print("\n--- All Students ---")
        
        students = self.manager.get_all_students()
        count = 0
        
        for student in students:
            count += 1
            print(f"\nStudent #{count}:")
            print("-" * 15)
            for key, value in student.items():
                if key != "_id":  # Skip MongoDB's internal ID
                    print(f"{key.capitalize()}: {value}")
        
        if count == 0:
            print("No students found in the database.")
        else:
            print(f"\nTotal students: {count}")
    
    def run(self):
        """Main method to run the student management system"""
        print("Welcome to the Student Management System!")
        
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                self.add_student_ui()
            elif choice == "2":
                self.find_student_ui()
            elif choice == "3":
                self.update_student_ui()
            elif choice == "4":
                self.delete_student_ui()
            elif choice == "5":
                self.display_all_students_ui()
            elif choice == "6":
                print("Thank you for using the Student Management System!")
                self.manager.close_connection()
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
            
            input("\nPress Enter to continue...")


# Start the program
if __name__ == "__main__":
    system = StudentManagementSystem()
    system.run()