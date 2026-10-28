# MedTrack - Simple Medical Appointment System

A simple Flask-based medical appointment booking system with doctor and patient functionality.

## Features

1. **Doctor Signup** - Register with name, phone number, specialization, and password
2. **Doctor Login** - Login using phone number and password
3. **Patient Signup** - Register with name, age, phone number, Aadhaar, and password
4. **Patient Login** - Login using phone number and password
5. **Doctor Search** - Patients can search and filter doctors by specialization
6. **Appointment Booking** - Patients can book appointments with selected doctors
7. **Prescription System** - Doctors can add prescriptions, patients can view them in their profile
8. **Logout** - Both doctors and patients can logout

## Setup Instructions

### 1. Install Dependencies
```bash
pip install flask mysql-connector-python
```

### 2. Setup Database
- Make sure MySQL is running on your system
- Update the database credentials in `app.py` (lines 12-17) if needed:
  ```python
  DB_CONFIG = {
      "host": "localhost",
      "user": "root",
      "password": "root",  # Change to your MySQL password
      "database": "medtrack"
  }
  ```

### 3. Create Database and Tables
Run the SQL script:
```bash
mysql -u root -p < setup_database.sql
```

Or manually execute the SQL in `setup_database.sql` using MySQL Workbench or phpMyAdmin.

### 4. Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## How to Use

### For Doctors:
1. Go to home page and click "Doctor Signup"
2. Fill in your details (name, phone, specialization, password)
3. Login using your phone number and password
4. View pending appointments and add prescriptions
5. Logout when done

### For Patients:
1. Go to home page and click "Patient Signup"
2. Fill in your details (name, age, phone, Aadhaar, password)
3. Login using your phone number and password
4. Click "Search Doctors" to find doctors
5. Filter by specialization if needed
6. Click "Book Appointment" on a doctor
7. Enter appointment date and symptoms
8. View your appointments and prescriptions in the dashboard
9. Logout when done

## File Structure
```
MedTrack/
├── app.py                      # Main Flask application
├── setup_database.sql          # Database schema
├── template/                   # HTML templates
│   ├── home.html
│   ├── doctor_signup.html
│   ├── doctor_login.html
│   ├── doctor_dashboard.html
│   ├── patient_signup.html
│   ├── patient_login.html
│   ├── patient_dashboard.html
│   ├── search_doctors.html
│   ├── book_appointment.html
│   └── add_prescription.html
└── README.md
```

## Notes
- This is a simple project without password hashing (for learning purposes)
- In production, always hash passwords and use proper authentication
- The database name is "medtrack" - make sure it exists before running
