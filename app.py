"""
Flask Application - Full-Fledged College Student Management System
With Supabase PostgreSQL support, NumPy, Pandas, Scikit-learn ML & ChatGPT-4 mini humanoid Chatbot
"""
import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from config import Config
from db import db_manager
from ml_analytics import analytics_engine
from chatbot_engine import chatbot_engine

app = Flask(__name__)
app.config.from_object(Config)

# ==================== AUTHENTICATION DECORATORS ====================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Please sign in to access this portal.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("login"))
            user = session["user"]
            if user.get("role") not in allowed_roles:
                flash("Access denied. You do not have permission for this section.", "danger")
                return redirect(url_for("dashboard"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Context Processor for Templates
@app.context_processor
def inject_global_data():
    return {
        "current_user": session.get("user"),
        "db_mode": db_manager.active_mode,
        "college_name": "Sri Ramakrishna College of Arts and Science for Women"
    }

# ==================== AUTHENTICATION ROUTES ====================
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        selected_role = request.form.get("role", "")

        user = db_manager.get_user_by_username(username)
        if not user:
            flash("Invalid username or account not found.", "danger")
            return render_template("login.html")

        if user["password"] != password:
            flash("Incorrect password. Please verify your credentials.", "danger")
            return render_template("login.html")

        if selected_role and user["role"].lower() != selected_role.lower():
            flash(f"Account '{username}' is registered as a {user['role']}, not {selected_role}.", "danger")
            return render_template("login.html")

        if user["status"] != "Active":
            flash("Your account is inactive. Please contact the administrator.", "danger")
            return render_template("login.html")

        session["user"] = user
        flash(f"Welcome back, {user['full_name']}! Signed in as {user['role']}.", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("login"))

# ==================== ROLE-BASED DASHBOARDS ====================
@app.route("/dashboard")
@login_required
def dashboard():
    role = session["user"].get("role")
    if role == "Student":
        return redirect(url_for("student_dashboard"))
    elif role == "Faculty":
        return redirect(url_for("faculty_dashboard"))
    elif role == "Admin":
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("login"))

@app.route("/student/dashboard")
@login_required
@role_required("Student")
def student_dashboard():
    student_id = session["user"].get("student_id")
    if not student_id:
        flash("No student profile linked to this user account.", "danger")
        return redirect(url_for("login"))

    analytics = analytics_engine.get_student_analytics(student_id)
    announcements = db_manager.get_announcements(target_audience="All Students")
    
    return render_template(
        "student_dashboard.html",
        data=analytics,
        student=analytics["student"],
        announcements=announcements
    )

@app.route("/faculty/dashboard")
@login_required
@role_required("Faculty", "Admin")
def faculty_dashboard():
    user = session["user"]
    faculty_id = user["user_id"]
    
    # Get subjects taught
    all_subjects = db_manager.get_all_subjects()
    my_subjects = [s for s in all_subjects if s.get("faculty_user_id") == faculty_id]
    
    overview = analytics_engine.get_class_overview_analytics()
    announcements = db_manager.get_announcements()
    
    return render_template(
        "faculty_dashboard.html",
        my_subjects=my_subjects,
        overview=overview,
        announcements=announcements
    )

@app.route("/admin/dashboard")
@login_required
@role_required("Admin")
def admin_dashboard():
    overview = analytics_engine.get_class_overview_analytics()
    users = db_manager.get_all_users()
    students = db_manager.get_all_students()
    announcements = db_manager.get_announcements()
    db_status = db_manager.get_db_status()
    
    return render_template(
        "admin_dashboard.html",
        overview=overview,
        users=users,
        students=students,
        announcements=announcements,
        db_status=db_status
    )

# ==================== MARKS MANAGEMENT ====================
@app.route("/marks")
@login_required
def marks_management():
    role = session["user"].get("role")
    
    if role == "Student":
        student_id = session["user"].get("student_id")
        marks = db_manager.get_marks_by_student(student_id)
        students = [db_manager.get_student_by_id(student_id)]
    else:
        marks = db_manager.get_all_marks()
        students = db_manager.get_all_students()

    subjects = db_manager.get_all_subjects()
    return render_template("marks_management.html", marks=marks, students=students, subjects=subjects)

@app.route("/api/marks/upsert", methods=["POST"])
@login_required
@role_required("Faculty", "Admin")
def api_upsert_mark():
    mark_id = request.form.get("mark_id", "").strip() or None
    student_id = request.form.get("student_id")
    subject_id = request.form.get("subject_id")
    internal = float(request.form.get("internal_marks_40", 0))
    external = float(request.form.get("external_marks_60", 0))
    exam_session = request.form.get("exam_session", "2025-26 Even")

    # Enforce boundaries
    internal = max(0.0, min(40.0, internal))
    external = max(0.0, min(60.0, external))

    res = db_manager.upsert_mark(mark_id, student_id, subject_id, internal, external, exam_session)
    flash(f"Marks updated successfully for {student_id}! Total: {res['total']}/100, Grade: {res['grade']}, Result: {res['result']}.", "success")
    return redirect(url_for("marks_management"))

@app.route("/report-card/<student_id>")
@login_required
def report_card(student_id):
    role = session["user"].get("role")
    # Verify student only views own report card
    if role == "Student" and session["user"].get("student_id") != student_id:
        flash("Unauthorized to view other students' report card.", "danger")
        return redirect(url_for("student_dashboard"))

    analytics = analytics_engine.get_student_analytics(student_id)
    if not analytics:
        flash("Student record not found.", "danger")
        return redirect(url_for("marks_management"))

    return render_template("report_card.html", data=analytics)

# ==================== ATTENDANCE MANAGEMENT ====================
@app.route("/attendance")
@login_required
def attendance_management():
    role = session["user"].get("role")
    if role == "Student":
        student_id = session["user"].get("student_id")
        attendance = db_manager.get_attendance_by_student(student_id)
        students = [db_manager.get_student_by_id(student_id)]
    else:
        attendance = db_manager.get_all_attendance()
        students = db_manager.get_all_students()

    subjects = db_manager.get_all_subjects()
    return render_template("attendance_management.html", attendance=attendance, students=students, subjects=subjects)

@app.route("/api/attendance/upsert", methods=["POST"])
@login_required
@role_required("Faculty", "Admin")
def api_upsert_attendance():
    attendance_id = request.form.get("attendance_id", "").strip() or None
    student_id = request.form.get("student_id")
    subject_id = request.form.get("subject_id")
    total_classes = int(request.form.get("total_classes", 0))
    classes_attended = int(request.form.get("classes_attended", 0))

    classes_attended = min(classes_attended, total_classes)

    res = db_manager.upsert_attendance(attendance_id, student_id, subject_id, total_classes, classes_attended)
    flash(f"Attendance recorded for {student_id}! Current percentage: {res['percentage']}%.", "success")
    return redirect(url_for("attendance_management"))

# ==================== STUDENT OBSERVATION / PERFORMANCE ====================
@app.route("/observations")
@login_required
def observations():
    role = session["user"].get("role")
    if role == "Student":
        student_id = session["user"].get("student_id")
        obs_list = db_manager.get_observations_by_student(student_id)
        students = [db_manager.get_student_by_id(student_id)]
    else:
        obs_list = db_manager.get_all_observations()
        students = db_manager.get_all_students()

    return render_template("observations.html", observations=obs_list, students=students)

@app.route("/api/observations/upsert", methods=["POST"])
@login_required
@role_required("Faculty", "Admin")
def api_upsert_observation():
    data = {
        "observation_id": request.form.get("observation_id", "").strip() or None,
        "student_id": request.form.get("student_id"),
        "faculty_user_id": session["user"]["user_id"],
        "observation_date": request.form.get("observation_date"),
        "academic_performance": request.form.get("academic_performance"),
        "communication": request.form.get("communication"),
        "teamwork": request.form.get("teamwork"),
        "technical_skills": request.form.get("technical_skills"),
        "faculty_remarks": request.form.get("faculty_remarks")
    }
    db_manager.upsert_observation(data)
    flash(f"Academic observation successfully saved for student {data['student_id']}.", "success")
    return redirect(url_for("observations"))

# ==================== COLLEGE GUIDELINES, SOPS & FAQS ====================
@app.route("/guidelines")
def guidelines():
    category = request.args.get("category", "All")
    sops = db_manager.get_sops(category if category != "All" else None)
    return render_template("sops.html", sops=sops, selected_category=category)

@app.route("/faqs")
def faqs():
    category = request.args.get("category", "All")
    query = request.args.get("q", "").strip()

    if query:
        search_results = analytics_engine.search_knowledge_base(query, top_k=8)
    else:
        search_results = None

    all_faqs = db_manager.get_faqs(category if category != "All" else None)
    return render_template(
        "faqs.html",
        faqs=all_faqs,
        search_results=search_results,
        query=query,
        selected_category=category
    )

# ==================== ANNOUNCEMENTS ====================
@app.route("/announcements")
@login_required
def announcements():
    role = session["user"].get("role")
    target = "All Students" if role == "Student" else None
    announcements_list = db_manager.get_announcements(target)
    return render_template("announcements.html", announcements=announcements_list)

@app.route("/api/announcements/create", methods=["POST"])
@login_required
@role_required("Faculty", "Admin")
def api_create_announcement():
    data = {
        "title": request.form.get("title"),
        "message": request.form.get("message"),
        "posted_date": request.form.get("posted_date"),
        "target_audience": request.form.get("target_audience", "All Students"),
        "posted_by_user_id": session["user"]["user_id"],
        "category": request.form.get("category", "General"),
        "priority": request.form.get("priority", "Medium")
    }
    db_manager.add_announcement(data)
    flash("Announcement published successfully!", "success")
    return redirect(url_for("announcements"))

@app.route("/api/announcements/delete/<an_id>", methods=["POST"])
@login_required
@role_required("Faculty", "Admin")
def api_delete_announcement(an_id):
    db_manager.delete_announcement(an_id)
    flash("Announcement deleted.", "info")
    return redirect(url_for("announcements"))

# ==================== ADVANCED ML & ANALYTICS ====================
@app.route("/analytics")
@login_required
def analytics():
    role = session["user"].get("role")
    if role == "Student":
        student_id = session["user"].get("student_id")
        student_data = analytics_engine.get_student_analytics(student_id)
        class_overview = None
    else:
        student_data = None
        class_overview = analytics_engine.get_class_overview_analytics()

    return render_template("analytics.html", student_data=student_data, overview=class_overview)

# ==================== CHATGPT-4 MINI HUMANOID CHATBOT ====================
@app.route("/chatbot")
@login_required
def chatbot_page():
    return render_template("chatbot.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    message = data.get("message", "")
    current_user = session.get("user")
    
    result = chatbot_engine.process_message(message, current_user)
    return jsonify(result)

# ==================== ADMIN SETTINGS & SUPABASE ====================
@app.route("/admin/settings", methods=["GET", "POST"])
@login_required
@role_required("Admin")
def admin_settings():
    db_status = db_manager.get_db_status()
    test_result = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "test_supabase":
            url = request.form.get("supabase_url", "").strip()
            key = request.form.get("supabase_key", "").strip()
            success, msg = db_manager.test_supabase_connection(url, key)
            test_result = {"success": success, "message": msg}

    return render_template("admin_settings.html", db_status=db_status, test_result=test_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
