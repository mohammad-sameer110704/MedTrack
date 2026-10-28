-- Create database
CREATE DATABASE IF NOT EXISTS medtrack;
USE medtrack;

-- Doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phno VARCHAR(20) UNIQUE NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    phno VARCHAR(20) UNIQUE NOT NULL,
    adhaar VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Appointments table
CREATE TABLE IF NOT EXISTS appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    patient_name VARCHAR(100) NOT NULL,
    patient_age INT NOT NULL,
    patient_phno VARCHAR(20) NOT NULL,
    symptoms TEXT NOT NULL,
    appointment_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Prescriptions table
CREATE TABLE IF NOT EXISTS prescriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT NOT NULL,
    doctor_id INT NOT NULL,
    patient_id INT NOT NULL,
    prescription_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id),
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
