# 📅 Smart Appointment Management System

A Django-based appointment management system for managing doctors, patients, and appointment scheduling.

## 📌 Overview

The **Smart Appointment Management System** is a web-based application developed using Django. It provides separate functionality for patients, doctors, and administrators to manage appointments efficiently.

The system includes appointment booking, doctor availability, appointment status management, and automatic generation of available appointment slots.

## ✨ Features

### 👤 Patient

* Patient registration and login
* View available doctors
* Book appointments
* View appointments
* Cancel appointments
* Reschedule appointments

### 👨‍⚕️ Doctor

* Doctor registration and login
* Doctor dashboard
* View assigned appointments
* Update appointment status
* View patient information

### 🔐 Administrator

* Manage doctors and patients
* Manage appointments
* Manage users and system data through the Django admin panel

## 🧠 Appointment Scheduling Algorithm

The system uses a **slot-generation and conflict-checking algorithm** for appointment scheduling.

The algorithm:

1. Reads the doctor's working hours.
2. Generates appointment slots at **30-minute intervals**.
3. Checks existing appointments for the selected doctor and date.
4. Removes slots that are already booked with a **Pending** or **Confirmed** appointment.
5. Displays the remaining available slots to the patient.

This helps prevent two appointments from being assigned to the same doctor at the same time.

## 🛠️ Technologies Used

* **Python 3**
* **Django**
* **HTML**
* **CSS**
* **JavaScript**
* **Bootstrap**
* **SQLite**
* **Git & GitHub**
* **VS Code**

## 📂 Project Structure

```text
smart-appointment-management-system/
│
├── accounts/
├── appointments/
├── doctors/
├── patients/
├── smart_appointment_management_system/
├── templates/
├── static/
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## 🚀 Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/WAIBA-33/smart-appointment-management-system.git
```

### 2. Open the project directory

```bash
cd smart-appointment-management-system
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## 🎓 Academic Project

This project was developed as a **BCA final-year project** using Python and Django, with a focus on role-based appointment management and automated appointment slot generation.
