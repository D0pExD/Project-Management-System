import mysql.connector
from datetime import datetime

###############################################################################
#                           ANSI Color Codes                                  #
###############################################################################
# You can adjust these as desired to get different colors or effects.
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[1;32m"
CYAN = "\033[1;36m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
YELLOW = "\033[1;33m"

###############################################################################
#                           Database Connection                               #
###############################################################################
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL root password
        database="freelancer_db"
    )

###############################################################################
#                           Projects CRUD                                     #
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
    print(f"\n{GREEN}Project added successfully!{RESET}")
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
    print(f"\n{BOLD}--- Projects ---{RESET}")
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
    print(f"\n{BOLD}--- Search Results ---{RESET}")
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

    print(f"\n{GREEN}Project updated successfully!{RESET}")
    conn.close()

def delete_project(project_id):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "DELETE FROM projects WHERE project_id = %s"
    cursor.execute(sql, (project_id,))
    conn.commit()
    print(f"\n{GREEN}Project deleted successfully!{RESET}")
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
    print(f"\n{GREEN}Project archived successfully!{RESET}")
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
#                           Task Management                                   #
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
    
    print(f"\n{GREEN}Task added successfully!{RESET}")
    conn.close()

def view_tasks(project_id):
    conn = connect_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM tasks WHERE project_id = %s"
    cursor.execute(sql, (project_id,))
    tasks = cursor.fetchall()
    print(f"\n{BOLD}--- Tasks for Project ID {project_id} ---{RESET}")
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
    
    print(f"\n{GREEN}Task updated successfully!{RESET}")
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
        
    print(f"\n{GREEN}Task deleted successfully!{RESET}")
    conn.close()

###############################################################################
#                           Project Logs                                      #
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
    print(f"\n{BOLD}--- Logs for Project ID {project_id} ---{RESET}")
    for log in logs:
        print(log)
    conn.close()

###############################################################################
#                           Reporting                                         #
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

    print(f"\n{BOLD}--- Project Summary Report ---{RESET}")
    for p in projects:
        (p_id, name, client_name, status, payment, deadline, progress,
         priority, team_members, client_email, client_phone,
         payment_status, completion_date, archived) = p
        print(
            f"\n{BOLD}Project ID:{RESET} {p_id}\n"
            f"{BOLD}Name:{RESET} {name}\n"
            f"{BOLD}Client:{RESET} {client_name}\n"
            f"{BOLD}Status:{RESET} {status}\n"
            f"{BOLD}Payment:{RESET} {payment}\n"
            f"{BOLD}Deadline:{RESET} {deadline}\n"
            f"{BOLD}Progress:{RESET} {progress}%\n"
            f"{BOLD}Priority:{RESET} {priority}\n"
            f"{BOLD}Team:{RESET} {team_members}\n"
            f"{BOLD}Client Email:{RESET} {client_email}\n"
            f"{BOLD}Client Phone:{RESET} {client_phone}\n"
            f"{BOLD}Payment Status:{RESET} {payment_status}\n"
            f"{BOLD}Completion Date:{RESET} {completion_date}\n"
            f"{BOLD}Archived:{RESET} {archived}"
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

    print(f"\n{GREEN}Projects exported to {filename} successfully!{RESET}")
    conn.close()

###############################################################################
#                           Menus                                             #
###############################################################################
def show_main_menu():
    """
    Display a visually appealing main menu with colors and ASCII formatting.
    """
    print(f"\n{BOLD}{GREEN}{'='*70}{RESET}")
    print(f"{BOLD}{GREEN}  F R E E L A N C E R   P R O J E C T   M G M T   BY   RAM CHIMNANI {RESET}".center(50))
    print(f"{BOLD}{GREEN}{'='*70}{RESET}")
    print(f"{CYAN} 1.{RESET}  Add Project")
    print(f"{CYAN} 2.{RESET}  View Projects (Active Only)")
    print(f"{CYAN} 3.{RESET}  Update Project")
    print(f"{CYAN} 4.{RESET}  Archive Project")
    print(f"{CYAN} 5.{RESET}  Delete Project")
    print(f"{CYAN} 6.{RESET}  Search Projects")
    print(f"{CYAN} 7.{RESET}  Mark Project Completed")
    print(f"{CYAN} 8.{RESET}  Project Tasks Menu")
    print(f"{CYAN} 9.{RESET}  View Project Logs")
    print(f"{CYAN}10.{RESET} Generate Report")
    print(f"{CYAN}11.{RESET} Export Projects to CSV")
    print(f"{CYAN}12.{RESET} View Archived Projects")
    print(f"{CYAN}13.{RESET} Exit")

def main_menu():
    """
    The main loop for the program, calling show_main_menu() for a nicer look.
    """
    while True:
        show_main_menu()
        choice = input(f"{BOLD}Enter your choice:{RESET} ")

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
            print(f"\n{BOLD}--- Archived Projects ---{RESET}")
            view_projects(show_archived=True)

        elif choice == '13':
            print(f"{YELLOW}Exiting... Goodbye!{RESET}")
            break

        else:
            print(f"{MAGENTA}Invalid choice. Please try again.{RESET}")

def task_menu():
    """
    Sub-menu for managing tasks. We can also apply a bit of styling here.
    """
    while True:
        print(f"\n{BLUE}{'='*10} Tasks Menu {'='*10}{RESET}")
        print(f"{CYAN}1.{RESET} Add Task")
        print(f"{CYAN}2.{RESET} View Tasks for a Project")
        print(f"{CYAN}3.{RESET} Update Task")
        print(f"{CYAN}4.{RESET} Delete Task")
        print(f"{CYAN}5.{RESET} Return to Main Menu")

        task_choice = input(f"{BOLD}Enter your choice:{RESET} ")

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
            new_assigned = input("New assigned to: ")
            new_due = input("New due date (YYYY-MM-DD): ")
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
            print(f"{MAGENTA}Invalid choice. Please try again.{RESET}")

if __name__ == "__main__":
    main_menu()
