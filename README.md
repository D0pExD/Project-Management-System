

# Freelancer Project Management System (FPMS)

Welcome to the **Freelancer Project Management System (FPMS)**! This project is a Class 12th Computer Science project designed to demonstrate the practical implementation of database management using Python and MySQL.

---

**Made by**: **Ram Chimnani**  
**School**: **Small Wonder School**  

---

## Table of Contents  
- [Project Overview](#project-overview)  
- [Features](#features)  
- [Requirements](#requirements)  
- [Setup and Installation](#setup-and-installation)  
- [Usage Instructions](#usage-instructions)  
- [Credits](#credits)  

---

## Project Overview  

The **FPMS** is a comprehensive project management system that allows freelancers to manage their projects efficiently. It provides a **color-coded, user-friendly console interface** and a robust database schema that supports **tasks**, **project logs**, **archiving**, **searching**, and more. This system showcases advanced Python-MySQL integration techniques, suitable for a Class 12th Computer Science project.


---

## Features  

1. **Project Management**  
   - **Add, View, Update, and Delete Projects**  
   - Store details such as client name, payment, deadlines, progress, and priority  
   - **Archive** projects instead of deleting them to preserve records  
   - Mark projects as **Completed**, automatically setting progress to 100%  

2. **Tasks**  
   - Manage **tasks** for each project: add, update, and delete tasks  
   - Assign tasks to team members, set due dates, and track status  

3. **Project Logs**  
   - **Automatic Logging** of significant changes (e.g., updates, deletions, task creation)  
   - View the **history** of changes to each project for better accountability  

4. **Advanced Searching**  
   - Search for projects by **client name**, **status**, or **payment status**  
   - Display archived or active projects selectively  

5. **Color-Coded Console UI**  
   - A **visually appealing** menu with ANSI escape codes for color and styling  
   - User-friendly **sub-menus** (e.g., Task Menu) to keep navigation clear  

6. **Reporting and Export**  
   - Generate a **project summary report** with progress, priorities, and deadlines  
   - **Export projects** to CSV for further analysis or backup  

---

## Requirements  

- **Python 3.x**  
- **MySQL Server** (running locally or remotely)  
- **Python Libraries**:  
  - `mysql-connector-python` (install using `pip install mysql-connector-python`)  

---

## Setup and Installation  

1. **Install MySQL**  
   - Ensure MySQL is installed and running on your system.  

2. **Create Database and Tables**  
   - Create a database named `freelancer_db` and run the extended SQL schema (including `projects`, `tasks`, and `project_logs`).  
   - Below is an example of how you might create the tables:
     ```sql
     CREATE DATABASE freelancer_db;
     USE freelancer_db;

     CREATE TABLE projects (
       project_id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       client_name VARCHAR(255) NOT NULL,
       status VARCHAR(50) NOT NULL DEFAULT 'Pending',
       payment FLOAT NOT NULL DEFAULT 0.0,
       deadline DATE,
       progress INT DEFAULT 0,
       priority VARCHAR(50) DEFAULT 'Medium',
       team_members TEXT,
       client_email VARCHAR(255),
       client_phone VARCHAR(15),
       payment_status VARCHAR(50) DEFAULT 'Pending',
       completion_date DATE,
       archived TINYINT(1) DEFAULT 0
     );

     CREATE TABLE tasks (
       task_id INT AUTO_INCREMENT PRIMARY KEY,
       project_id INT,
       task_name VARCHAR(255) NOT NULL,
       description TEXT,
       assigned_to VARCHAR(255),
       due_date DATE,
       status VARCHAR(50) DEFAULT 'Pending',
       priority VARCHAR(50) DEFAULT 'Medium',
       FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
     );

     CREATE TABLE project_logs (
       log_id INT AUTO_INCREMENT PRIMARY KEY,
       project_id INT,
       log_message TEXT,
       log_date DATETIME DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
     );
     ```

3. **Install Required Python Libraries**  
   ```bash
   pip install mysql-connector-python
   ```

4. **Clone or Download This Project**  
   - Save the main Python code (e.g., `fpms.py`) into a folder.  

5. **Configure MySQL Connection**  
   - In `fpms.py`, update the `connect_db` function with your MySQL credentials:
     ```python
     def connect_db():
         return mysql.connector.connect(
             host="localhost",
             user="root",
             password="YOUR_PASSWORD_HERE",
             database="freelancer_db"
         )
     ```

---

## Usage Instructions  

1. **Run the Program**  
   ```bash
   python fpms.py
   ```

2. **Main Menu**  
   - The application presents a **colorful console menu** with options to manage projects and tasks.  
   - Use the **numeric input** to navigate through options such as:  
     - **Add Project**: Specify project name, client details, payment, etc.  
     - **View Projects**: Displays all active projects.  
     - **Update Project**: Dynamically update status, payment, progress, etc.  
     - **Archive Project**: Archive instead of deleting.  
     - **Search Projects**: Search by client name, status, or payment status.  
     - **Task Menu**: Manage project tasks in a separate sub-menu.  
     - **Logs**: View the change history for a specific project.  
     - **Generate Report**: Shows a summary of all projects (archived or active).  
     - **Export to CSV**: Export data for backup or external analysis.  
   - **Exit** to close the application.  

3. **Task Menu**  
   - **Add Task**: Create tasks for any project.  
   - **View Tasks**: List all tasks belonging to a specific project.  
   - **Update Task**: Change task name, description, due date, status, etc.  
   - **Delete Task**: Remove an existing task.  

---

## Credits  

This project was created by **Ram Chimnani** from **Small Wonder School** as part of the Class 12th Computer Science curriculum.  

For any queries or feedback, please feel free to reach out!  

---

Enjoy managing your freelance projects with FPMS! 🎉
