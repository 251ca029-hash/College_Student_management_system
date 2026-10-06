import os
import sqlite3
from config import Config
from seed_data import (
    STUDENTS_DATA, USERS_DATA, SUBJECTS_DATA,
    MARKS_DATA, ATTENDANCE_DATA, OBSERVATIONS_DATA,
    ANNOUNCEMENTS_DATA, SOPS_DATA, FAQS_DATA
)

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    Client = None

class DatabaseManager:
    def __init__(self):
        self.sqlite_path = Config.SQLITE_DB_PATH
        self.supabase_url = Config.SUPABASE_URL
        self.supabase_key = Config.SUPABASE_KEY
        self.supabase_client = None
        self.active_mode = "sqlite" # 'supabase' or 'sqlite'
        
        self.init_sqlite()
        self.init_supabase_if_configured()

    def get_sqlite_conn(self):
        conn = sqlite3.connect(self.sqlite_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_sqlite(self):
        """Initializes SQLite schema and seeds datasets if empty."""
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            gender TEXT,
            date_of_birth TEXT,
            course TEXT,
            department TEXT,
            year INTEGER DEFAULT 1,
            semester INTEGER DEFAULT 1,
            batch TEXT,
            city TEXT
        );

        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            student_id TEXT,
            email TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        );

        CREATE TABLE IF NOT EXISTS subjects (
            subject_id TEXT PRIMARY KEY,
            subject_code TEXT UNIQUE NOT NULL,
            subject_name TEXT NOT NULL,
            credits INTEGER DEFAULT 3,
            faculty_user_id TEXT,
            FOREIGN KEY (faculty_user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS marks (
            mark_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            subject_id TEXT NOT NULL,
            internal_marks_40 REAL DEFAULT 0,
            external_marks_60 REAL DEFAULT 0,
            total_marks_100 REAL DEFAULT 0,
            grade TEXT,
            result TEXT,
            exam_session TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        );

        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            subject_id TEXT NOT NULL,
            total_classes INTEGER DEFAULT 0,
            classes_attended INTEGER DEFAULT 0,
            attendance_percentage REAL DEFAULT 0.0,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        );

        CREATE TABLE IF NOT EXISTS observations (
            observation_id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            faculty_user_id TEXT,
            observation_date TEXT,
            academic_performance TEXT,
            communication TEXT,
            teamwork TEXT,
            technical_skills TEXT,
            faculty_remarks TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (faculty_user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS announcements (
            announcement_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            posted_date TEXT,
            target_audience TEXT DEFAULT 'All Students',
            posted_by_user_id TEXT,
            category TEXT DEFAULT 'General',
            priority TEXT DEFAULT 'Medium',
            FOREIGN KEY (posted_by_user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS sops (
            sop_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            guideline TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS faqs (
            faq_id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            keywords TEXT,
            answer TEXT NOT NULL
        );
        """)
        
        # Check if empty, then seed
        cur.execute("SELECT COUNT(*) FROM students")
        if cur.fetchone()[0] == 0:
            self._seed_sqlite(cur)
            
        conn.commit()
        conn.close()

    def _seed_sqlite(self, cur):
        for s in STUDENTS_DATA:
            cur.execute("""
                INSERT OR REPLACE INTO students (student_id, full_name, email, phone, gender, date_of_birth, course, department, year, semester, batch, city)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (s["student_id"], s["full_name"], s["email"], s["phone"], s["gender"], s["date_of_birth"], s["course"], s["department"], s["year"], s["semester"], s["batch"], s["city"]))

        for u in USERS_DATA:
            cur.execute("""
                INSERT OR REPLACE INTO users (user_id, username, password, role, full_name, student_id, email, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (u["user_id"], u["username"], u["password"], u["role"], u["full_name"], u["student_id"], u["email"], u["status"]))

        for sub in SUBJECTS_DATA:
            cur.execute("""
                INSERT OR REPLACE INTO subjects (subject_id, subject_code, subject_name, credits, faculty_user_id)
                VALUES (?, ?, ?, ?, ?)
            """, (sub["subject_id"], sub["subject_code"], sub["subject_name"], sub["credits"], sub["faculty_user_id"]))

        for m in MARKS_DATA:
            cur.execute("""
                INSERT OR REPLACE INTO marks (mark_id, student_id, subject_id, internal_marks_40, external_marks_60, total_marks_100, grade, result, exam_session)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (m["mark_id"], m["student_id"], m["subject_id"], m["internal_marks_40"], m["external_marks_60"], m["total_marks_100"], m["grade"], m["result"], m["exam_session"]))

        for a in ATTENDANCE_DATA:
            cur.execute("""
                INSERT OR REPLACE INTO attendance (attendance_id, student_id, subject_id, total_classes, classes_attended, attendance_percentage)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (a["attendance_id"], a["student_id"], a["subject_id"], a["total_classes"], a["classes_attended"], a["attendance_percentage"]))

        for o in OBSERVATIONS_DATA:
            cur.execute("""
                INSERT OR REPLACE INTO observations (observation_id, student_id, faculty_user_id, observation_date, academic_performance, communication, teamwork, technical_skills, faculty_remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (o["observation_id"], o["student_id"], o["faculty_user_id"], o["observation_date"], o["academic_performance"], o["communication"], o["teamwork"], o["technical_skills"], o["faculty_remarks"]))

        for an in ANNOUNCEMENTS_DATA:
            cur.execute("""
                INSERT OR REPLACE INTO announcements (announcement_id, title, message, posted_date, target_audience, posted_by_user_id, category, priority)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (an["announcement_id"], an["title"], an["message"], an["posted_date"], an["target_audience"], an["posted_by_user_id"], an["category"], an["priority"]))

        for sop in SOPS_DATA:
            cur.execute("""
                INSERT OR REPLACE INTO sops (sop_id, category, guideline)
                VALUES (?, ?, ?)
            """, (sop["sop_id"], sop["category"], sop["guideline"]))

        for faq in FAQS_DATA:
            cur.execute("""
                INSERT OR REPLACE INTO faqs (faq_id, category, question, keywords, answer)
                VALUES (?, ?, ?, ?, ?)
            """, (faq["faq_id"], faq["category"], faq["question"], faq["keywords"], faq["answer"]))

    def init_supabase_if_configured(self):
        if SUPABASE_AVAILABLE and self.supabase_url and self.supabase_key:
            try:
                self.supabase_client = create_client(self.supabase_url, self.supabase_key)
                self.active_mode = "supabase"
            except Exception as e:
                print(f"[Supabase Init Warning] Could not connect to Supabase: {e}. Defaulting to SQLite.")
                self.active_mode = "sqlite"
        else:
            self.active_mode = "sqlite"

    def test_supabase_connection(self, url, key):
        if not SUPABASE_AVAILABLE:
            return False, "supabase Python library is not installed."
        try:
            client = create_client(url, key)
            res = client.table("students").select("student_id").limit(1).execute()
            return True, f"Connection successful! Found response from Supabase."
        except Exception as e:
            return False, f"Supabase error: {str(e)}"

    def get_db_status(self):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM students")
        student_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM marks")
        marks_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM attendance")
        attendance_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM announcements")
        announcement_count = cur.fetchone()[0]
        conn.close()

        return {
            "active_mode": self.active_mode,
            "supabase_available": SUPABASE_AVAILABLE,
            "supabase_url": self.supabase_url or "Not configured (Using SQLite)",
            "student_count": student_count,
            "marks_count": marks_count,
            "attendance_count": attendance_count,
            "announcement_count": announcement_count
        }

    # ==================== DATA ACCESS METHODS ====================
    def get_user_by_username(self, username):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username.strip(),))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_user_by_id(self, user_id):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def get_all_users(self):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, role, full_name, student_id, email, status FROM users ORDER BY role, username")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all_students(self):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY student_id")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_student_by_id(self, student_id):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    def update_student(self, student_id, data):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE students SET
                full_name = ?, phone = ?, city = ?, course = ?, department = ?, year = ?, semester = ?, batch = ?
            WHERE student_id = ?
        """, (data.get("full_name"), data.get("phone"), data.get("city"), data.get("course"), data.get("department"),
              data.get("year"), data.get("semester"), data.get("batch"), student_id))
        conn.commit()
        conn.close()
        return True

    def get_all_subjects(self):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.*, u.full_name as faculty_name 
            FROM subjects s 
            LEFT JOIN users u ON s.faculty_user_id = u.user_id
            ORDER BY s.subject_code
        """)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_marks_by_student(self, student_id):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT m.*, s.subject_code, s.subject_name, s.credits
            FROM marks m
            JOIN subjects s ON m.subject_id = s.subject_id
            WHERE m.student_id = ?
            ORDER BY s.subject_code
        """, (student_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all_marks(self):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT m.*, st.full_name as student_name, sub.subject_code, sub.subject_name
            FROM marks m
            JOIN students st ON m.student_id = st.student_id
            JOIN subjects sub ON m.subject_id = sub.subject_id
            ORDER BY m.student_id, sub.subject_code
        """)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def upsert_mark(self, mark_id, student_id, subject_id, internal, external, exam_session="2025-26 Even"):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        
        total = round(internal + external, 2)
        # Calculate grade and result
        if total >= 90:
            grade = "O"
        elif total >= 80:
            grade = "A+"
        elif total >= 70:
            grade = "A"
        elif total >= 60:
            grade = "B+"
        elif total >= 50:
            grade = "B"
        elif total >= 40:
            grade = "C"
        else:
            grade = "F"
            
        result = "Pass" if (total >= 40 and external >= 21) else "Fail"
        if result == "Fail":
            grade = "F"

        if not mark_id:
            # Generate new mark_id
            cur.execute("SELECT COUNT(*) FROM marks")
            count = cur.fetchone()[0] + 1
            mark_id = f"M{count:03d}"

        cur.execute("""
            INSERT OR REPLACE INTO marks 
            (mark_id, student_id, subject_id, internal_marks_40, external_marks_60, total_marks_100, grade, result, exam_session)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (mark_id, student_id, subject_id, internal, external, total, grade, result, exam_session))
        
        conn.commit()
        conn.close()
        return {"mark_id": mark_id, "total": total, "grade": grade, "result": result}

    def get_attendance_by_student(self, student_id):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.*, s.subject_code, s.subject_name
            FROM attendance a
            JOIN subjects s ON a.subject_id = s.subject_id
            WHERE a.student_id = ?
            ORDER BY s.subject_code
        """, (student_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all_attendance(self):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT a.*, st.full_name as student_name, s.subject_code, s.subject_name
            FROM attendance a
            JOIN students st ON a.student_id = st.student_id
            JOIN subjects s ON a.subject_id = s.subject_id
            ORDER BY a.student_id, s.subject_code
        """)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def upsert_attendance(self, attendance_id, student_id, subject_id, total, attended):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        
        pct = round((attended / total * 100), 2) if total > 0 else 0.0
        
        if not attendance_id:
            cur.execute("SELECT COUNT(*) FROM attendance")
            count = cur.fetchone()[0] + 1
            attendance_id = f"A{count:03d}"
            
        cur.execute("""
            INSERT OR REPLACE INTO attendance 
            (attendance_id, student_id, subject_id, total_classes, classes_attended, attendance_percentage)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (attendance_id, student_id, subject_id, total, attended, pct))
        
        conn.commit()
        conn.close()
        return {"attendance_id": attendance_id, "percentage": pct}

    def get_observations_by_student(self, student_id):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.*, u.full_name as faculty_name
            FROM observations o
            LEFT JOIN users u ON o.faculty_user_id = u.user_id
            WHERE o.student_id = ?
            ORDER BY o.observation_date DESC
        """, (student_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all_observations(self):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT o.*, st.full_name as student_name, u.full_name as faculty_name
            FROM observations o
            JOIN students st ON o.student_id = st.student_id
            LEFT JOIN users u ON o.faculty_user_id = u.user_id
            ORDER BY o.student_id
        """)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def upsert_observation(self, data):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        
        obs_id = data.get("observation_id")
        if not obs_id:
            cur.execute("SELECT COUNT(*) FROM observations")
            count = cur.fetchone()[0] + 1
            obs_id = f"O{count:03d}"
            
        cur.execute("""
            INSERT OR REPLACE INTO observations
            (observation_id, student_id, faculty_user_id, observation_date, academic_performance, communication, teamwork, technical_skills, faculty_remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (obs_id, data.get("student_id"), data.get("faculty_user_id"), data.get("observation_date"),
              data.get("academic_performance"), data.get("communication"), data.get("teamwork"),
              data.get("technical_skills"), data.get("faculty_remarks")))
        
        conn.commit()
        conn.close()
        return obs_id

    def get_announcements(self, target_audience=None):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        if target_audience and target_audience != "All":
            cur.execute("""
                SELECT a.*, u.full_name as posted_by_name
                FROM announcements a
                LEFT JOIN users u ON a.posted_by_user_id = u.user_id
                WHERE a.target_audience IN (?, 'All Students')
                ORDER BY a.posted_date DESC
            """, (target_audience,))
        else:
            cur.execute("""
                SELECT a.*, u.full_name as posted_by_name
                FROM announcements a
                LEFT JOIN users u ON a.posted_by_user_id = u.user_id
                ORDER BY a.posted_date DESC
            """)
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def add_announcement(self, data):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM announcements")
        count = cur.fetchone()[0] + 1
        an_id = f"AN{count:03d}"
        
        cur.execute("""
            INSERT INTO announcements 
            (announcement_id, title, message, posted_date, target_audience, posted_by_user_id, category, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (an_id, data.get("title"), data.get("message"), data.get("posted_date"),
              data.get("target_audience", "All Students"), data.get("posted_by_user_id"),
              data.get("category", "General"), data.get("priority", "Medium")))
        
        conn.commit()
        conn.close()
        return an_id

    def delete_announcement(self, an_id):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM announcements WHERE announcement_id = ?", (an_id,))
        conn.commit()
        conn.close()
        return True

    def get_sops(self, category=None):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        if category and category != "All":
            cur.execute("SELECT * FROM sops WHERE category = ? ORDER BY sop_id", (category,))
        else:
            cur.execute("SELECT * FROM sops ORDER BY category, sop_id")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_faqs(self, category=None):
        conn = self.get_sqlite_conn()
        cur = conn.cursor()
        if category and category != "All":
            cur.execute("SELECT * FROM faqs WHERE category = ? ORDER BY faq_id", (category,))
        else:
            cur.execute("SELECT * FROM faqs ORDER BY category, faq_id")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

db_manager = DatabaseManager()
