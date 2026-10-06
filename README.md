# 🎓 Sri Ramakrishna College of Arts and Science for Women (SRCW)
## Full-Fledged College Student Management System

An enterprise-grade, professional College Student Management System built with **Python Flask**, **Supabase PostgreSQL**, **NumPy**, **Pandas**, and **Scikit-Learn Machine Learning**, featuring a natural humanoid AI Campus Assistant (**Nova**) that mirrors **ChatGPT-4 mini**.

---

## 🌟 Key Modules & Architectural Highlights

### 1. 🔐 Login & Role-Based Authentication
* **Role-Based Portals**: Dedicated access dashboards for **Student**, **Faculty**, and **Administrator**.
* **Credentials Security**: Username/password validation with session handling.
* **1-Click Demo Accounts**: Instant test login chips on the sign-in screen:
  * **System Admin**: `admin` / `Admin@123`
  * **Faculty 1**: `faculty1` / `Faculty@123` (Dr. Meenakshi Sundar)
  * **Faculty 2**: `faculty2` / `Faculty@123` (Prof. Rajesh Kannan)
  * **Student (High Standing)**: `cs001` / `Student@001` (Ananya Krishnan)
  * **Student (Shortage/Arrears)**: `cs007` / `Student@007` (Rahul Balasubramani)

### 2. 👨‍🎓 Student Dashboard
* **Personal Profile**: Register Number (e.g. `CS001`), Department, Degree, Semester, Year, Batch, City, Email, and Phone.
* **Academic Standing**: Dynamic CGPA calculation (10-point credit-weighted scale), Overall Percentage, and Arrear backlogs.
* **Attendance Tracking & Warning**: Overall percentage gauge with **prominent shortage alerts (< 75%)** and Proforma III regulatory notice.
* **Visual Subject Performance**: Custom graphical progress bars comparing subject scores (e.g. Python, DBMS, Java, Data Structures).
* **360° Academic Observations**: Soft skills matrix (Communication, Teamwork, Technical Skills, Discipline) and faculty mentor notes.
* **Printable Official Grade Sheet**: Full marks report with security formatting, watermarks, and signature lines.

### 3. 📊 Marks Management (CIA & ESE)
* **Autonomous Scheme**: 40 Marks Internal Assessment (CIA) + 60 Marks Semester End Examination (ESE).
* **Grading Criteria**: Auto-computes Total, Grade (`O`, `A+`, `A`, `B+`, `B`, `C`, `F`), and Result (`Pass` requires min 21 in external & 40 total; else `Fail`).
* **Needs Improvement Alerts**: Automatically flags subjects scoring below 65% or failed papers.
* **Faculty Controls**: Modal for entering and updating marks with validation.

### 4. 🕐 Attendance Management
* **Subject-Wise Breakdown**: Total classes conducted, classes attended, and precise attendance percentage.
* **Eligibility Rule**: Strict compliance with College SOP 01 (Min 75% required).
* **Shortage Monitoring**: Real-time identification of students subject to Third Proforma.

### 5. 📝 Student Observation / 360° Performance
* **Comprehensive Metrics**: Evaluates Academic Performance, Communication, Participation, Discipline, Technical Coding Skills, and Teamwork.
* **Intelligent Synthesis**: Natural language summary synthesis (e.g. *"Demonstrates good academic performance, active participation in departmental activities, and requires focused improvement in problem-solving skills."*).

### 6. 📚 College Guidelines, SOPs & Knowledge Base
* **Official SOPs**: Attendance, Examinations, Lab Safety, Library Rules, Dress Code, Leave Procedures, and Grievance redressal.
* **Strict Anti-Ragging Mandate**: Zero-tolerance alert with 24/7 Helpline: `1800-180-5522`.
* **Campus Contacts**: Phone `0422-2243624` / `7373144766`, Address `#395 Sarojini Naidu Rd, Siddhapudur, Coimbatore - 641044`.

### 7. 📢 Announcements & Notice Board
* Categorized notifications: Exam Schedules, Assignment Deadlines, Tech Fest (`CodeVerse 2026`), Placement Drives, and Holidays.
* Priority indicators (High, Medium, Low) with targeted audience filters.

### 8. 📈 Machine Learning & Analytics (NumPy, Pandas, Scikit-Learn)
* **K-Means Student Clustering ($k=3$)**: Unsupervised segmentation into:
  1. *High Achievers / Placement Ready*
  2. *Consistent Core Performers*
  3. *At-Risk / Urgent Intervention Needed*
* **Pearson Correlation Engine**: Analyzes real-time correlation between attendance and examination performance ($r \approx +0.85$).
* **Statistical Visualizations**: Subject pass ratios and grade distributions via Chart.js.
* **At-Risk Diagnostic Classifier**: Scikit-Learn predictive model evaluating academic standing and generating personalized faculty action plans.

### 9. 🤖 Nova AI Campus Advisor (ChatGPT-4 mini Experience)
* **Humanoid Empathy & Conversational Fluidity**: Warm, articulate, professional, and supportive persona.
* **Dual Interface**: Persistent floating chat widget across all pages + dedicated full-screen AI advisor portal (`/chatbot`).
* **Contextual Grounding**: Understands the logged-in student's marks and attendance, and can answer personal questions like *"How is my attendance?"* or *"Which subjects do I need to improve?"*.
* **Scikit-Learn TF-IDF NLP Search**: Resolves queries on fees, admissions, Principal Dr. K. Chitra, NAAC A+, hostel, bus transport, hackathons, and clubs.

---

## 🗄️ Supabase PostgreSQL & Local Database Architecture

The system features **dual-engine support**:
1. **Supabase PostgreSQL Cloud**:
   - Ready-to-deploy SQL migration script: `schema_supabase.sql`.
   - Admin settings console (`/admin/settings`) to test connections with `SUPABASE_URL` and `SUPABASE_KEY`.
2. **Instant Local Persistence**:
   - High-fidelity SQLite database automatically initialized and pre-seeded with all 20 students, 160 marks records, 160 attendance entries, observations, SOPs, circulars, and FAQs.

---

## 🚀 Running the Project

1. Open PowerShell and navigate to the project directory:
   ```powershell
   cd C:\Users\Pavi\.gemini\antigravity\scratch\college-student-management-system
   ```

2. Run the Flask server:
   ```powershell
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```
