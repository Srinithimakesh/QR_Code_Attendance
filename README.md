# QR Code Student Attendance System

A beginner-friendly attendance management web application built with Python, Flask, SQLite, and QR codes.

## Features

- Generate a QR code that opens the attendance form.
- Submit student name, register number, and course from a phone or computer.
- Prevent duplicate attendance for the same register number on the same day.
- View attendance records and search by student name, register number, or course.
- See total attendance statistics on the dashboard.

## Requirements

- Python 3.10 or newer
- A web browser
- VS Code (recommended)

## Installation on Windows

1. Extract this ZIP file.
2. Open the extracted folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Install dependencies:

   ```bash
   py -m pip install -r requirements.txt
   ```

5. Start the application:

   ```bash
   py app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

## Scan the QR code using a phone

The QR code uses the computer's network address only if the app is opened through that address. For phone testing:

1. Connect the computer and phone to the same Wi-Fi network.
2. Find the computer's local IPv4 address by running `ipconfig` in Command Prompt.
3. Open `http://YOUR-COMPUTER-IP:5000` on the computer. Replace `YOUR-COMPUTER-IP` with the IPv4 address shown by `ipconfig`.
4. The dashboard QR code will now point to the same network address. Scan it using the phone camera.

If Windows Firewall asks for permission, allow Python on your private network.

## Project structure

```text
QR_Code_Attendance_System_English/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── mark.html
│   └── attendance.html
└── static/
    └── style.css
```

## Important notes

- The SQLite database file `attendance.db` is created automatically when the app starts.
- This is a student project suitable for local demonstrations. Add authentication, stronger secret management, and deployment security before using it for real institutional records.
- The QR code opens the attendance form; it does not itself verify a student's identity.
