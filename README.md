# python-capstone-project
Python-based telehealth appointment, triage, and follow-up system

## Project Description

This project is a Python-based telehealth management system designed to support remote healthcare services by handling patient registration, appointment scheduling, symptom triage, and automated follow-ups. It focuses on backend logic and workflow automation commonly required in telemedicine settings.

## Problem solved

Missed appointments, poor follow-up, and inefficient triage are common challenges in telehealth services. This project provides a lightweight digital solution that helps clinics manage telehealth appointments, guide patients through symptom-based triage, and automate reminders and follow-ups to improve continuity of care and patient engagement.
The system is built to be simple, modular, and extensible, making it suitable for small clinics or pilot telehealth programs.

##  Project Objectives
- Project Objectives
- Maintain organized and confidential patient records
- Schedule and monitor telehealth consultations
- Perform basic symptom-based triage to support clinical decision-making
- Send appointment reminders and follow-up notifications to patients
- Demonstrate structured program design using object-oriented principles

## Features
- Patient registration and record management
- Telehealth appointment scheduling and monitoring
- Appointment status tracking (Scheduled, Completed, Missed)
- Rule-based symptom triage with severity indication
- Automated appointment reminders and follow-up notification
- Simple command-line interface (CLI) for ease of use

##  Technologies Used
- Python
- SQLite (for data storage)
- Object-Oriented Programming (OOP)
- Optional APIs (Twilio / Email – simulated if not configured)

##  Project Structure
telehealth-system/
│
├── models/
│   ├── patient.py
│   ├── appointment.py
│
├── services/
│   ├── triage.py
│   ├── notifications.py
│
├── database.py
├── main.py
├── README.md
└── requirements.txt

## Installation 
git clone https://github.com/wambuiimaina/python-capstone-project.git
cd python-capstone-project
pip install -r requirements.txt
python main.py

