CREATE DATABASE IF NOT EXISTS user_service_db;
USE user_service_db;

CREATE TABLE IF NOT EXISTS location (
    id INT PRIMARY KEY AUTO_INCREMENT,
    postal_code VARCHAR(45),
    city VARCHAR(45),
    country VARCHAR(45)
);

CREATE TABLE IF NOT EXISTS user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(45),
    last_name VARCHAR(45),
    email VARCHAR(45),
    oauth_id VARCHAR(45),
    location_id INT,
    FOREIGN KEY (location_id) REFERENCES location(id)
);

CREATE TABLE IF NOT EXISTS favorite_companies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS reservations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reservation_code VARCHAR(45),
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id)
);
