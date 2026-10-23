from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import qrcode
import io
import base64
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("attendance.db")

def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                register_number TEXT NOT NULL,
                course TEXT NOT NULL,
                attendance_date TEXT NOT NULL,
                attendance_time TEXT NOT NULL,
                UNIQUE(register_number, attendance_date)
            )
        """)

def make_qr_image(data):
    qr = qrcode.QRCode(box_size=8, border=3)
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

@app.route("/")
def index():
    qr_url = request.url_root.rstrip("/") + url_for("mark_attendance")
    qr_image = make_qr_image(qr_url)
    with get_db() as db:
        total = db.execute("SELECT COUNT(*) FROM attendance").fetchone()[0]
        today = datetime.now().strftime("%Y-%m-%d")
        today_total = db.execute(
            "SELECT COUNT(*) FROM attendance WHERE attendance_date = ?", (today,)
        ).fetchone()[0]
        recent = db.execute(
            "SELECT * FROM attendance ORDER BY id DESC LIMIT 8"
        ).fetchall()
    return render_template("index.html", qr_image=qr_image, total=total,
                           today_total=today_total, recent=recent, qr_url=qr_url)

@app.route("/mark", methods=["GET", "POST"])
def mark_attendance():
    if request.method == "POST":
        name = request.form.get("student_name", "").strip()
        register_number = request.form.get("register_number", "").strip().upper()
        course = request.form.get("course", "").strip()
        if not name or not register_number or not course:
            flash("Please complete all fields.", "error")
            return redirect(url_for("mark_attendance"))
        now = datetime.now()
        try:
            with get_db() as db:
                db.execute(
                    """INSERT INTO attendance
                    (student_name, register_number, course, attendance_date, attendance_time)
                    VALUES (?, ?, ?, ?, ?)""",
                    (name, register_number, course, now.strftime("%Y-%m-%d"),
                     now.strftime("%H:%M:%S"))
                )
            flash("Attendance marked successfully!", "success")
        except sqlite3.IntegrityError:
            flash("Attendance has already been marked for this register number today.", "error")
        return redirect(url_for("mark_attendance"))
    return render_template("mark.html")

@app.route("/attendance")
def attendance():
    search = request.args.get("search", "").strip()
    with get_db() as db:
        rows = db.execute(
            """SELECT * FROM attendance
            WHERE student_name LIKE ? OR register_number LIKE ? OR course LIKE ?
            ORDER BY attendance_date DESC, attendance_time DESC""",
            (f"%{search}%", f"%{search}%", f"%{search}%")
        ).fetchall()
    return render_template("attendance.html", rows=rows, search=search)

initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)