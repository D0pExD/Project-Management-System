CREATE DATABASE freelancer_db;

USE freelancer_db;

CREATE TABLE projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    payment FLOAT NOT NULL DEFAULT 0.0
);