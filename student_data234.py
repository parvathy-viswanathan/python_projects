import streamlit as st
import csv

file_path = r'C:\Users\HI\Desktop\student_data.csv'

# Load data from the CSV file into the students dictionary
def load_data_from_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        students = {}
        for row in reader:
            roll_no = row['roll_no']
            students[roll_no] = {'name': row['name'], 'marks': float(row['marks'])}
        st.session_state.students = students
    st.success("Data loaded successfully from CSV.")

# Initialize the students dictionary in session state
if 'students' not in st.session_state:
    st.session_state.students = {}
    # Load existing data from CSV when the app starts
    load_data_from_csv(file_path)

# Save the updated students dictionary back to the CSV file
def save_data_to_csv(file_path):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['roll_no', 'name', 'marks'])
        writer.writeheader()
        for roll_no, student in st.session_state.students.items():
            writer.writerow({'roll_no': roll_no, 'name': student['name'], 'marks': student['marks']})
    st.success("Data saved successfully to CSV.")

def add_student():
    name = st.text_input("Enter student name:")
    roll_no = st.text_input("Enter roll number:")
    marks = st.number_input("Enter marks:", min_value=0.0, max_value=100.0, step=0.1)
    if st.button("Add Student"):
        if roll_no and name:
            st.session_state.students[roll_no] = {'name': name, 'marks': marks}
            save_data_to_csv(file_path)  # Save data immediately after adding
            st.success("Student added and saved successfully!")
        else:
            st.warning("Please enter both roll number and name.")

def view_students():
    if not st.session_state.students:
        st.info("No students added yet.")
    else:
        st.write("### Student Details:")
        student_data = [
            {"Roll No": roll_no, "Name": student['name'], "Marks": student['marks']}
            for roll_no, student in st.session_state.students.items()
        ]
        st.table(student_data)

def search_student():
    roll_no = st.text_input("Enter roll number to search:")
    if st.button("Search"):
        if roll_no in st.session_state.students:
            st.write("### Student Details:")
            student = st.session_state.students[roll_no]
            st.write(f"Roll No: {roll_no} | Name: {student['name']} | Marks: {student['marks']}")
        else:
            st.warning("Student not found.")

def update_student():
    roll_no = st.text_input("Enter roll number to update:")
    if roll_no in st.session_state.students:
        new_name = st.text_input("Enter new name:", value=st.session_state.students[roll_no]['name'])
        new_marks = st.number_input("Enter new marks:", value=st.session_state.students[roll_no]['marks'], min_value=0.0, max_value=100.0, step=0.1)
        if st.button("Update Student"):
            st.session_state.students[roll_no]['name'] = new_name
            st.session_state.students[roll_no]['marks'] = new_marks
            save_data_to_csv(file_path)  # Save data immediately after updating
            st.success("Student updated and saved successfully!")
    else:
        st.warning("Student not found.")

def delete_student():
    roll_no = st.text_input("Enter roll number to delete:")
    if st.button("Delete Student"):
        if roll_no in st.session_state.students:
            del st.session_state.students[roll_no]
            save_data_to_csv(file_path)  # Save data immediately after deleting
            st.success("Student deleted and saved successfully!")
        else:
            st.warning("Student not found.")

# Main Streamlit interface
st.title("Student Management System")

if st.button("Load Data"):
    load_data_from_csv(file_path)

st.sidebar.title("Actions")
action = st.sidebar.radio("Choose an action:", ["Add Student", "View Students", "Search Student", "Update Student", "Delete Student", "Save and Exit"])

if action == "Add Student":
    add_student()
elif action == "View Students":
    view_students()
elif action == "Search Student":
    search_student()
elif action == "Update Student":
    update_student()
elif action == "Delete Student":
    delete_student()
elif action == "Save and Exit":
    save_data_to_csv(file_path)
    st.sidebar.success("Data saved and program exited.")