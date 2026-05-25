import streamlit as st
import requests
from api_service import *
from datetime import datetime

#config 
st.set_page_config(page_title="Task Manager Pro", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose App Mode", ["Task Manager", "Student Registration"])

if app_mode == "Task Manager":
    # --- EXISTING TASK MANAGER CODE ---
    #initialization 
    if "add_desc" not in st.session_state:
        st.session_state.add_desc = ""

    if "add_priority" not in st.session_state:
        st.session_state.add_priority = "low"
        

    if "add_due_date" not in st.session_state:
        st.session_state.add_due_date = datetime.today()

    if "reset_from" not in st.session_state:
        st.session_state.reset_from = False

    #RESET fields after ading a task 

    if st.session_state.reset_from:
        st.session_state.add_Title = ""
        st.session_state.add_desc = ""
        st.session_state.add_priority = "low"
        st.session_state.add_due_date = datetime.today()
        st.session_state.reset_from =False

    #HEADER 
    st.title("MY Task Manager")

    #ADD TASKS
    st.subheader("Add tasks")

    with st.form("add_task_from"):
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Title", key="add_Title")

        with col2: 
            description = st.text_input("Description", key="add_desc")

        priority = st.selectbox("priority",["low","medium","high"], key = "add_priority")

        due_date = st.date_input("Due_date", key = "add_due_date")

        submitted = st.form_submit_button("Add task")

        if submitted:
            if title.strip() :
                add_task(title,description,priority,str(due_date))
                st.session_state.reset_from = True 
                st.success("task added successfully")
                st.rerun()
            else:
                st.error("title is required")
    st.divider()


    #SEARCH tasks
    search_query = st.text_input("search tasks",placeholder="type to search any task with its tittle ...",
                                 key = "search_input")

    #FETCH all TASKS
    if search_query:
        tasks = search_tasks(search_query)
    else:
        tasks = gettasks()
    st.divider()

    #show tasks list
    st.subheader("your tasks")

    if not tasks:
        st.info("no tasks found")

    PRIORITY_LABELS = {
        "high":"High",
        "medium":"Medium",
        "low":"Low"
    }

    for task in tasks:
        with st.container():
            col1, col2, col3, col4 = st.columns([5,2,2,1])
            with col1:
                st.markdown(f"**{task['title']}**")
                st.caption(task['description'])
            with col2:
                st.write(task['due_date'])
            with col3:
                st.markdown(f"**{PRIORITY_LABELS.get(task['priority'],task['priority'])}**")
            with col4:
                if st.button("Edit",key = f"edit_{task['id']}"):
                    st.session_state.edit_task= task
                if st.button("delete",key=f"del_{task['id']}"):
                    delete_task(task['id'])
                    st.success("task deleted successfully")
                    st.rerun()
    st.divider()

    #EDITE TASK SECTION
    if "edit_task" in st.session_state:
        task = st.session_state.edit_task
        st.subheader("Edit Task")

        with st.form("edit_task_form"):
            new_title = st.text_input("Title", value=task['title'], key="edit_title")
            new_sesc = st.text_input("Description", value=task['description'], key="edit_desc")
            new_priority = st.selectbox("Priority", ["low", "medium", "high"], index=["low","medium","high"].index(task['priority']), key="edit_priority")
            default_date = datetime.strptime(task['due_date'], "%Y-%m-%d")

            col1, col2 = st.columns(2)
            with col1:
                save = st.form_submit_button("save changes")
            with col2:
                cancel = st.form_submit_button("cancel")

            if save:
                update_task(task['id'], new_title, new_sesc, new_priority, str(default_date),task['completed'])
                del st.session_state.edit_task
                st.success("task updated successfully")
                st.rerun()
            if cancel:
                del st.session_state.edit_task
                st.info("edit cancelled")
                st.rerun()

elif app_mode == "Student Registration":
    # --- NEW STUDENT REGISTRATION CODE ---
    st.title("Student Registration Form")
    st.write("Enter student details below to save them to the MySQL database.")

    with st.form("student_form"):
        student_name = st.text_input("Student Name")
        student_age = st.number_input("Student Age", min_value=1, max_value=150, step=1)
        student_standard = st.text_input("Student Standard/Class")
        
        submit_student = st.form_submit_button("Submit")

        if submit_student:
            if student_name.strip() and student_standard.strip():
                # Prepare data payload for FastAPI backend
                payload = {
                    "studentName": student_name,
                    "studentAge": int(student_age),
                    "studentstandard": student_standard
                }
                
                # Send POST request
                try:
                    response = requests.post("http://localhost:8000/students", json=payload)
                    if response.status_code == 200:
                        st.success(f"Student '{student_name}' registered successfully in MySQL!")
                    else:
                        st.error(f"Error registering student: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}. Is your FastAPI server running on port 8000?")
            else:
                st.warning("Please fill in all fields.")
