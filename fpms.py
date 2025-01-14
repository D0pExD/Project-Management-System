import mysql.connector
from datetime import datetime

###############################################################################
#                        Database Connection                                  #
###############################################################################
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL root password
        database="freelancer_db"
    )

###############################################################################
#                         Project Management                                  #
###############################################################################
def add_project(name, client_name, payment, deadline, progress, priority, 
                team_members, client_email, client_phone, payment_status):
    conn = connect_db()
    cursor = conn.cursor()
    sql = """
    INSERT INTO projects
    (name, client_name, payment, deadline, progress, priority,
     team_members, client_email, client_phone, payment_status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (name, client_name, payment, deadline, progress, priority, 
              team_members, client_email, client_phone, payment_status)
    cursor.execute(sql, values)
    conn.commit()
    print("\nProject added successfully!")
    conn.close()

def view_projects(show_archived=False):
    """
    If show_archived = False, hides archived projects.
    """
    conn = connect_db()
    cursor = conn.cursor()
    if show_archived:
        sql = "SELECT * FROM projects"
    else:
        sql = "SELECT * FROM projects WHERE archived = 0"
    cursor.execute(sql)
    projects = cursor.fetchall()
    print("\n--- Projects ---")
    for project in projects:
        print(project)
    conn.close()

def search_projects(query):
    """
    Search projects by matching client name, status, payment_status, etc.
    """
    conn = connect_db()
    cursor = conn.cursor()
    # Searching multiple columns using OR
    sql = """
    SELECT * FROM projects
    WHERE archived = 0
      AND (
          client_name LIKE %s OR
          status LIKE %s OR
          payment_status LIKE %s
      )
    """
    wildcard = f"%{query}%"
    cursor.execute(sql, (wildcard, wildcard, wildcard))
    projects = cursor.fetchall()
    print("\n--- Search Results ---")
    for project in projects:
        print(project)
    conn.close()

def update_project(project_id, **kwargs):
    """
    Update various fields of a project dynamically using **kwargs.
    Possible fields: status, payment, progress, deadline, priority,
                     team_members, payment_status, completion_date.
    """
    if not kwargs:
        print("No fields provided to update.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    set_clauses = []
    values = []

    for field, value in kwargs.items():
        set_clauses.append(f"{field} = %s")
        values.append(value)

    set_statement = ", ".join(set_clauses)
    sql = f"UPDATE projects SET {set_statement} WHERE project_id = %s"
    values.append(project_id)

    cursor.execute(sql, tuple(values))
    conn.commit()

    # Log the update in project_logs
    log_message = f"Updated fields: {kwargs}"
    add_project_log(project_id, log_message)

    print("\nProject updated successfully!")
    conn.close()

def delete_project(project_id):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "DELETE FROM projects WHERE project_id = %s"
    cursor.execute(sql, (project_id,))
    conn.commit()
    print("\nProject deleted successfully!")
    conn.close()

def archive_project(project_id):
    """
    Instead of deleting, mark a project as archived for record-keeping.
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = "UPDATE projects SET archived = 1 WHERE project_id = %s"
    cursor.execute(sql, (project_id,))
    conn.commit()

    add_project_log(project_id, "Archived project.")
    print("\nProject archived successfully!")
    conn.close()

def mark_project_completed(project_id):
    """
    Set project status to 'Completed', record completion_date as today,
    set progress to 100, and update payment_status if needed.
    """
    today = datetime.today().strftime('%Y-%m-%d')
    update_project(
        project_id,
        status="Completed",
        completion_date=today,
        progress=100,
        payment_status="Paid"
    )

###############################################################################
#                              Task Management                                #
###############################################################################
def add_task(project_id, task_name, description, assigned_to, due_date, priority):
    conn = connect_db()
    cursor = conn.cursor()
    sql = """
    INSERT INTO tasks (project_id, task_name, description, assigned_to, due_date, priority)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (project_id, task_name, description, assigned_to, due_date, priority)
    cursor.execute(sql, values)
    conn.commit()
    
    # Log the creation of a new task
    add_project_log(project_id, f"Task created: {task_name}")
    
    print("\nTask added successfully!")
    conn.close()

def view_tasks(project_id):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM tasks WHERE project_id = %s"
    cursor.execute(sql, (project_id,))
    tasks = cursor.fetchall()
    print(f"\n--- Tasks for Project ID {project_id} ---")
    for task in tasks:
        print(task)
    conn.close()

def update_task(task_id, **kwargs):
    """
    Update various fields of a task using **kwargs.
    Possible fields: task_name, description, assigned_to, due_date, status, priority
    """
    if not kwargs:
        print("No fields provided to update.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    set_clauses = []
    values = []

    for field, value in kwargs.items():
        set_clauses.append(f"{field} = %s")
        values.append(value)

    set_statement = ", ".join(set_clauses)
    sql = f"UPDATE tasks SET {set_statement} WHERE task_id = %s"
    values.append(task_id)

    cursor.execute(sql, tuple(values))
    conn.commit()

    # Fetch the project_id for logging
    cursor.execute("SELECT project_id FROM tasks WHERE task_id = %s", (task_id,))
    result = cursor.fetchone()
    if result:
        project_id = result[0]
        add_project_log(project_id, f"Updated task {task_id} fields: {kwargs}")
    
    print("\nTask updated successfully!")
    conn.close()

def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    # First, get project_id for logging
    cursor.execute("SELECT project_id FROM tasks WHERE task_id = %s", (task_id,))
    result = cursor.fetchone()
    if result:
        project_id = result[0]
    else:
        project_id = None

    # Delete the task
    sql = "DELETE FROM tasks WHERE task_id = %s"
    cursor.execute(sql, (task_id,))
    conn.commit()
    
    if project_id:
        add_project_log(project_id, f"Deleted task {task_id}")
        
    print("\nTask deleted successfully!")
    conn.close()

###############################################################################
#                             Project Logs                                    #
###############################################################################
def add_project_log(project_id, log_message):
    """
    Records any update/event in the project_logs table.
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = "INSERT INTO project_logs (project_id, log_message) VALUES (%s, %s)"
    cursor.execute(sql, (project_id, log_message))
    conn.commit()
    conn.close()

def view_project_logs(project_id):
    """
    View all logs for a given project.
    """
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM project_logs WHERE project_id = %s ORDER BY log_date DESC"
    cursor.execute(sql, (project_id,))
    logs = cursor.fetchall()
    print(f"\n--- Logs for Project ID {project_id} ---")
    for log in logs:
        print(log)
    conn.close()

###############################################################################
#                       Reporting and Advanced Features                       #
###############################################################################
def generate_report(all_projects=False):
    """
    Generates a summary report of all active or all projects.
    If all_projects=True, include archived; otherwise, exclude them.
    """
    conn = connect_db()
    cursor = conn.cursor()
    if all_projects:
        sql = "SELECT * FROM projects"
    else:
        sql = "SELECT * FROM projects WHERE archived = 0"
    cursor.execute(sql)
    projects = cursor.fetchall()

    print("\n--- Project Summary Report ---")
    for p in projects:
        (p_id, name, client_name, status, payment, deadline, progress,
         priority, team_members, client_email, client_phone,
         payment_status, completion_date, archived) = p
        print(
            f"\nProject ID: {p_id}\n"
            f"Name: {name}\n"
            f"Client: {client_name}\n"
            f"Status: {status}\n"
            f"Payment: {payment}\n"
            f"Deadline: {deadline}\n"
            f"Progress: {progress}%\n"
            f"Priority: {priority}\n"
            f"Team: {team_members}\n"
            f"Client Email: {client_email}\n"
            f"Client Phone: {client_phone}\n"
            f"Payment Status: {payment_status}\n"
            f"Completion Date: {completion_date}\n"
            f"Archived: {archived}"
        )
    conn.close()

def export_projects_to_csv(filename="projects_export.csv"):
    """
    Simple CSV export of project data to a local file.
    """
    import csv

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    # Retrieve column names
    column_names = [desc[0] for desc in cursor.description]

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(column_names)
        for row in projects:
            writer.writerow(row)

    print(f"\nProjects exported to {filename} successfully!")
    conn.close()

###############################################################################
#                               Main Menu                                     #
###############################################################################
def main_menu():
    while True:
        print("\n==============================")
        print("Freelancer Project Management")
        print("==============================")
        print("1.  Add Project")
        print("2.  View Projects (Active Only)")
        print("3.  Update Project")
        print("4.  Archive Project")
        print("5.  Delete Project")
        print("6.  Search Projects")
        print("7.  Mark Project Completed")
        print("8.  Project Tasks Menu")
        print("9.  View Project Logs")
        print("10. Generate Report")
        print("11. Export Projects to CSV")
        print("12. View Archived Projects")
        print("13. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter project name: ")
            client_name = input("Enter client name: ")
            payment = float(input("Enter payment amount: "))
            deadline = input("Enter project deadline (YYYY-MM-DD): ")
            progress = int(input("Enter project progress (0-100): "))
            priority = input("Enter project priority (Low, Medium, High): ")
            team_members = input("Enter team members (comma separated): ")
            client_email = input("Enter client email: ")
            client_phone = input("Enter client phone number: ")
            payment_status = input("Enter payment status (Pending, Partial, Paid, Overdue): ")
            add_project(name, client_name, payment, deadline, progress, priority, 
                        team_members, client_email, client_phone, payment_status)

        elif choice == '2':
            view_projects(show_archived=False)

        elif choice == '3':
            project_id = int(input("Enter project ID: "))
            # Let’s allow dynamic updates
            print("Enter new values (leave blank if no update):")
            new_status = input("New status: ")
            new_payment = input("New payment: ")
            new_progress = input("New progress (0-100): ")
            new_deadline = input("New deadline (YYYY-MM-DD): ")
            new_priority = input("New priority: ")
            new_team = input("New team members: ")
            new_payment_status = input("New payment status: ")
            new_completion_date = input("New completion date (YYYY-MM-DD): ")

            fields_to_update = {}
            if new_status.strip():
                fields_to_update['status'] = new_status
            if new_payment.strip():
                fields_to_update['payment'] = float(new_payment)
            if new_progress.strip():
                fields_to_update['progress'] = int(new_progress)
            if new_deadline.strip():
                fields_to_update['deadline'] = new_deadline
            if new_priority.strip():
                fields_to_update['priority'] = new_priority
            if new_team.strip():
                fields_to_update['team_members'] = new_team
            if new_payment_status.strip():
                fields_to_update['payment_status'] = new_payment_status
            if new_completion_date.strip():
                fields_to_update['completion_date'] = new_completion_date
            
            update_project(project_id, **fields_to_update)

        elif choice == '4':
            project_id = int(input("Enter project ID to archive: "))
            archive_project(project_id)

        elif choice == '5':
            project_id = int(input("Enter project ID to delete: "))
            delete_project(project_id)

        elif choice == '6':
            search_query = input("Enter search query (client name, status, etc.): ")
            search_projects(search_query)

        elif choice == '7':
            project_id = int(input("Enter project ID to mark completed: "))
            mark_project_completed(project_id)

        elif choice == '8':
            task_menu()

        elif choice == '9':
            project_id = int(input("Enter project ID to view logs: "))
            view_project_logs(project_id)

        elif choice == '10':
            all_proj = input("Include archived projects in report? (y/n): ").lower()
            generate_report(all_projects=(all_proj == 'y'))

        elif choice == '11':
            filename = input("Enter filename (default: projects_export.csv): ")
            if not filename.strip():
                filename = "projects_export.csv"
            export_projects_to_csv(filename)

        elif choice == '12':
            print("\n--- Archived Projects ---")
            view_projects(show_archived=True)

        elif choice == '13':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

###############################################################################
#                             Task Menu                                       #
###############################################################################
def task_menu():
    """
    Sub-menu for managing tasks.
    """
    while True:
        print("\n======== Tasks Menu ========")
        print("1. Add Task")
        print("2. View Tasks for a Project")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Return to Main Menu")
        task_choice = input("Enter your choice: ")

        if task_choice == '1':
            project_id = int(input("Enter project ID: "))
            task_name = input("Enter task name: ")
            description = input("Enter task description: ")
            assigned_to = input("Enter person assigned: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            priority = input("Enter task priority (Low, Medium, High): ")
            add_task(project_id, task_name, description, assigned_to, due_date, priority)

        elif task_choice == '2':
            project_id = int(input("Enter project ID: "))
            view_tasks(project_id)

        elif task_choice == '3':
            task_id = int(input("Enter task ID: "))
            print("Enter new values (leave blank if no update):")
            new_name = input("New task name: ")
            new_desc = input("New description: ")
            new_assigned = input("New assigned_to: ")
            new_due = input("New due_date (YYYY-MM-DD): ")
            new_status = input("New status (Pending, In Progress, Completed): ")
            new_priority = input("New priority (Low, Medium, High): ")

            fields_to_update = {}
            if new_name.strip():
                fields_to_update['task_name'] = new_name
            if new_desc.strip():
                fields_to_update['description'] = new_desc
            if new_assigned.strip():
                fields_to_update['assigned_to'] = new_assigned
            if new_due.strip():
                fields_to_update['due_date'] = new_due
            if new_status.strip():
                fields_to_update['status'] = new_status
            if new_priority.strip():
                fields_to_update['priority'] = new_priority

            update_task(task_id, **fields_to_update)

        elif task_choice == '4':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)

        elif task_choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")

###############################################################################
#                               Script Entry                                  #
###############################################################################
if __name__ == "__main__":
    main_menu()
