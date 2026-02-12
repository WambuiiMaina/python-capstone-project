import sqlite3
from datetime import datetime
import streamlit as st


# Database initialization

def get_connection():
    return sqlite3.connect("telehealth_1.db")  

def init_db():
    conn = get_connection()
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER,
        phone TEXT NOT NULL,
        email TEXT UNIQUE
    )
    """)

    # Appointments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        date_time TEXT,
        status TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            ON DELETE RESTRICT
            ON UPDATE CASCADE
    )
    """)

    # Triage table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS triage (
        triage_id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        patient_id INTEGER,
        visit_date TEXT,
        bp_systolic INTEGER,
        bp_diastolic INTEGER,
        pulse INTEGER,
        weight REAL,
        height REAL,
        bmi REAL,
        rbs REAL,
        fbs REAL,
        symptoms TEXT,
        danger TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY(appointment_id) REFERENCES appointments(appointment_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
    """)

    # Consultation table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultation (
        consult_id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        patient_id INTEGER,
        triage_id INTEGER,
        diagnosis TEXT,
        notes TEXT,
        meds TEXT,
        plan TEXT,
        next_review TEXT,
        FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY(appointment_id) REFERENCES appointments(appointment_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        FOREIGN KEY(triage_id) REFERENCES triage(triage_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Patient Class

class Patient:
    def __init__(self, patient_id, first_name, last_name, age, phone, email):
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.phone = phone
        self.email = email

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (patient_id, first_name, last_name, age, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.patient_id, self.first_name, self.last_name, self.age, self.phone, self.email))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        rows = cursor.fetchall()
        conn.close()
        return rows

# Appointment Class

class Appointment:
    STATUS = ["Scheduled", "Arrived", "Triaged", "Completed", "Missed"]

    def __init__(self, appointment_id, patient_id, date_time, status="Scheduled"):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.date_time = date_time
        self.status = status

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO appointments (appointment_id, patient_id, date_time, status)
            VALUES (?, ?, ?, ?)
        """, (self.appointment_id, self.patient_id, self.date_time, self.status))
        conn.commit()
        conn.close()

    @staticmethod
    def update_status(appointment_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET status=? WHERE appointment_id=?", (status, appointment_id))
        conn.commit()
        conn.close()

    @staticmethod
    def all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments ORDER BY date_time DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def for_patient(patient_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments WHERE patient_id=? ORDER BY date_time DESC", (patient_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

# Triage Class
class Triage:
    def __init__(self, appointment_id, patient_id, bp_systolic, bp_diastolic, pulse,
                 weight, height, rbs, fbs, symptoms, danger):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.visit_date = str(datetime.now())
        self.bp_systolic = bp_systolic
        self.bp_diastolic = bp_diastolic
        self.pulse = pulse
        self.weight = weight
        self.height = height
        self.bmi = round(weight / ((height / 100) ** 2), 2) if height else 0
        self.rbs = rbs
        self.fbs = fbs
        self.symptoms = symptoms
        self.danger = danger

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO triage (appointment_id, patient_id, visit_date,
                                bp_systolic, bp_diastolic, pulse,
                                weight, height, bmi, rbs, fbs,
                                symptoms, danger)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.appointment_id, self.patient_id, self.visit_date,
              self.bp_systolic, self.bp_diastolic, self.pulse,
              self.weight, self.height, self.bmi, self.rbs, self.fbs,
              self.symptoms, self.danger))
        conn.commit()
        conn.close()
        Appointment.update_status(self.appointment_id, "Triaged")

    @staticmethod
    def for_appointment(appointment_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM triage WHERE appointment_id=?", (appointment_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

# Consultation Class

class Consultation:
    def __init__(self, appointment_id, patient_id, triage_id, diagnosis, notes, meds, plan, next_review):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.triage_id = triage_id
        self.diagnosis = diagnosis
        self.notes = notes
        self.meds = meds
        self.plan = plan
        self.next_review = next_review

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO consultation 
            (appointment_id, patient_id, triage_id, diagnosis, notes, meds, plan, next_review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.appointment_id,
            self.patient_id,
            self.triage_id,
            self.diagnosis,
            self.notes,
            self.meds,
            self.plan,
            self.next_review
        ))
        conn.commit()
        conn.close()

        Appointment.update_status(self.appointment_id, "Completed")

        if self.next_review:
            existing_appts = Appointment.all()
            new_id = max([a[0] for a in existing_appts] + [0]) + 1
            next_appt = Appointment(new_id, self.patient_id, self.next_review, "Scheduled")
            next_appt.save()

    @staticmethod
    def for_patient(patient_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM consultation
            WHERE patient_id=?
            ORDER BY next_review DESC
        """, (patient_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows

# Streamlit UI
st.title("🏥 Chronic Care System (HTN & Diabetes)")

menu = st.sidebar.selectbox(
    "Menu",
    ["Register Patient", "Appointments", "Triage", "Consultation", "Patient History"]
)

# 1. Register Patient

if menu == "Register Patient":
    st.subheader("New Patient Registration")
    
    first = st.text_input("First Name")
    last = st.text_input("Last Name")
    age = st.number_input("Age", 1, 120)
    phone = st.text_input("Phone")
    email = st.text_input("Email")

    if st.button("Save Patient"):
        patients = Patient.all()
        new_id = max([p[0] for p in patients] + [0]) + 1
        p = Patient(new_id, first, last, age, phone, email)
        p.save()
        st.success(f"Patient {first} {last} registered successfully!")

# 2. Schedule / View Appointments

elif menu == "Appointments":
    st.subheader("Schedule / View Appointments")
    
    patients = Patient.all()
    patient_map = {f"{p[0]} - {p[1]} {p[2]}": p[0] for p in patients}
    
    if patient_map:
        selected = st.selectbox("Select Patient", list(patient_map.keys()))
        date = st.date_input("Date")
        time = st.time_input("Time")
        if st.button("Schedule Appointment"):
            appointments = Appointment.all()
            new_id = max([a[0] for a in appointments] + [0]) + 1
            dt = f"{date} {time}"
            appt = Appointment(new_id, patient_map[selected], dt)
            appt.save()
            st.success("Appointment scheduled!")

        st.write("### All Appointments")
        for a in Appointment.all():
            st.write(f"ID: {a[0]} | Patient: {a[1]} | Date: {a[2]} | Status: {a[3]}")

    else:
        st.info("No patients available. Please register a patient first.")


# 3. Triage Entry
elif menu == "Triage":
    st.subheader("Patient Triage")
    
    appointments = Appointment.all()
    triage_appts = [a for a in appointments if a[3] in ["Scheduled", "Arrived"]]
    appt_map = {f"{a[0]} | Patient: {a[1]} | Date: {a[2]}": (a[0], a[1]) for a in triage_appts}
    
    if appt_map:
        selected = st.selectbox("Select Appointment", list(appt_map.keys()))
        aid, pid = appt_map[selected]

        bp_sys = st.number_input("Systolic BP")
        bp_dia = st.number_input("Diastolic BP")
        pulse = st.number_input("Pulse")
        weight = st.number_input("Weight (kg)")
        height = st.number_input("Height (cm)")
        st.write("BMI:", round(weight / ((height/100) ** 2), 2) if height else 0)
        rbs = st.number_input("RBS")
        fbs = st.number_input("FBS")
        symptoms = st.text_area("Symptoms")
        danger = st.text_area("Danger Signs")

        if st.button("Save Triage"):
            t = Triage(aid, pid, bp_sys, bp_dia, pulse, weight, height, rbs, fbs, symptoms, danger)
            t.save()
            st.success("Triage saved! Appointment status updated to Triaged.")

    else:
        st.info("No appointments ready for triage.")

# 4. Consultation Entry
elif menu == "Consultation":
    st.subheader("Consultation")
    
    appointments = Appointment.all()
    triaged_appts = [a for a in appointments if a[3] == "Triaged"]
    appt_map = {f"{a[0]} | Patient: {a[1]} | Date: {a[2]}": (a[0], a[1]) for a in triaged_appts}

    if appt_map:
        selected = st.selectbox("Select Triaged Appointment", list(appt_map.keys()))
        aid, pid = appt_map[selected]

        triage_records = Triage.for_appointment(aid)
        triage_map = {f"{t[0]} | {t[3]} / {t[4]} BP": t[0] for t in triage_records}
        triage_id = st.selectbox("Select Triage Record", list(triage_map.keys()))

        diagnosis = st.text_area("Diagnosis")
        notes = st.text_area("Notes")
        meds = st.text_area("Medications / Changes")
        plan = st.text_area("Plan")
        next_review = st.date_input("Next Review Date")

        if st.button("Save Consultation"):
            c = Consultation(aid, pid, triage_map[triage_id], diagnosis, notes, meds, plan, next_review)
            c.save()
            st.success("Consultation saved! Next appointment automatically created.")

    else:
        st.info("No appointments available for consultation.")

# 5. Patient History

elif menu == "Patient History":
    st.subheader("Patient History")

    patients = Patient.all()
    patient_map = {f"{p[0]} - {p[1]} {p[2]}": p[0] for p in patients}
    
    if patient_map:
        selected = st.selectbox("Select Patient", list(patient_map.keys()))
        pid = patient_map[selected]

        st.write("### Appointments")
        for a in Appointment.for_patient(pid):
            st.write(f"ID: {a[0]} | Date: {a[2]} | Status: {a[3]}")

        st.write("### Triage Records")
        for a in Appointment.for_patient(pid):
            triages = Triage.for_appointment(a[0])
            for t in triages:
                st.write(f"ID: {t[0]} | BP: {t[3]}/{t[4]} | BMI: {t[9]} | Symptoms: {t[11]} | Danger: {t[12]}")

        st.write("### Consultations")
        for c in Consultation.for_patient(pid):
            st.write(f"ID: {c[0]} | Diagnosis: {c[4]} | Meds: {c[6]} | Plan: {c[7]} | Next Review: {c[8]}")

    else:
        st.info("No patients available.")
