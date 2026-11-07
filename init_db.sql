-- SQL Script to Initialize the MySQL Database
-- You can run this in MySQL Workbench, phpMyAdmin, or mysql CLI:
-- mysql -u root -p < init_db.sql

CREATE DATABASE IF NOT EXISTS food_traceability_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE food_traceability_db;

-- Show status
SELECT 'Database food_traceability_db created or already exists' AS Status;

