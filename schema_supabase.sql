-- ============================================================
-- Supabase PostgreSQL Schema & Seed for College Student Management System
-- Database: PostgreSQL (Supabase Compatible)
-- ============================================================

-- 1. Create Tables
CREATE TABLE IF NOT EXISTS students (
    student_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    gender VARCHAR(10),
    date_of_birth DATE,
    course VARCHAR(100),
    department VARCHAR(100),
    year INT DEFAULT 1,
    semester INT DEFAULT 1,
    batch VARCHAR(20),
    city VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(20) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Admin', 'Faculty', 'Student')),
    full_name VARCHAR(100) NOT NULL,
    student_id VARCHAR(20) REFERENCES students(student_id) ON DELETE SET NULL,
    email VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id VARCHAR(20) PRIMARY KEY,
    subject_code VARCHAR(20) UNIQUE NOT NULL,
    subject_name VARCHAR(100) NOT NULL,
    credits INT DEFAULT 3,
    faculty_user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS marks (
    mark_id VARCHAR(20) PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id VARCHAR(20) NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    internal_marks_40 NUMERIC(5,2) DEFAULT 0,
    external_marks_60 NUMERIC(5,2) DEFAULT 0,
    total_marks_100 NUMERIC(5,2) DEFAULT 0,
    grade VARCHAR(5),
    result VARCHAR(10) CHECK (result IN ('Pass', 'Fail')),
    exam_session VARCHAR(50),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_student_subject_mark UNIQUE (student_id, subject_id, exam_session)
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id VARCHAR(20) PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id VARCHAR(20) NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    total_classes INT DEFAULT 0,
    classes_attended INT DEFAULT 0,
    attendance_percentage NUMERIC(5,2) DEFAULT 0.0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_student_subject_att UNIQUE (student_id, subject_id)
);

CREATE TABLE IF NOT EXISTS observations (
    observation_id VARCHAR(20) PRIMARY KEY,
    student_id VARCHAR(20) NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    faculty_user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE SET NULL,
    observation_date DATE DEFAULT CURRENT_DATE,
    academic_performance VARCHAR(50),
    communication VARCHAR(50),
    teamwork VARCHAR(50),
    technical_skills VARCHAR(50),
    faculty_remarks TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS announcements (
    announcement_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    posted_date DATE DEFAULT CURRENT_DATE,
    target_audience VARCHAR(50) DEFAULT 'All Students',
    posted_by_user_id VARCHAR(20) REFERENCES users(user_id) ON DELETE SET NULL,
    category VARCHAR(50) DEFAULT 'General',
    priority VARCHAR(20) DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sops (
    sop_id VARCHAR(20) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    guideline TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS faqs (
    faq_id VARCHAR(20) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    question TEXT NOT NULL,
    keywords TEXT,
    answer TEXT NOT NULL
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_marks_student ON marks(student_id);
CREATE INDEX IF NOT EXISTS idx_attendance_student ON attendance(student_id);
CREATE INDEX IF NOT EXISTS idx_observations_student ON observations(student_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- RLS (Row Level Security) - Optional in Supabase
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE marks ENABLE ROW LEVEL SECURITY;
ALTER TABLE attendance ENABLE ROW LEVEL SECURITY;
ALTER TABLE observations ENABLE ROW LEVEL SECURITY;
ALTER TABLE announcements ENABLE ROW LEVEL SECURITY;
ALTER TABLE sops ENABLE ROW LEVEL SECURITY;
ALTER TABLE faqs ENABLE ROW LEVEL SECURITY;

-- Allow public read/write for demo integration or configure as appropriate
CREATE POLICY "Public Read Students" ON students FOR SELECT USING (true);
CREATE POLICY "Public All Users" ON users FOR ALL USING (true);
CREATE POLICY "Public All Marks" ON marks FOR ALL USING (true);
CREATE POLICY "Public All Attendance" ON attendance FOR ALL USING (true);
CREATE POLICY "Public All Observations" ON observations FOR ALL USING (true);
CREATE POLICY "Public All Announcements" ON announcements FOR ALL USING (true);
CREATE POLICY "Public All SOPs" ON sops FOR ALL USING (true);
CREATE POLICY "Public All FAQs" ON faqs FOR ALL USING (true);
