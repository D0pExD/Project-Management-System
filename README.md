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
- [Documentation](#documentation)  
- [Credits](#credits)  

---

## Project Overview  

The FPMS is a simple project management system that allows freelancers to manage their projects efficiently. It provides functionalities for adding, viewing, updating, and deleting projects using a Python-based interface connected to a MySQL database.

You can explore the project’s web-based documentation at:  
👉 [FPMS Documentation](https://fpms-class12.vercel.app/)

---

## Features  

1. **Add Projects**: Create a new project with client details and payment amount.  
2. **View Projects**: View all the stored projects in the database.  
3. **Update Projects**: Modify the status and payment of an existing project.  
4. **Delete Projects**: Remove a project from the system.  
5. **Interactive Console**: Command-line interface for user interaction.  

---

## Requirements  

- Python 3.x  
- MySQL Server  
- Python Libraries:  
  - `mysql-connector-python` (install using `pip install mysql-connector-python`)  

---

## Setup and Installation  

1. **Install MySQL**:  
   Ensure MySQL is installed and running on your system. Create a database named `freelancer_db` and a table `projects` using the following SQL commands:  

   ```sql
   CREATE DATABASE freelancer_db;

   USE freelancer_db;

   CREATE TABLE projects (
       project_id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(100),
       client_name VARCHAR(100),
       status VARCHAR(50) DEFAULT 'Pending',
       payment FLOAT
   );
   ```

2. **Install Required Python Libraries**:  
   Run the following command to install the MySQL connector library:  
   ```bash
   pip install mysql-connector-python
   ```

3. **Clone or Download the Project**:  
   Save the Python code to a file, e.g., `fpms.py`.

4. **Configure MySQL Connection**:  
   Update the `connect_db` function in the code with your MySQL username, password, and host details:  
   ```python
   def connect_db():
       return mysql.connector.connect(
           host="localhost",
           user="root",
           password="",  # Replace with your MySQL password
           database="freelancer_db"
       )
   ```

---

## Usage Instructions  

1. Run the program:  
   ```bash
   python fpms.py
   ```

2. Use the console menu to interact with the system:  
   - Add a new project by entering the project name, client name, and payment amount.  
   - View all projects stored in the database.  
   - Update an existing project’s status and payment.  
   - Delete a project using its project ID.  

3. Exit the program by selecting the "Exit" option.

---

## Documentation  

For detailed documentation and features, visit the project’s web page:  
👉 [FPMS Documentation](https://fpms-class12.vercel.app/)  

---

## Credits  

This project was created by **Ram Chimnani** from **Small Wonder School** as part of the Class 12th Computer Science curriculum.  

For any queries or feedback, please feel free to reach out!  

---  

Enjoy managing your projects with FPMS! 🎉