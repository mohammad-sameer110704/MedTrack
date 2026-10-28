from flask import Flask, request, render_template, redirect, url_for, session, flash
from datetime import datetime
import mysql.connector

app = Flask(__name__, static_folder='statick')
app.secret_key = 'medtrack_secret_key_123'

# Database Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "medtrack"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ==================== HOME ====================
@app.route('/')
def home():
    return render_template('home.html')

# ==================== DOCTOR SIGNUP ====================
@app.route('/doctor/signup', methods=['GET', 'POST'])
def doctor_signup():
    if request.method == 'GET':
        return render_template('doctor_signup.html')

    name = request.form.get('name')
    phno = request.form.get('phno')
    specialization = request.form.get('specialization')
    password = request.form.get('password')

    if not all([name, phno, specialization, password]):
        flash('All fields are required!', 'error')
        return redirect(url_for('doctor_signup'))

    conn = get_connection()
    cursor = conn.cursor()

    # Check if phone number already exists
    cursor.execute("SELECT id FROM doctors WHERE phno = %s", (phno,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        flash('Phone number already registered!', 'error')
        return redirect(url_for('doctor_signup'))

    # Insert doctor
    cursor.execute(
        "INSERT INTO doctors (name, phno, specialization, password) VALUES (%s, %s, %s, %s)",
        (name, phno, specialization, password)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash('Doctor registration successful! Please login.', 'success')
    return redirect(url_for('doctor_login'))

# ==================== DOCTOR LOGIN ====================
@app.route('/doctor/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'GET':
        return render_template('doctor_login.html')

    phno = request.form.get('phno')
    password = request.form.get('password')

    if not all([phno, password]):
        flash('Phone number and password are required!', 'error')
        return redirect(url_for('doctor_login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM doctors WHERE phno = %s AND password = %s", (phno, password))
    doctor = cursor.fetchone()
    cursor.close()
    conn.close()

    if doctor:
        session['user_id'] = doctor['id']
        session['user_name'] = doctor['name']
        session['user_role'] = 'doctor'
        flash('Login successful!', 'success')
        return redirect(url_for('doctor_dashboard'))
    else:
        flash('Invalid phone number or password!', 'error')
        return redirect(url_for('doctor_login'))

# ==================== DOCTOR DASHBOARD ====================
@app.route('/doctor/dashboard')
def doctor_dashboard():
    if 'user_role' not in session or session['user_role'] != 'doctor':
        flash('Please login first!', 'error')
        return redirect(url_for('doctor_login'))

    doctor_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get pending appointments
    cursor.execute("""
        SELECT a.*, p.name as patient_name, p.phno as patient_phno, p.age as patient_age
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.doctor_id = %s AND a.status = 'pending'
        ORDER BY a.appointment_date DESC
    """, (doctor_id,))
    pending_appointments = cursor.fetchall()

    # Get completed appointments
    cursor.execute("""
        SELECT a.*, p.name as patient_name, p.phno as patient_phno, p.age as patient_age
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.doctor_id = %s AND a.status = 'completed'
        ORDER BY a.appointment_date DESC
    """, (doctor_id,))
    completed_appointments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('doctor_dashboard.html',
                         pending_appointments=pending_appointments,
                         completed_appointments=completed_appointments)

# ==================== PATIENT SIGNUP ====================
@app.route('/patient/signup', methods=['GET', 'POST'])
def patient_signup():
    if request.method == 'GET':
        return render_template('patient_signup.html')

    name = request.form.get('name')
    age = request.form.get('age')
    phno = request.form.get('phno')
    adhaar = request.form.get('adhaar')
    password = request.form.get('password')

    if not all([name, age, phno, adhaar, password]):
        flash('All fields are required!', 'error')
        return redirect(url_for('patient_signup'))

    conn = get_connection()
    cursor = conn.cursor()

    # Check if phone number already exists
    cursor.execute("SELECT id FROM patients WHERE phno = %s", (phno,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        flash('Phone number already registered!', 'error')
        return redirect(url_for('patient_signup'))

    # Insert patient
    cursor.execute(
        "INSERT INTO patients (name, age, phno, adhaar, password) VALUES (%s, %s, %s, %s, %s)",
        (name, age, phno, adhaar, password)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash('Patient registration successful! Please login.', 'success')
    return redirect(url_for('patient_login'))

# ==================== PATIENT LOGIN ====================
@app.route('/patient/login', methods=['GET', 'POST'])
def patient_login():
    if request.method == 'GET':
        return render_template('patient_login.html')

    phno = request.form.get('phno')
    password = request.form.get('password')

    if not all([phno, password]):
        flash('Phone number and password are required!', 'error')
        return redirect(url_for('patient_login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM patients WHERE phno = %s AND password = %s", (phno, password))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if patient:
        session['user_id'] = patient['id']
        session['user_name'] = patient['name']
        session['user_role'] = 'patient'
        flash('Login successful!', 'success')
        return redirect(url_for('patient_dashboard'))
    else:
        flash('Invalid phone number or password!', 'error')
        return redirect(url_for('patient_login'))

# ==================== PATIENT DASHBOARD ====================
@app.route('/patient/dashboard')
def patient_dashboard():
    if 'user_role' not in session or session['user_role'] != 'patient':
        flash('Please login first!', 'error')
        return redirect(url_for('patient_login'))

    patient_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get patient's appointments with prescriptions
    cursor.execute("""
        SELECT a.*, d.name as doctor_name, d.specialization,
               (SELECT prescription_text FROM prescriptions WHERE appointment_id = a.id) as prescription
        FROM appointments a
        JOIN doctors d ON a.doctor_id = d.id
        WHERE a.patient_id = %s
        ORDER BY a.appointment_date DESC
    """, (patient_id,))
    appointments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('patient_dashboard.html', appointments=appointments)

# ==================== SEARCH DOCTORS ====================
@app.route('/search/doctors', methods=['GET', 'POST'])
def search_doctors():
    if 'user_role' not in session or session['user_role'] != 'patient':
        flash('Please login as patient first!', 'error')
        return redirect(url_for('patient_login'))

    if request.method == 'GET':
        specialization = request.args.get('specialization', '')
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if specialization:
            cursor.execute("SELECT * FROM doctors WHERE specialization = %s", (specialization,))
        else:
            cursor.execute("SELECT * FROM doctors")

        doctors = cursor.fetchall()

        # Get all specializations for filter dropdown
        cursor.execute("SELECT DISTINCT specialization FROM doctors")
        specializations = [row['specialization'] for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return render_template('search_doctors.html',
                             doctors=doctors,
                             specializations=specializations,
                             selected_specialization=specialization)

# ==================== BOOK APPOINTMENT ====================
@app.route('/book/appointment/<int:doctor_id>', methods=['GET', 'POST'])
def book_appointment(doctor_id):
    if 'user_role' not in session or session['user_role'] != 'patient':
        flash('Please login as patient first!', 'error')
        return redirect(url_for('patient_login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get doctor details
    cursor.execute("SELECT * FROM doctors WHERE id = %s", (doctor_id,))
    doctor = cursor.fetchone()

    if not doctor:
        cursor.close()
        conn.close()
        flash('Doctor not found!', 'error')
        return redirect(url_for('search_doctors'))

    if request.method == 'GET':
        cursor.close()
        conn.close()
        return render_template('book_appointment.html', doctor=doctor)

    # POST - Book appointment
    patient_id = session['user_id']
    patient_name = session['user_name']

    # Get patient details
    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()

    symptoms = request.form.get('symptoms')
    appointment_date = request.form.get('appointment_date')

    if not all([symptoms, appointment_date]):
        cursor.close()
        conn.close()
        flash('Symptoms and appointment date are required!', 'error')
        return redirect(url_for('book_appointment', doctor_id=doctor_id))

    # Insert appointment
    cursor.execute(
        """INSERT INTO appointments
           (patient_id, doctor_id, patient_name, patient_age, patient_phno, symptoms, appointment_date, status)
           VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')""",
        (patient_id, doctor_id, patient['name'], patient['age'], patient['phno'], symptoms, appointment_date)
    )
    conn.commit()
    cursor.close()
    conn.close()

    flash('Appointment booked successfully!', 'success')
    return redirect(url_for('patient_dashboard'))

# ==================== ADD PRESCRIPTION ====================
@app.route('/add/prescription/<int:appointment_id>', methods=['GET', 'POST'])
def add_prescription(appointment_id):
    if 'user_role' not in session or session['user_role'] != 'doctor':
        flash('Please login as doctor first!', 'error')
        return redirect(url_for('doctor_login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Get appointment details
    cursor.execute("""
        SELECT a.*, p.id as patient_id
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        WHERE a.id = %s AND a.doctor_id = %s
    """, (appointment_id, session['user_id']))
    appointment = cursor.fetchone()

    if not appointment:
        cursor.close()
        conn.close()
        flash('Appointment not found!', 'error')
        return redirect(url_for('doctor_dashboard'))

    if request.method == 'GET':
        cursor.close()
        conn.close()
        return render_template('add_prescription.html', appointment=appointment)

    # POST - Add prescription
    prescription_text = request.form.get('prescription')

    if not prescription_text:
        cursor.close()
        conn.close()
        flash('Prescription is required!', 'error')
        return redirect(url_for('add_prescription', appointment_id=appointment_id))

    # Insert prescription
    cursor.execute(
        """INSERT INTO prescriptions (appointment_id, doctor_id, patient_id, prescription_text)
           VALUES (%s, %s, %s, %s)""",
        (appointment_id, session['user_id'], appointment['patient_id'], prescription_text)
    )

    # Update appointment status to completed
    cursor.execute("UPDATE appointments SET status = 'completed' WHERE id = %s", (appointment_id,))

    conn.commit()
    cursor.close()
    conn.close()

    flash('Prescription added successfully!', 'success')
    return redirect(url_for('doctor_dashboard'))

# ==================== LOGOUT ====================
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
