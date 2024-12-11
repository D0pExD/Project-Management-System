import mysql.connector # Use 'pip install mysql-connector-python'

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL root password
        database="freelancer_db"
    )

# Add Project
def add_project(name, client_name, payment):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO projects (name, client_name, payment) VALUES (%s, %s, %s)"
    values = (name, client_name, payment)
    cursor.execute(query, values)
    conn.commit()
    print("Project added successfully!")
    conn.close()

# View All Projects
def view_projects():
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM projects"
    cursor.execute(query)
    projects = cursor.fetchall()
    print("Projects:")
    for project in projects:
        print(project)
    conn.close()

# Update Project
def update_project(project_id, status, payment):
    conn = connect_db()
    cursor = conn.cursor()
    query = "UPDATE projects SET status = %s, payment = %s WHERE project_id = %s"
    values = (status, payment, project_id)
    cursor.execute(query, values)
    conn.commit()
    print("Project updated successfully!")
    conn.close()

# Delete Project
def delete_project(project_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "DELETE FROM projects WHERE project_id = %s"
    values = (project_id,)
    cursor.execute(query, values)
    conn.commit()
    print("Project deleted successfully!")
    conn.close()

# Main Menu
def main_menu():
    while True:
        print("\nFreelancer Project Management")
        print("1. Add Project")
        print("2. View Projects")
        print("3. Update Project")
        print("4. Delete Project")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter project name: ")
            client_name = input("Enter client name: ")
            payment = float(input("Enter payment amount: "))
            add_project(name, client_name, payment)
        elif choice == '2':
            view_projects()
        elif choice == '3':
            project_id = int(input("Enter project ID: "))
            status = input("Enter project status: ")
            payment = float(input("Enter updated payment amount: "))
            update_project(project_id, status, payment)
        elif choice == '4':
            project_id = int(input("Enter project ID to delete: "))
            delete_project(project_id)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()