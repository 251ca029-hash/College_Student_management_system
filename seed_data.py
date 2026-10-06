"""
Seed Data Script for College Student Management System
Populates all tables matching the provided datasets exactly.
"""
import os
import csv
import json

STUDENTS_DATA = [
    {"student_id": "CS001", "full_name": "Ananya Krishnan", "email": "ananya.krishnan@collegedemo.edu", "phone": "9697226012", "gender": "F", "date_of_birth": "2005-09-07", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Trichy"},
    {"student_id": "CS002", "full_name": "Priya Venkatesh", "email": "priya.venkatesh@collegedemo.edu", "phone": "9647338124", "gender": "F", "date_of_birth": "2005-04-15", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Coimbatore"},
    {"student_id": "CS003", "full_name": "Kavya Raghunathan", "email": "kavya.raghunathan@collegedemo.edu", "phone": "9755667651", "gender": "F", "date_of_birth": "2005-03-23", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Pollachi"},
    {"student_id": "CS004", "full_name": "Arjun Subramanian", "email": "arjun.subramanian@collegedemo.edu", "phone": "9723718431", "gender": "M", "date_of_birth": "2005-03-07", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Tiruppur"},
    {"student_id": "CS005", "full_name": "Karthik Murugan", "email": "karthik.murugan@collegedemo.edu", "phone": "9756164955", "gender": "M", "date_of_birth": "2005-07-04", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Pollachi"},
    {"student_id": "CS006", "full_name": "Divya Shanmugam", "email": "divya.shanmugam@collegedemo.edu", "phone": "9781971316", "gender": "F", "date_of_birth": "2005-01-24", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Tiruppur"},
    {"student_id": "CS007", "full_name": "Rahul Balasubramani", "email": "rahul.balasubramani@collegedemo.edu", "phone": "9649349722", "gender": "M", "date_of_birth": "2005-07-03", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Madurai"},
    {"student_id": "CS008", "full_name": "Meena Chandran", "email": "meena.chandran@collegedemo.edu", "phone": "9619335534", "gender": "F", "date_of_birth": "2005-10-07", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Coimbatore"},
    {"student_id": "CS009", "full_name": "Vignesh Ramasamy", "email": "vignesh.ramasamy@collegedemo.edu", "phone": "9720709497", "gender": "M", "date_of_birth": "2005-11-08", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Salem"},
    {"student_id": "CS010", "full_name": "Lakshmi Narayanan", "email": "lakshmi.narayanan@collegedemo.edu", "phone": "9770855700", "gender": "F", "date_of_birth": "2005-02-13", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Madurai"},
    {"student_id": "CS011", "full_name": "Surya Prakash", "email": "surya.prakash@collegedemo.edu", "phone": "9738119557", "gender": "M", "date_of_birth": "2005-03-12", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Pollachi"},
    {"student_id": "CS012", "full_name": "Harini Selvaraj", "email": "harini.selvaraj@collegedemo.edu", "phone": "9619583482", "gender": "F", "date_of_birth": "2005-12-22", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Erode"},
    {"student_id": "CS013", "full_name": "Aravind Kumar", "email": "aravind.kumar@collegedemo.edu", "phone": "9831931511", "gender": "M", "date_of_birth": "2005-09-24", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Karur"},
    {"student_id": "CS014", "full_name": "Swetha Duraisamy", "email": "swetha.duraisamy@collegedemo.edu", "phone": "9684752529", "gender": "F", "date_of_birth": "2005-07-09", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Salem"},
    {"student_id": "CS015", "full_name": "Mohan Raj", "email": "mohan.raj@collegedemo.edu", "phone": "9840742311", "gender": "M", "date_of_birth": "2005-11-11", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Coimbatore"},
    {"student_id": "CS016", "full_name": "Deepika Palanisamy", "email": "deepika.palanisamy@collegedemo.edu", "phone": "9718883684", "gender": "F", "date_of_birth": "2005-06-13", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Salem"},
    {"student_id": "CS017", "full_name": "Sanjay Gopalan", "email": "sanjay.gopalan@collegedemo.edu", "phone": "9738538251", "gender": "M", "date_of_birth": "2005-10-23", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Karur"},
    {"student_id": "CS018", "full_name": "Revathi Anand", "email": "revathi.anand@collegedemo.edu", "phone": "9729175900", "gender": "F", "date_of_birth": "2005-07-21", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Pollachi"},
    {"student_id": "CS019", "full_name": "Naveen Thangavel", "email": "naveen.thangavel@collegedemo.edu", "phone": "9685345555", "gender": "M", "date_of_birth": "2005-03-08", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Pollachi"},
    {"student_id": "CS020", "full_name": "Nithya Sundaram", "email": "nithya.sundaram@collegedemo.edu", "phone": "9788320463", "gender": "F", "date_of_birth": "2005-12-19", "course": "B.Sc Computer Science", "department": "Computer Science", "year": 2, "semester": 4, "batch": "2024-2027", "city": "Trichy"}
]

USERS_DATA = [
    {"user_id": "U001", "username": "admin", "password": "Admin@123", "role": "Admin", "full_name": "System Administrator", "student_id": None, "email": "admin@collegedemo.edu", "status": "Active"},
    {"user_id": "U002", "username": "faculty1", "password": "Faculty@123", "role": "Faculty", "full_name": "Dr. Meenakshi Sundar", "student_id": None, "email": "meenakshi.sundar@collegedemo.edu", "status": "Active"},
    {"user_id": "U003", "username": "faculty2", "password": "Faculty@123", "role": "Faculty", "full_name": "Prof. Rajesh Kannan", "student_id": None, "email": "rajesh.kannan@collegedemo.edu", "status": "Active"},
    {"user_id": "U004", "username": "cs001", "password": "Student@001", "role": "Student", "full_name": "Ananya Krishnan", "student_id": "CS001", "email": "ananya.krishnan@collegedemo.edu", "status": "Active"},
    {"user_id": "U005", "username": "cs002", "password": "Student@002", "role": "Student", "full_name": "Priya Venkatesh", "student_id": "CS002", "email": "priya.venkatesh@collegedemo.edu", "status": "Active"},
    {"user_id": "U006", "username": "cs003", "password": "Student@003", "role": "Student", "full_name": "Kavya Raghunathan", "student_id": "CS003", "email": "kavya.raghunathan@collegedemo.edu", "status": "Active"},
    {"user_id": "U007", "username": "cs004", "password": "Student@004", "role": "Student", "full_name": "Arjun Subramanian", "student_id": "CS004", "email": "arjun.subramanian@collegedemo.edu", "status": "Active"},
    {"user_id": "U008", "username": "cs005", "password": "Student@005", "role": "Student", "full_name": "Karthik Murugan", "student_id": "CS005", "email": "karthik.murugan@collegedemo.edu", "status": "Active"},
    {"user_id": "U009", "username": "cs006", "password": "Student@006", "role": "Student", "full_name": "Divya Shanmugam", "student_id": "CS006", "email": "divya.shanmugam@collegedemo.edu", "status": "Active"},
    {"user_id": "U010", "username": "cs007", "password": "Student@007", "role": "Student", "full_name": "Rahul Balasubramani", "student_id": "CS007", "email": "rahul.balasubramani@collegedemo.edu", "status": "Active"},
    {"user_id": "U011", "username": "cs008", "password": "Student@008", "role": "Student", "full_name": "Meena Chandran", "student_id": "CS008", "email": "meena.chandran@collegedemo.edu", "status": "Active"},
    {"user_id": "U012", "username": "cs009", "password": "Student@009", "role": "Student", "full_name": "Vignesh Ramasamy", "student_id": "CS009", "email": "vignesh.ramasamy@collegedemo.edu", "status": "Active"},
    {"user_id": "U013", "username": "cs010", "password": "Student@010", "role": "Student", "full_name": "Lakshmi Narayanan", "student_id": "CS010", "email": "lakshmi.narayanan@collegedemo.edu", "status": "Active"},
    {"user_id": "U014", "username": "cs011", "password": "Student@011", "role": "Student", "full_name": "Surya Prakash", "student_id": "CS011", "email": "surya.prakash@collegedemo.edu", "status": "Active"},
    {"user_id": "U015", "username": "cs012", "password": "Student@012", "role": "Student", "full_name": "Harini Selvaraj", "student_id": "CS012", "email": "harini.selvaraj@collegedemo.edu", "status": "Active"},
    {"user_id": "U016", "username": "cs013", "password": "Student@013", "role": "Student", "full_name": "Aravind Kumar", "student_id": "CS013", "email": "aravind.kumar@collegedemo.edu", "status": "Active"},
    {"user_id": "U017", "username": "cs014", "password": "Student@014", "role": "Student", "full_name": "Swetha Duraisamy", "student_id": "CS014", "email": "swetha.duraisamy@collegedemo.edu", "status": "Active"},
    {"user_id": "U018", "username": "cs015", "password": "Student@015", "role": "Student", "full_name": "Mohan Raj", "student_id": "CS015", "email": "mohan.raj@collegedemo.edu", "status": "Active"},
    {"user_id": "U019", "username": "cs016", "password": "Student@016", "role": "Student", "full_name": "Deepika Palanisamy", "student_id": "CS016", "email": "deepika.palanisamy@collegedemo.edu", "status": "Active"},
    {"user_id": "U020", "username": "cs017", "password": "Student@017", "role": "Student", "full_name": "Sanjay Gopalan", "student_id": "CS017", "email": "sanjay.gopalan@collegedemo.edu", "status": "Active"},
    {"user_id": "U021", "username": "cs018", "password": "Student@018", "role": "Student", "full_name": "Revathi Anand", "student_id": "CS018", "email": "revathi.anand@collegedemo.edu", "status": "Active"},
    {"user_id": "U022", "username": "cs019", "password": "Student@019", "role": "Student", "full_name": "Naveen Thangavel", "student_id": "CS019", "email": "naveen.thangavel@collegedemo.edu", "status": "Active"},
    {"user_id": "U023", "username": "cs020", "password": "Student@020", "role": "Student", "full_name": "Nithya Sundaram", "student_id": "CS020", "email": "nithya.sundaram@collegedemo.edu", "status": "Active"}
]

SUBJECTS_DATA = [
    {"subject_id": "SUB01", "subject_code": "CS201", "subject_name": "Python Programming", "credits": 4, "faculty_user_id": "U002"},
    {"subject_id": "SUB02", "subject_code": "CS202", "subject_name": "Database Management Systems", "credits": 4, "faculty_user_id": "U002"},
    {"subject_id": "SUB03", "subject_code": "CS203", "subject_name": "Java Programming", "credits": 4, "faculty_user_id": "U002"},
    {"subject_id": "SUB04", "subject_code": "CS204", "subject_name": "Web Designing", "credits": 3, "faculty_user_id": "U002"},
    {"subject_id": "SUB05", "subject_code": "CS205", "subject_name": "Data Structures", "credits": 4, "faculty_user_id": "U003"},
    {"subject_id": "SUB06", "subject_code": "CS206", "subject_name": "Operating Systems", "credits": 4, "faculty_user_id": "U003"},
    {"subject_id": "SUB07", "subject_code": "CS207", "subject_name": "Computer Networks", "credits": 3, "faculty_user_id": "U003"},
    {"subject_id": "SUB08", "subject_code": "CS208", "subject_name": "Software Engineering", "credits": 3, "faculty_user_id": "U003"}
]

# Raw CSV content for marks (M001 to M160)
RAW_MARKS = """M001,CS001,SUB01,27,39,66,B+,Pass,2025-26 Even
M002,CS001,SUB02,22,39,61,B+,Pass,2025-26 Even
M003,CS001,SUB03,26,39,65,B+,Pass,2025-26 Even
M004,CS001,SUB04,30,42,72,A,Pass,2025-26 Even
M005,CS001,SUB05,21,37,58,B,Pass,2025-26 Even
M006,CS001,SUB06,25,40,65,B+,Pass,2025-26 Even
M007,CS001,SUB07,27,45,72,A,Pass,2025-26 Even
M008,CS001,SUB08,27,35,62,B+,Pass,2025-26 Even
M009,CS002,SUB01,33,48,81,A+,Pass,2025-26 Even
M010,CS002,SUB02,35,47,82,A+,Pass,2025-26 Even
M011,CS002,SUB03,31,46,77,A,Pass,2025-26 Even
M012,CS002,SUB04,29,45,74,A,Pass,2025-26 Even
M013,CS002,SUB05,31,49,80,A+,Pass,2025-26 Even
M014,CS002,SUB06,34,50,84,A+,Pass,2025-26 Even
M015,CS002,SUB07,31,47,78,A,Pass,2025-26 Even
M016,CS002,SUB08,33,50,83,A+,Pass,2025-26 Even
M017,CS003,SUB01,22,32,54,B,Pass,2025-26 Even
M018,CS003,SUB02,17,25,42,C,Pass,2025-26 Even
M019,CS003,SUB03,19,26,45,C,Pass,2025-26 Even
M020,CS003,SUB04,18,26,44,C,Pass,2025-26 Even
M021,CS003,SUB05,16,29,45,C,Pass,2025-26 Even
M022,CS003,SUB06,20,31,51,B,Pass,2025-26 Even
M023,CS003,SUB07,20,29,49,C,Pass,2025-26 Even
M024,CS003,SUB08,24,32,56,B,Pass,2025-26 Even
M025,CS004,SUB01,35,50,85,A+,Pass,2025-26 Even
M026,CS004,SUB02,31,51,82,A+,Pass,2025-26 Even
M027,CS004,SUB03,32,52,84,A+,Pass,2025-26 Even
M028,CS004,SUB04,30,48,78,A,Pass,2025-26 Even
M029,CS004,SUB05,31,48,79,A,Pass,2025-26 Even
M030,CS004,SUB06,31,49,80,A+,Pass,2025-26 Even
M031,CS004,SUB07,32,48,80,A+,Pass,2025-26 Even
M032,CS004,SUB08,34,50,84,A+,Pass,2025-26 Even
M033,CS005,SUB01,28,47,75,A,Pass,2025-26 Even
M034,CS005,SUB02,26,35,61,B+,Pass,2025-26 Even
M035,CS005,SUB03,29,43,72,A,Pass,2025-26 Even
M036,CS005,SUB04,24,36,60,B+,Pass,2025-26 Even
M037,CS005,SUB05,24,32,56,B,Pass,2025-26 Even
M038,CS005,SUB06,32,42,74,A,Pass,2025-26 Even
M039,CS005,SUB07,23,33,56,B,Pass,2025-26 Even
M040,CS005,SUB08,27,36,63,B+,Pass,2025-26 Even
M041,CS006,SUB01,19,23,42,C,Pass,2025-26 Even
M042,CS006,SUB02,21,29,50,B,Pass,2025-26 Even
M043,CS006,SUB03,21,28,49,C,Pass,2025-26 Even
M044,CS006,SUB04,19,28,47,C,Pass,2025-26 Even
M045,CS006,SUB05,16,28,44,C,Pass,2025-26 Even
M046,CS006,SUB06,19,29,48,C,Pass,2025-26 Even
M047,CS006,SUB07,21,30,51,B,Pass,2025-26 Even
M048,CS006,SUB08,22,34,56,B,Pass,2025-26 Even
M049,CS007,SUB01,18,29,47,C,Pass,2025-26 Even
M050,CS007,SUB02,12,19,31,F,Fail,2025-26 Even
M051,CS007,SUB03,14,23,37,F,Fail,2025-26 Even
M052,CS007,SUB04,14,25,39,F,Fail,2025-26 Even
M053,CS007,SUB05,17,29,46,C,Pass,2025-26 Even
M054,CS007,SUB06,16,22,38,F,Fail,2025-26 Even
M055,CS007,SUB07,13,17,30,F,Fail,2025-26 Even
M056,CS007,SUB08,18,22,40,C,Pass,2025-26 Even
M057,CS008,SUB01,38,51,89,A+,Pass,2025-26 Even
M058,CS008,SUB02,37,53,90,O,Pass,2025-26 Even
M059,CS008,SUB03,35,51,86,A+,Pass,2025-26 Even
M060,CS008,SUB04,39,59,98,O,Pass,2025-26 Even
M061,CS008,SUB05,35,58,93,O,Pass,2025-26 Even
M062,CS008,SUB06,34,55,89,A+,Pass,2025-26 Even
M063,CS008,SUB07,38,58,96,O,Pass,2025-26 Even
M064,CS008,SUB08,36,59,95,O,Pass,2025-26 Even
M065,CS009,SUB01,27,37,64,B+,Pass,2025-26 Even
M066,CS009,SUB02,24,41,65,B+,Pass,2025-26 Even
M067,CS009,SUB03,27,44,71,A,Pass,2025-26 Even
M068,CS009,SUB04,30,41,71,A,Pass,2025-26 Even
M069,CS009,SUB05,21,34,55,B,Pass,2025-26 Even
M070,CS009,SUB06,22,36,58,B,Pass,2025-26 Even
M071,CS009,SUB07,28,42,70,A,Pass,2025-26 Even
M072,CS009,SUB08,30,40,70,A,Pass,2025-26 Even
M073,CS010,SUB01,20,34,54,B,Pass,2025-26 Even
M074,CS010,SUB02,22,29,51,B,Pass,2025-26 Even
M075,CS010,SUB03,18,28,46,C,Pass,2025-26 Even
M076,CS010,SUB04,22,33,55,B,Pass,2025-26 Even
M077,CS010,SUB05,17,28,45,C,Pass,2025-26 Even
M078,CS010,SUB06,21,32,53,B,Pass,2025-26 Even
M079,CS010,SUB07,19,31,50,B,Pass,2025-26 Even
M080,CS010,SUB08,23,34,57,B,Pass,2025-26 Even
M081,CS011,SUB01,32,51,83,A+,Pass,2025-26 Even
M082,CS011,SUB02,35,49,84,A+,Pass,2025-26 Even
M083,CS011,SUB03,34,49,83,A+,Pass,2025-26 Even
M084,CS011,SUB04,28,43,71,A,Pass,2025-26 Even
M085,CS011,SUB05,33,52,85,A+,Pass,2025-26 Even
M086,CS011,SUB06,33,52,85,A+,Pass,2025-26 Even
M087,CS011,SUB07,31,47,78,A,Pass,2025-26 Even
M088,CS011,SUB08,36,50,86,A+,Pass,2025-26 Even
M089,CS012,SUB01,27,44,71,A,Pass,2025-26 Even
M090,CS012,SUB02,28,46,74,A,Pass,2025-26 Even
M091,CS012,SUB03,28,42,70,A,Pass,2025-26 Even
M092,CS012,SUB04,28,45,73,A,Pass,2025-26 Even
M093,CS012,SUB05,25,43,68,B+,Pass,2025-26 Even
M094,CS012,SUB06,28,43,71,A,Pass,2025-26 Even
M095,CS012,SUB07,26,39,65,B+,Pass,2025-26 Even
M096,CS012,SUB08,23,34,57,B,Pass,2025-26 Even
M097,CS013,SUB01,35,51,86,A+,Pass,2025-26 Even
M098,CS013,SUB02,39,56,95,O,Pass,2025-26 Even
M099,CS013,SUB03,37,55,92,O,Pass,2025-26 Even
M100,CS013,SUB04,40,58,98,O,Pass,2025-26 Even
M101,CS013,SUB05,38,58,96,O,Pass,2025-26 Even
M102,CS013,SUB06,37,56,93,O,Pass,2025-26 Even
M103,CS013,SUB07,36,52,88,A+,Pass,2025-26 Even
M104,CS013,SUB08,37,58,95,O,Pass,2025-26 Even
M105,CS014,SUB01,30,43,73,A,Pass,2025-26 Even
M106,CS014,SUB02,27,46,73,A,Pass,2025-26 Even
M107,CS014,SUB03,24,35,59,B,Pass,2025-26 Even
M108,CS014,SUB04,29,42,71,A,Pass,2025-26 Even
M109,CS014,SUB05,28,46,74,A,Pass,2025-26 Even
M110,CS014,SUB06,25,32,57,B,Pass,2025-26 Even
M111,CS014,SUB07,22,39,61,B+,Pass,2025-26 Even
M112,CS014,SUB08,24,39,63,B+,Pass,2025-26 Even
M113,CS015,SUB01,32,48,80,A+,Pass,2025-26 Even
M114,CS015,SUB02,32,49,81,A+,Pass,2025-26 Even
M115,CS015,SUB03,33,47,80,A+,Pass,2025-26 Even
M116,CS015,SUB04,30,48,78,A,Pass,2025-26 Even
M117,CS015,SUB05,35,50,85,A+,Pass,2025-26 Even
M118,CS015,SUB06,33,47,80,A+,Pass,2025-26 Even
M119,CS015,SUB07,32,53,85,A+,Pass,2025-26 Even
M120,CS015,SUB08,34,48,82,A+,Pass,2025-26 Even
M121,CS016,SUB01,18,23,41,C,Pass,2025-26 Even
M122,CS016,SUB02,13,18,31,F,Fail,2025-26 Even
M123,CS016,SUB03,14,17,31,F,Fail,2025-26 Even
M124,CS016,SUB04,16,25,41,C,Pass,2025-26 Even
M125,CS016,SUB05,18,28,46,C,Pass,2025-26 Even
M126,CS016,SUB06,14,26,40,C,Pass,2025-26 Even
M127,CS016,SUB07,16,28,44,C,Pass,2025-26 Even
M128,CS016,SUB08,16,21,37,F,Fail,2025-26 Even
M129,CS017,SUB01,26,36,62,B+,Pass,2025-26 Even
M130,CS017,SUB02,27,42,69,B+,Pass,2025-26 Even
M131,CS017,SUB03,29,41,70,A,Pass,2025-26 Even
M132,CS017,SUB04,31,47,78,A,Pass,2025-26 Even
M133,CS017,SUB05,30,47,77,A,Pass,2025-26 Even
M134,CS017,SUB06,26,40,66,B+,Pass,2025-26 Even
M135,CS017,SUB07,29,42,71,A,Pass,2025-26 Even
M136,CS017,SUB08,30,42,72,A,Pass,2025-26 Even
M137,CS018,SUB01,26,39,65,B+,Pass,2025-26 Even
M138,CS018,SUB02,26,35,61,B+,Pass,2025-26 Even
M139,CS018,SUB03,25,40,65,B+,Pass,2025-26 Even
M140,CS018,SUB04,32,43,75,A,Pass,2025-26 Even
M141,CS018,SUB05,26,39,65,B+,Pass,2025-26 Even
M142,CS018,SUB06,25,33,58,B,Pass,2025-26 Even
M143,CS018,SUB07,26,34,60,B+,Pass,2025-26 Even
M144,CS018,SUB08,22,38,60,B+,Pass,2025-26 Even
M145,CS019,SUB01,39,56,95,O,Pass,2025-26 Even
M146,CS019,SUB02,38,52,90,O,Pass,2025-26 Even
M147,CS019,SUB03,36,58,94,O,Pass,2025-26 Even
M148,CS019,SUB04,38,53,91,O,Pass,2025-26 Even
M149,CS019,SUB05,38,56,94,O,Pass,2025-26 Even
M150,CS019,SUB06,39,58,97,O,Pass,2025-26 Even
M151,CS019,SUB07,40,57,97,O,Pass,2025-26 Even
M152,CS019,SUB08,37,60,97,O,Pass,2025-26 Even
M153,CS020,SUB01,30,45,75,A,Pass,2025-26 Even
M154,CS020,SUB02,31,48,79,A,Pass,2025-26 Even
M155,CS020,SUB03,35,49,84,A+,Pass,2025-26 Even
M156,CS020,SUB04,31,49,80,A+,Pass,2025-26 Even
M157,CS020,SUB05,29,45,74,A,Pass,2025-26 Even
M158,CS020,SUB06,34,52,86,A+,Pass,2025-26 Even
M159,CS020,SUB07,30,46,76,A,Pass,2025-26 Even
M160,CS020,SUB08,29,48,77,A,Pass,2025-26 Even"""

MARKS_DATA = []
for line in RAW_MARKS.strip().split("\n"):
    parts = line.split(",")
    MARKS_DATA.append({
        "mark_id": parts[0],
        "student_id": parts[1],
        "subject_id": parts[2],
        "internal_marks_40": int(parts[3]),
        "external_marks_60": int(parts[4]),
        "total_marks_100": int(parts[5]),
        "grade": parts[6],
        "result": parts[7],
        "exam_session": parts[8]
    })

# Raw CSV content for Attendance (A001 to A160)
RAW_ATTENDANCE = """A001,CS001,SUB01,50,44,88
A002,CS001,SUB02,44,33,75
A003,CS001,SUB03,44,37,84.09
A004,CS001,SUB04,50,40,80
A005,CS001,SUB05,50,40,80
A006,CS001,SUB06,48,37,77.08
A007,CS001,SUB07,46,40,86.96
A008,CS001,SUB08,46,40,86.96
A009,CS002,SUB01,46,40,86.96
A010,CS002,SUB02,50,45,90
A011,CS002,SUB03,46,41,89.13
A012,CS002,SUB04,50,43,86
A013,CS002,SUB05,44,41,93.18
A014,CS002,SUB06,48,45,93.75
A015,CS002,SUB07,50,46,92
A016,CS002,SUB08,45,40,88.89
A017,CS003,SUB01,50,37,74
A018,CS003,SUB02,44,31,70.45
A019,CS003,SUB03,45,35,77.78
A020,CS003,SUB04,44,29,65.91
A021,CS003,SUB05,46,29,63.04
A022,CS003,SUB06,48,32,66.67
A023,CS003,SUB07,48,32,66.67
A024,CS003,SUB08,44,28,63.64
A025,CS004,SUB01,48,44,91.67
A026,CS004,SUB02,44,37,84.09
A027,CS004,SUB03,44,39,88.64
A028,CS004,SUB04,48,42,87.5
A029,CS004,SUB05,48,42,87.5
A030,CS004,SUB06,50,43,86
A031,CS004,SUB07,44,38,86.36
A032,CS004,SUB08,48,44,91.67
A033,CS005,SUB01,48,35,72.92
A034,CS005,SUB02,48,38,79.17
A035,CS005,SUB03,50,44,88
A036,CS005,SUB04,45,33,73.33
A037,CS005,SUB05,44,38,86.36
A038,CS005,SUB06,44,39,88.64
A039,CS005,SUB07,50,37,74
A040,CS005,SUB08,50,40,80
A041,CS006,SUB01,48,37,77.08
A042,CS006,SUB02,46,31,67.39
A043,CS006,SUB03,46,34,73.91
A044,CS006,SUB04,48,37,77.08
A045,CS006,SUB05,45,34,75.56
A046,CS006,SUB06,44,29,65.91
A047,CS006,SUB07,48,37,77.08
A048,CS006,SUB08,50,30,60
A049,CS007,SUB01,44,19,43.18
A050,CS007,SUB02,50,22,44
A051,CS007,SUB03,45,28,62.22
A052,CS007,SUB04,46,26,56.52
A053,CS007,SUB05,44,18,40.91
A054,CS007,SUB06,44,22,50
A055,CS007,SUB07,48,27,56.25
A056,CS007,SUB08,44,18,40.91
A057,CS008,SUB01,46,43,93.48
A058,CS008,SUB02,46,45,97.83
A059,CS008,SUB03,45,42,93.33
A060,CS008,SUB04,48,45,93.75
A061,CS008,SUB05,45,44,97.78
A062,CS008,SUB06,46,45,97.83
A063,CS008,SUB07,45,42,93.33
A064,CS008,SUB08,48,46,95.83
A065,CS009,SUB01,46,36,78.26
A066,CS009,SUB02,45,38,84.44
A067,CS009,SUB03,44,35,79.55
A068,CS009,SUB04,50,41,82
A069,CS009,SUB05,45,36,80
A070,CS009,SUB06,48,40,83.33
A071,CS009,SUB07,50,38,76
A072,CS009,SUB08,46,34,73.91
A073,CS010,SUB01,50,33,66
A074,CS010,SUB02,46,32,69.57
A075,CS010,SUB03,46,34,73.91
A076,CS010,SUB04,46,35,76.09
A077,CS010,SUB05,48,31,64.58
A078,CS010,SUB06,44,30,68.18
A079,CS010,SUB07,50,35,70
A080,CS010,SUB08,45,34,75.56
A081,CS011,SUB01,44,39,88.64
A082,CS011,SUB02,44,39,88.64
A083,CS011,SUB03,45,39,86.67
A084,CS011,SUB04,48,45,93.75
A085,CS011,SUB05,48,46,95.83
A086,CS011,SUB06,48,44,91.67
A087,CS011,SUB07,44,38,86.36
A088,CS011,SUB08,45,42,93.33
A089,CS012,SUB01,45,34,75.56
A090,CS012,SUB02,48,42,87.5
A091,CS012,SUB03,50,42,84
A092,CS012,SUB04,48,41,85.42
A093,CS012,SUB05,46,40,86.96
A094,CS012,SUB06,48,36,75
A095,CS012,SUB07,46,38,82.61
A096,CS012,SUB08,45,38,84.44
A097,CS013,SUB01,48,47,97.92
A098,CS013,SUB02,48,44,91.67
A099,CS013,SUB03,50,46,92
A100,CS013,SUB04,44,43,97.73
A101,CS013,SUB05,48,46,95.83
A102,CS013,SUB06,48,48,100
A103,CS013,SUB07,48,45,93.75
A104,CS013,SUB08,50,46,92
A105,CS014,SUB01,44,33,75
A106,CS014,SUB02,48,37,77.08
A107,CS014,SUB03,46,36,78.26
A108,CS014,SUB04,48,38,79.17
A109,CS014,SUB05,44,38,86.36
A110,CS014,SUB06,46,36,78.26
A111,CS014,SUB07,44,35,79.55
A112,CS014,SUB08,45,36,80
A113,CS015,SUB01,44,41,93.18
A114,CS015,SUB02,46,41,89.13
A115,CS015,SUB03,44,38,86.36
A116,CS015,SUB04,44,39,88.64
A117,CS015,SUB05,45,39,86.67
A118,CS015,SUB06,46,44,95.65
A119,CS015,SUB07,50,42,84
A120,CS015,SUB08,46,40,86.96
A121,CS016,SUB01,48,26,54.17
A122,CS016,SUB02,48,30,62.5
A123,CS016,SUB03,50,30,60
A124,CS016,SUB04,50,28,56
A125,CS016,SUB05,50,24,48
A126,CS016,SUB06,44,21,47.73
A127,CS016,SUB07,48,28,58.33
A128,CS016,SUB08,48,24,50
A129,CS017,SUB01,46,37,80.43
A130,CS017,SUB02,46,33,71.74
A131,CS017,SUB03,45,38,84.44
A132,CS017,SUB04,45,39,86.67
A133,CS017,SUB05,44,33,75
A134,CS017,SUB06,45,36,80
A135,CS017,SUB07,50,42,84
A136,CS017,SUB08,46,40,86.96
A137,CS018,SUB01,45,34,75.56
A138,CS018,SUB02,50,38,76
A139,CS018,SUB03,48,38,79.17
A140,CS018,SUB04,44,34,77.27
A141,CS018,SUB05,45,36,80
A142,CS018,SUB06,46,34,73.91
A143,CS018,SUB07,45,39,86.67
A144,CS018,SUB08,46,40,86.96
A145,CS019,SUB01,45,41,91.11
A146,CS019,SUB02,44,43,97.73
A147,CS019,SUB03,44,41,93.18
A148,CS019,SUB04,44,42,95.45
A149,CS019,SUB05,48,46,95.83
A150,CS019,SUB06,48,46,95.83
A151,CS019,SUB07,50,46,92
A152,CS019,SUB08,45,43,95.56
A153,CS020,SUB01,45,39,86.67
A154,CS020,SUB02,44,40,90.91
A155,CS020,SUB03,46,39,84.78
A156,CS020,SUB04,46,42,91.3
A157,CS020,SUB05,50,48,96
A158,CS020,SUB06,44,41,93.18
A159,CS020,SUB07,45,39,86.67
A160,CS020,SUB08,46,43,93.48"""

ATTENDANCE_DATA = []
for line in RAW_ATTENDANCE.strip().split("\n"):
    parts = line.split(",")
    ATTENDANCE_DATA.append({
        "attendance_id": parts[0],
        "student_id": parts[1],
        "subject_id": parts[2],
        "total_classes": int(parts[3]),
        "classes_attended": int(parts[4]),
        "attendance_percentage": float(parts[5])
    })

OBSERVATIONS_DATA = [
    {"observation_id": "O001", "student_id": "CS001", "faculty_user_id": "U003", "observation_date": "2026-02-04", "academic_performance": "Average", "communication": "Good", "teamwork": "Good", "technical_skills": "Average", "faculty_remarks": "Cooperative in team tasks; should revise fundamentals regularly."},
    {"observation_id": "O002", "student_id": "CS002", "faculty_user_id": "U003", "observation_date": "2026-03-13", "academic_performance": "Good", "communication": "Good", "teamwork": "Excellent", "technical_skills": "Good", "faculty_remarks": "Good grasp of concepts; can reach top ranks with more practice."},
    {"observation_id": "O003", "student_id": "CS003", "faculty_user_id": "U003", "observation_date": "2026-02-03", "academic_performance": "Needs Improvement", "communication": "Average", "teamwork": "Average", "technical_skills": "Needs Improvement", "faculty_remarks": "Struggles with core concepts; extra practice sessions recommended."},
    {"observation_id": "O004", "student_id": "CS004", "faculty_user_id": "U003", "observation_date": "2026-03-11", "academic_performance": "Good", "communication": "Good", "teamwork": "Excellent", "technical_skills": "Good", "faculty_remarks": "Good grasp of concepts; can reach top ranks with more practice."},
    {"observation_id": "O005", "student_id": "CS005", "faculty_user_id": "U002", "observation_date": "2026-01-08", "academic_performance": "Average", "communication": "Good", "teamwork": "Good", "technical_skills": "Average", "faculty_remarks": "Performs adequately; needs more practice in problem solving."},
    {"observation_id": "O006", "student_id": "CS006", "faculty_user_id": "U003", "observation_date": "2026-03-02", "academic_performance": "Needs Improvement", "communication": "Average", "teamwork": "Average", "technical_skills": "Needs Improvement", "faculty_remarks": "Struggles with core concepts; extra practice sessions recommended."},
    {"observation_id": "O007", "student_id": "CS007", "faculty_user_id": "U003", "observation_date": "2026-03-21", "academic_performance": "Needs Improvement", "communication": "Needs Improvement", "teamwork": "Average", "technical_skills": "Needs Improvement", "faculty_remarks": "Shows little engagement; parent meeting recommended."},
    {"observation_id": "O008", "student_id": "CS008", "faculty_user_id": "U003", "observation_date": "2026-01-19", "academic_performance": "Excellent", "communication": "Excellent", "teamwork": "Excellent", "technical_skills": "Excellent", "faculty_remarks": "Highly motivated and self-driven; strong candidate for placement and research."},
    {"observation_id": "O009", "student_id": "CS009", "faculty_user_id": "U003", "observation_date": "2026-01-16", "academic_performance": "Average", "communication": "Good", "teamwork": "Good", "technical_skills": "Average", "faculty_remarks": "Cooperative in team tasks; should revise fundamentals regularly."},
    {"observation_id": "O010", "student_id": "CS010", "faculty_user_id": "U003", "observation_date": "2026-02-11", "academic_performance": "Needs Improvement", "communication": "Average", "teamwork": "Average", "technical_skills": "Needs Improvement", "faculty_remarks": "Struggles with core concepts; extra practice sessions recommended."},
    {"observation_id": "O011", "student_id": "CS011", "faculty_user_id": "U002", "observation_date": "2026-02-14", "academic_performance": "Good", "communication": "Good", "teamwork": "Excellent", "technical_skills": "Good", "faculty_remarks": "Good grasp of concepts; can reach top ranks with more practice."},
    {"observation_id": "O012", "student_id": "CS012", "faculty_user_id": "U003", "observation_date": "2026-03-13", "academic_performance": "Average", "communication": "Good", "teamwork": "Good", "technical_skills": "Average", "faculty_remarks": "Performs adequately; needs more practice in problem solving."},
    {"observation_id": "O013", "student_id": "CS013", "faculty_user_id": "U003", "observation_date": "2026-01-11", "academic_performance": "Excellent", "communication": "Excellent", "teamwork": "Excellent", "technical_skills": "Excellent", "faculty_remarks": "Highly motivated and self-driven; strong candidate for placement and research."},
    {"observation_id": "O014", "student_id": "CS014", "faculty_user_id": "U003", "observation_date": "2026-01-25", "academic_performance": "Average", "communication": "Good", "teamwork": "Good", "technical_skills": "Average", "faculty_remarks": "Cooperative in team tasks; should revise fundamentals regularly."},
    {"observation_id": "O015", "student_id": "CS015", "faculty_user_id": "U002", "observation_date": "2026-03-28", "academic_performance": "Good", "communication": "Good", "teamwork": "Excellent", "technical_skills": "Good", "faculty_remarks": "Good grasp of concepts; can reach top ranks with more practice."},
    {"observation_id": "O016", "student_id": "CS016", "faculty_user_id": "U003", "observation_date": "2026-01-07", "academic_performance": "Needs Improvement", "communication": "Needs Improvement", "teamwork": "Average", "technical_skills": "Needs Improvement", "faculty_remarks": "Shows little engagement; parent meeting recommended."},
    {"observation_id": "O017", "student_id": "CS017", "faculty_user_id": "U003", "observation_date": "2026-03-15", "academic_performance": "Average", "communication": "Good", "teamwork": "Good", "technical_skills": "Average", "faculty_remarks": "Performs adequately; needs more practice in problem solving."},
    {"observation_id": "O018", "student_id": "CS018", "faculty_user_id": "U002", "observation_date": "2026-02-18", "academic_performance": "Average", "communication": "Good", "teamwork": "Good", "technical_skills": "Average", "faculty_remarks": "Performs adequately; needs more practice in problem solving."},
    {"observation_id": "O019", "student_id": "CS019", "faculty_user_id": "U003", "observation_date": "2026-02-23", "academic_performance": "Excellent", "communication": "Excellent", "teamwork": "Excellent", "technical_skills": "Excellent", "faculty_remarks": "Highly motivated and self-driven; strong candidate for placement and research."},
    {"observation_id": "O020", "student_id": "CS020", "faculty_user_id": "U002", "observation_date": "2026-01-21", "academic_performance": "Good", "communication": "Good", "teamwork": "Excellent", "technical_skills": "Good", "faculty_remarks": "Steady and dependable; submits assignments on time and participates actively."}
]

ANNOUNCEMENTS_DATA = [
    {"announcement_id": "AN001", "title": "Internal Examination - Series 1", "message": "Internal assessment tests begin from 10 Feb 2026. Timetable is available on the notice board.", "posted_date": "2026-02-02", "target_audience": "All Students", "posted_by_user_id": "U001", "category": "Exam", "priority": "High"},
    {"announcement_id": "AN002", "title": "Python Assignment Deadline", "message": "Submit the Python programming assignment (Unit 3) by 20 Feb 2026, 5:00 PM.", "posted_date": "2026-02-12", "target_audience": "All Students", "posted_by_user_id": "U002", "category": "Assignment", "priority": "Medium"},
    {"announcement_id": "AN003", "title": "DBMS Mini Project Submission", "message": "Mini project reports on Database Management Systems are due on 5 Mar 2026.", "posted_date": "2026-02-20", "target_audience": "All Students", "posted_by_user_id": "U002", "category": "Assignment", "priority": "Medium"},
    {"announcement_id": "AN004", "title": "Department Tech Fest - CodeVerse 2026", "message": "Annual department tech fest with coding, quiz and web design contests on 14 Mar 2026.", "posted_date": "2026-03-01", "target_audience": "All Students", "posted_by_user_id": "U001", "category": "Event", "priority": "Medium"},
    {"announcement_id": "AN005", "title": "Placement Training Programme", "message": "Aptitude and communication training for placements from 16 Mar 2026, 4:00 PM in Seminar Hall.", "posted_date": "2026-03-05", "target_audience": "All Students", "posted_by_user_id": "U001", "category": "Placement", "priority": "High"},
    {"announcement_id": "AN006", "title": "Holiday - Tamil New Year", "message": "College will remain closed on 14 Apr 2026 on account of Tamil New Year.", "posted_date": "2026-04-08", "target_audience": "All Students", "posted_by_user_id": "U001", "category": "Holiday", "priority": "Low"},
    {"announcement_id": "AN007", "title": "Faculty Meeting", "message": "Department faculty meeting on curriculum review on 18 Mar 2026 at 3:30 PM.", "posted_date": "2026-03-12", "target_audience": "Faculty", "posted_by_user_id": "U001", "category": "Meeting", "priority": "Medium"},
    {"announcement_id": "AN008", "title": "Attendance Warning", "message": "Students below 75% attendance must meet their faculty mentor before 25 Mar 2026.", "posted_date": "2026-03-15", "target_audience": "All Students", "posted_by_user_id": "U001", "category": "Attendance", "priority": "High"},
    {"announcement_id": "AN009", "title": "Guest Lecture on Cloud Computing", "message": "Industry expert session on cloud computing on 28 Mar 2026, 11:00 AM in Auditorium.", "posted_date": "2026-03-20", "target_audience": "All Students", "posted_by_user_id": "U003", "category": "Event", "priority": "Medium"},
    {"announcement_id": "AN010", "title": "Semester End Examination Schedule", "message": "End-semester examinations start on 20 Apr 2026. Hall tickets will be issued from 10 Apr.", "posted_date": "2026-04-01", "target_audience": "All Students", "posted_by_user_id": "U001", "category": "Exam", "priority": "High"}
]

SOPS_DATA = [
    {"sop_id": "SOP01", "category": "Attendance", "guideline": "Students must maintain a minimum of 75% attendance in every subject to be eligible for semester examinations."},
    {"sop_id": "SOP02", "category": "Attendance", "guideline": "Medical leave requires a valid certificate submitted within 3 days of rejoining."},
    {"sop_id": "SOP03", "category": "Examinations", "guideline": "Internal marks carry 40 marks and external examination carries 60 marks per subject."},
    {"sop_id": "SOP04", "category": "Examinations", "guideline": "A minimum of 40 total marks, with at least 21 in the external exam, is required to pass a subject."},
    {"sop_id": "SOP05", "category": "Examinations", "guideline": "Use of mobile phones or unfair means in the examination hall leads to disciplinary action."},
    {"sop_id": "SOP06", "category": "Assignments", "guideline": "Assignments must be submitted by the deadline; late submissions lose 10% marks per day."},
    {"sop_id": "SOP07", "category": "Conduct", "guideline": "Students must carry their ID card on campus at all times."},
    {"sop_id": "SOP08", "category": "Conduct", "guideline": "Ragging in any form is strictly prohibited and punishable as per law and college rules. Zero tolerance policy with 24/7 Helpline: 1800-180-5522."},
    {"sop_id": "SOP09", "category": "Dress Code", "guideline": "Students should wear decent, formal attire; the department T-shirt is allowed on Fridays."},
    {"sop_id": "SOP10", "category": "Laboratory", "guideline": "Students must follow lab safety rules and may not install unauthorised software on lab systems."},
    {"sop_id": "SOP11", "category": "Laboratory", "guideline": "Lab records must be completed and signed by faculty before each practical session ends."},
    {"sop_id": "SOP12", "category": "Library", "guideline": "Books may be borrowed for 14 days; a fine of Rs. 2 per day applies for overdue books. Scan ID card upon entry."},
    {"sop_id": "SOP13", "category": "Placement", "guideline": "Students must attend at least 80% of placement training sessions to be eligible for campus drives."},
    {"sop_id": "SOP14", "category": "Grievance", "guideline": "Grievances are submitted in writing to the department head and resolved within 7 working days."}
]

FAQS_DATA = [
    {"faq_id": "FAQ01", "category": "Attendance", "question": "What is the minimum attendance required?", "keywords": "attendance, minimum attendance, eligibility", "answer": "Students must maintain at least 75% attendance in every subject to be eligible for semester examinations."},
    {"faq_id": "FAQ02", "category": "Attendance", "question": "What happens if attendance is below 75%?", "keywords": "attendance shortage, low attendance, performa", "answer": "Students with attendance below 75% may not be allowed to appear for the semester exam as they will be categorized under the third proforma and will need to attend academic semesters back."},
    {"faq_id": "FAQ03", "category": "Attendance", "question": "How can I apply for leave?", "keywords": "leave, leave procedure, absence", "answer": "Students must inform in the official group created by the class advisor before taking leave. Their parents should inform the class advisor prior to the leave."},
    {"faq_id": "FAQ04", "category": "Attendance", "question": "Who approves student leave?", "keywords": "leave approval, class advisor, hod", "answer": "Leave requests are approved by the class advisor or the Head of the Department (HOD)."},
    {"faq_id": "FAQ05", "category": "Examinations", "question": "What essentials should I bring to the Examinations?", "keywords": "exam rules, hall ticket, id card", "answer": "Students must bring their hall ticket and ID card to the examination hall for semester exams. For internal tests, the college ID card is mandatory."},
    {"faq_id": "FAQ06", "category": "Conduct", "question": "Are mobile phones allowed in class?", "keywords": "mobile phone, phone policy, confiscation", "answer": "Mobile phones are not allowed during class hours unless permitted by faculty. Otherwise, mobile phones will be confiscated by respective departments."},
    {"faq_id": "FAQ07", "category": "Admissions", "question": "How do I apply for this college?", "keywords": "apply, admission, registration, intake", "answer": "You can apply online via the 'Admissions' portal on our website (srcw.ac.in). The deadline for Fall admissions is June 30."},
    {"faq_id": "FAQ08", "category": "Finance", "question": "What is the fee structure for B.Sc Computer Science?", "keywords": "fee, bsc cs, cost, payment", "answer": "The annual tuition fee for B.Sc Computer Science programs is approximately ₹38,000 to ₹40,000. This does not include hostel or semester exam fees."},
    {"faq_id": "FAQ09", "category": "Examinations", "question": "When are the final semester exams?", "keywords": "exam date, timetable, schedule", "answer": "The final exams are scheduled to begin in mid-April to May. You can download the timetable from the college official website srcw.ac.in."},
    {"faq_id": "FAQ10", "category": "Facilities", "question": "Does the college have hostel facilities?", "keywords": "hostel, stay, dorm, accommodation", "answer": "Yes, we offer secure hostel facilities for students with 24/7 security, purified drinking water, warden supervision, and high-speed Wi-Fi."},
    {"faq_id": "FAQ11", "category": "Placement", "question": "What are the placement records?", "keywords": "placement, jobs, salary, package, recruiters", "answer": "Over 90.5% of eligible students are placed, with packages up to 5.5 LPA. Top recruiters include Deloitte, Cognizant, KGISL, [24]7.ai, GEP, and Infosys."},
    {"faq_id": "FAQ12", "category": "Admissions", "question": "What documents are needed for admission?", "keywords": "documents, certificate, transcripts, id proof", "answer": "You need 10th and 12th marksheets/transcripts, Transfer Certificate (TC), Conduct Certificate, Community Certificate, Aadhar Card, and 4 passport-size photographs."},
    {"faq_id": "FAQ13", "category": "Admissions", "question": "What is the minimum percentage required for admission?", "keywords": "eligibility, cutoff, marks criteria", "answer": "A minimum of 55-60% in Higher Secondary (+2) with Mathematics/Computer Science is typically required for computer science courses."},
    {"faq_id": "FAQ14", "category": "Finance", "question": "Do you offer scholarships?", "keywords": "scholarship, financial aid, concession", "answer": "Yes, merit-based scholarships up to 50% tuition fee concession are offered for high scorers, as well as government schemes like Pudhumai Penn, Moovalur Ramamirtham, and community scholarships."},
    {"faq_id": "FAQ15", "category": "Finance", "question": "Can I pay fees in installments?", "keywords": "installment, fee payment, semester payment", "answer": "Yes, tuition fees can be paid in two equal installments at the beginning of each semester upon approval from the Accounts Office."},
    {"faq_id": "FAQ16", "category": "Facilities", "question": "What are the library timings?", "keywords": "library hours, book borrowing, timings", "answer": "The Central Library is open from 8:30 AM to 5:00 PM on all working weekdays. Students scan their ID cards at the gate register."},
    {"faq_id": "FAQ17", "category": "Facilities", "question": "Is there a canteen on campus?", "keywords": "canteen, cafeteria, food, angaadi", "answer": "Yes, we have a main cafeteria serving healthy vegetarian and snack options, and 'Angaadi'—an entrepreneurial snack hub managed by EDC students."},
    {"faq_id": "FAQ18", "category": "Facilities", "question": "Are there sports facilities?", "keywords": "sports, badminton, volleyball, athletics", "answer": "The campus has badminton, volleyball, and throwball courts, plus indoor board games. Major athletic track events (100m, 200m, high jump, shot put) take place at Nehru Stadium."},
    {"faq_id": "FAQ19", "category": "Conduct", "question": "How do I get my ID card?", "keywords": "id card, identity card, student affairs", "answer": "ID cards are issued by the Student Affairs / Academic Section during the first two weeks of enrollment upon submitting admission receipts."},
    {"faq_id": "FAQ20", "category": "Conduct", "question": "What is the anti-ragging policy?", "keywords": "anti ragging, helpline, complaints", "answer": "We enforce strict zero-tolerance anti-ragging policies. Immediate reporting can be made to the 24/7 National Anti-Ragging Helpline at 1800-180-5522 or the college anti-ragging squad."},
    {"faq_id": "FAQ21", "category": "Facilities", "question": "Does the college provide bus transport?", "keywords": "bus, transport, routes, shuttle", "answer": "Yes, the college operates buses across 15+ major arterial routes throughout Coimbatore, Tiruppur, and surrounding areas with monthly transport passes."},
    {"faq_id": "FAQ22", "category": "General", "question": "Where is the college located?", "keywords": "location, address, route, siddhapudur", "answer": "The college is located at #395, Sarojini Naidu Road, Siddhapudur, Coimbatore - 641044, Tamil Nadu."},
    {"faq_id": "FAQ23", "category": "General", "question": "What is the official contact number and website?", "keywords": "contact number, phone, email, website", "answer": "Phone: 0422-2243624, 7373144766. Official Website: www.srcw.ac.in. Email: info@srcw.ac.in."},
    {"faq_id": "FAQ24", "category": "Administration", "question": "Who is the Principal of the college?", "keywords": "principal, dr k chitra, leadership", "answer": "Our Principal is Dr. K. Chitra, M.Com, MBA, M.Phil, Ph.D., with 30+ years of academic and administrative experience, 75+ research publications, and multiple funded research grants."},
    {"faq_id": "FAQ25", "category": "Accreditation", "question": "What is the college accreditation and affiliation?", "keywords": "naac, autonomous, bharathiar university, ranking", "answer": "The college is Reaccredited by NAAC with 'A+' Grade, autonomous, and affiliated to Bharathiar University. It consistently ranks in the Top 100 in national surveys by The Week, India Today, and Times B-School."},
    {"faq_id": "FAQ26", "category": "Administration", "question": "Who is the Head of the Computer Science Department?", "keywords": "hod computer science, dr tajunisha, dr rani", "answer": "Dr. N. Tajunisha (MCA, M.Phil, Ph.D.) and Dr. V. G. Rani (MCA, M.Phil, Ph.D.) lead the Department of Computer Science."},
    {"faq_id": "FAQ27", "category": "Academics", "question": "What are the college class and prayer timings?", "keywords": "timings, class hours, prayer, break", "answer": "Classes run from 9:00 AM to 2:00 PM. Morning prayer and mudras for mindfulness are conducted from 9:00 AM to 9:10 AM. CS Department break is from 11:40 AM to 12:10 PM."},
    {"faq_id": "FAQ28", "category": "Academics", "question": "How many computer and science laboratories are available?", "keywords": "labs, computer lab, laboratory facilities", "answer": "There are 6 fully equipped, air-conditioned laboratories with high-speed internet, modern compilers, database tools, and ICT support."},
    {"faq_id": "FAQ29", "category": "Activities", "question": "What student clubs and extracurricular activities exist?", "keywords": "clubs, edc, cyber security, nss, ncc, tedx, rotaract", "answer": "Active clubs include Women's Empowerment Cell, Entrepreneurship Development Cell (EDC), Cyber Security Club, TEDx, Music, Photography, Dance, NSS, NCC, Youth Red Cross, and Yuva Club."},
    {"faq_id": "FAQ30", "category": "Activities", "question": "What is Hackathon and who can participate?", "keywords": "hackathon, coding competition, sih", "answer": "Hackathons are time-bound software building contests. All interested students, especially from Computer Science and IT, can participate. Our college won National Awards at Smart India Hackathon (SIH 2019 & SIH 2022)."}
]

def export_csvs(data_dir):
    os.makedirs(data_dir, exist_ok=True)
    
    datasets = [
        ("students.csv", STUDENTS_DATA),
        ("users.csv", USERS_DATA),
        ("subjects.csv", SUBJECTS_DATA),
        ("marks.csv", MARKS_DATA),
        ("attendance.csv", ATTENDANCE_DATA),
        ("observations.csv", OBSERVATIONS_DATA),
        ("announcements.csv", ANNOUNCEMENTS_DATA),
        ("sops.csv", SOPS_DATA),
        ("faqs.csv", FAQS_DATA)
    ]
    
    for filename, rows in datasets:
        filepath = os.path.join(data_dir, filename)
        if rows:
            keys = rows[0].keys()
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(rows)
            print(f"Exported {len(rows)} records to {filepath}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data")
    export_csvs(data_path)
