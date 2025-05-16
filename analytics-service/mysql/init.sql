CREATE DATABASE IF NOT EXISTS reservation_service_db;
USE reservation_service_db;

CREATE TABLE IF NOT EXISTS time (
    id INT PRIMARY KEY AUTO_INCREMENT,
    year VARCHAR(4),
    month VARCHAR(2),
    week VARCHAR(2),
    quarter VARCHAR(2),
    day_in_month VARCHAR(2),
    day_in_week VARCHAR(2),
    hour VARCHAR(2)
);

CREATE TABLE IF NOT EXISTS employee (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(45),
    last_name VARCHAR(45),
    position VARCHAR(45),
    employee_code VARCHAR(45),
    emso VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS location (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45),
    country VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS service (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45),
    price DECIMAL(10,2),
    valid_until DATE,
    service_code VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS payment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45),
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS cancellation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(45),
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(45),
    last_name VARCHAR(45),
    email VARCHAR(45),
    points INT
);

CREATE TABLE IF NOT EXISTS reservation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    payment_id INT,
    cancellation_id INT,
    time_id INT,
    user_id INT,
    employee_id INT,
    location_id INT,
    service_id INT,
    company_id INT,
    sms_sent BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (payment_id) REFERENCES payment(id),
    FOREIGN KEY (cancellation_id) REFERENCES cancellation(id),
    FOREIGN KEY (time_id) REFERENCES time(id),
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (location_id) REFERENCES location(id),
    FOREIGN KEY (service_id) REFERENCES service(id)
);
