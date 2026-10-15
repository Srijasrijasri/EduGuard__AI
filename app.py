import os
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from ml.risk_predictor import StudentRiskPredictor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "database.db")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "student-risk-prediction-secret-key-2026")

# Initialize Risk Predictor
predictor = StudentRiskPredictor()

def get_db_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            attendance_percentage REAL NOT NULL,
            internal_marks REAL NOT NULL,
            assignment_score REAL NOT NULL,
            previous_semester_percentage REAL NOT NULL,
            study_hours_per_day REAL NOT NULL,
            backlogs INTEGER NOT NULL,
            extracurricular_participation TEXT NOT NULL,
            family_support TEXT NOT NULL,
            internet_access TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            confidence REAL NOT NULL,
            recommendations TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

# Initialize DB on app import
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            student_name = request.form.get("student_name", "").strip()
            if not student_name:
                flash("Student Name is required.", "danger")
                return render_template("predict.html", form_data=request.form)

            age = int(request.form.get("age", 20))
            if not (15 <= age <= 100):
                flash("Age must be between 15 and 100.", "danger")
                return render_template("predict.html", form_data=request.form)

            gender = request.form.get("gender", "Male")
            if gender not in ["Male", "Female", "Other"]:
                flash("Invalid gender selection.", "danger")
                return render_template("predict.html", form_data=request.form)

            attendance = float(request.form.get("attendance_percentage", 0))
            if not (0.0 <= attendance <= 100.0):
                flash("Attendance percentage must be between 0 and 100.", "danger")
                return render_template("predict.html", form_data=request.form)

            internal_marks = float(request.form.get("internal_marks", 0))
            if not (0.0 <= internal_marks <= 100.0):
                flash("Internal marks must be between 0 and 100.", "danger")
                return render_template("predict.html", form_data=request.form)

            assignment_score = float(request.form.get("assignment_score", 0))
            if not (0.0 <= assignment_score <= 100.0):
                flash("Assignment score must be between 0 and 100.", "danger")
                return render_template("predict.html", form_data=request.form)

            prev_sem = float(request.form.get("previous_semester_percentage", 0))
            if not (0.0 <= prev_sem <= 100.0):
                flash("Previous semester percentage must be between 0 and 100.", "danger")
                return render_template("predict.html", form_data=request.form)

            study_hours = float(request.form.get("study_hours_per_day", 0))
            if not (0.0 <= study_hours <= 24.0):
                flash("Study hours per day must be between 0 and 24.", "danger")
                return render_template("predict.html", form_data=request.form)

            backlogs = int(request.form.get("backlogs", 0))
            if backlogs < 0:
                flash("Number of backlogs cannot be negative.", "danger")
                return render_template("predict.html", form_data=request.form)

            extracurricular = request.form.get("extracurricular_participation", "No")
            family_support = request.form.get("family_support", "Yes")
            internet_access = request.form.get("internet_access", "Yes")

            student_data = {
                "age": age,
                "gender": gender,
                "attendance_percentage": attendance,
                "internal_marks": internal_marks,
                "assignment_score": assignment_score,
                "previous_semester_percentage": prev_sem,
                "study_hours_per_day": study_hours,
                "backlogs": backlogs,
                "extracurricular_participation": extracurricular,
                "family_support": family_support,
                "internet_access": internet_access
            }

            # ML Risk Prediction
            result = predictor.predict_risk(student_data)
            
            risk_level = result["predicted_risk"]
            confidence = result["confidence_score"]
            recs_json = json.dumps(result["recommendations"])

            # Store in database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (
                    student_name, age, gender, attendance_percentage, internal_marks,
                    assignment_score, previous_semester_percentage, study_hours_per_day,
                    backlogs, extracurricular_participation, family_support, internet_access,
                    risk_level, confidence, recommendations
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_name, age, gender, attendance, internal_marks,
                assignment_score, prev_sem, study_hours, backlogs,
                extracurricular, family_support, internet_access,
                risk_level, confidence, recs_json
            ))
            student_id = cursor.lastrowid
            conn.commit()
            conn.close()

            flash("Academic risk prediction completed successfully!", "success")
            return redirect(url_for("result", student_id=student_id))

        except Exception as e:
            flash(f"An unexpected error occurred during prediction: {str(e)}", "danger")
            return render_template("predict.html", form_data=request.form)

    return render_template("predict.html", form_data={})

@app.route("/result/<int:student_id>")
def result(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()

    if not student:
        flash("Student prediction record not found.", "warning")
        return redirect(url_for("predict"))

    recommendations = json.loads(student["recommendations"]) if student["recommendations"] else []
    
    # Generate factors dynamically from stored student metrics
    factors = predictor._extract_contributing_factors({
        "attendance_percentage": student["attendance_percentage"],
        "internal_marks": student["internal_marks"],
        "assignment_score": student["assignment_score"],
        "previous_semester_percentage": student["previous_semester_percentage"],
        "study_hours_per_day": student["study_hours_per_day"],
        "backlogs": student["backlogs"]
    })

    return render_template(
        "result.html",
        student=student,
        recommendations=recommendations,
        factors=factors
    )

@app.route("/dashboard")
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE risk_level = 'LOW RISK'")
    low_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE risk_level = 'MEDIUM RISK'")
    med_risk = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE risk_level = 'HIGH RISK'")
    high_risk = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(attendance_percentage), AVG(internal_marks) FROM students")
    avg_row = cursor.fetchone()
    avg_attendance = round(avg_row[0], 1) if avg_row[0] is not None else 0.0
    avg_marks = round(avg_row[1], 1) if avg_row[1] is not None else 0.0

    cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 5")
    recent_students = cursor.fetchall()
    conn.close()

    return render_template(
        "dashboard.html",
        total_students=total_students,
        low_risk=low_risk,
        med_risk=med_risk,
        high_risk=high_risk,
        avg_attendance=avg_attendance,
        avg_marks=avg_marks,
        recent_students=recent_students
    )

@app.route("/api/stats")
def api_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Risk Distribution
    cursor.execute("SELECT risk_level, COUNT(*) FROM students GROUP BY risk_level")
    risk_rows = cursor.fetchall()
    risk_counts = {"LOW RISK": 0, "MEDIUM RISK": 0, "HIGH RISK": 0}
    for row in risk_rows:
        risk_counts[row[0]] = row[1]

    # Attendance & Marks by Risk Level
    cursor.execute("""
        SELECT risk_level, AVG(attendance_percentage), AVG(internal_marks) 
        FROM students 
        GROUP BY risk_level
    """)
    avg_rows = cursor.fetchall()
    attendance_by_risk = {"LOW RISK": 0, "MEDIUM RISK": 0, "HIGH RISK": 0}
    marks_by_risk = {"LOW RISK": 0, "MEDIUM RISK": 0, "HIGH RISK": 0}
    
    for row in avg_rows:
        risk = row[0]
        attendance_by_risk[risk] = round(row[1], 1) if row[1] else 0
        marks_by_risk[risk] = round(row[2], 1) if row[2] else 0

    conn.close()

    return jsonify({
        "risk_counts": risk_counts,
        "attendance_by_risk": attendance_by_risk,
        "marks_by_risk": marks_by_risk
    })

@app.route("/students")
def students():
    search_query = request.args.get("search", "").strip()
    risk_filter = request.args.get("risk", "").strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if search_query:
        query += " AND student_name LIKE ?"
        params.append(f"%{search_query}%")

    if risk_filter and risk_filter != "ALL":
        query += " AND risk_level = ?"
        params.append(risk_filter)

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    student_records = cursor.fetchall()
    conn.close()

    return render_template(
        "students.html",
        students=student_records,
        search_query=search_query,
        risk_filter=risk_filter
    )

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
