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
    archived TINYINT(1) DEFAULT 0  -- 0 = not archived, 1 = archived
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
    FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE
);


CREATE TABLE project_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    log_message TEXT,
    log_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (project_id) ON DELETE CASCADE
);
