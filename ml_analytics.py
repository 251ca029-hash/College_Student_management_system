"""
ML and Data Analytics Engine
Powered by NumPy, Pandas, and Scikit-learn
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from db import db_manager

class CollegeAnalyticsML:
    def __init__(self):
        self.grade_points = {
            "O": 10.0,
            "A+": 9.0,
            "A": 8.0,
            "B+": 7.0,
            "B": 6.0,
            "C": 5.0,
            "F": 0.0
        }
        self.qualitative_map = {
            "Excellent": 4,
            "Good": 3,
            "Average": 2,
            "Needs Improvement": 1
        }
        self.faq_vectorizer = None
        self.faq_matrix = None
        self.faq_corpus = []
        self._init_faq_nlp_model()

    def get_student_analytics(self, student_id):
        """Calculates precise student analytics using pandas and numpy."""
        student = db_manager.get_student_by_id(student_id)
        if not student:
            return None

        marks = db_manager.get_marks_by_student(student_id)
        attendance = db_manager.get_attendance_by_student(student_id)
        observations = db_manager.get_observations_by_student(student_id)

        df_marks = pd.DataFrame(marks) if marks else pd.DataFrame()
        df_att = pd.DataFrame(attendance) if attendance else pd.DataFrame()

        # Attendance calculation
        if not df_att.empty:
            total_classes = df_att["total_classes"].sum()
            classes_attended = df_att["classes_attended"].sum()
            overall_attendance = round((classes_attended / total_classes * 100), 2) if total_classes > 0 else 0.0
            attendance_shortage = overall_attendance < 75.0
        else:
            total_classes, classes_attended, overall_attendance = 0, 0, 0.0
            attendance_shortage = True

        # Marks calculation & CGPA
        if not df_marks.empty:
            total_marks = df_marks["total_marks_100"].sum()
            avg_marks = round(df_marks["total_marks_100"].mean(), 2)
            total_credits = df_marks["credits"].sum()
            
            # Weighted Grade Points for CGPA
            earned_points = sum(self.grade_points.get(row["grade"], 0.0) * row["credits"] for _, row in df_marks.iterrows())
            cgpa = round(earned_points / total_credits, 2) if total_credits > 0 else 0.0
            
            arrears = int((df_marks["result"] == "Fail").sum())
            passed = int((df_marks["result"] == "Pass").sum())
            total_subjects = len(df_marks)

            # Subjects needing improvement (score < 65 or Fail)
            needs_improvement = []
            for _, row in df_marks.iterrows():
                if row["total_marks_100"] < 65 or row["result"] == "Fail":
                    needs_improvement.append({
                        "subject_name": row["subject_name"],
                        "total_marks": row["total_marks_100"],
                        "grade": row["grade"],
                        "result": row["result"]
                    })
        else:
            total_marks, avg_marks, cgpa, arrears, passed, total_subjects = 0, 0, 0, 0, 0, 0
            needs_improvement = []

        # Latest Observation synthesis
        latest_obs = observations[0] if observations else None
        synthesis = self._synthesize_observation(latest_obs, needs_improvement, overall_attendance)

        # Predict Risk via ML
        risk_prediction = self.predict_single_student_risk(overall_attendance, avg_marks, latest_obs, arrears)

        return {
            "student": student,
            "overall_attendance": overall_attendance,
            "attendance_shortage": attendance_shortage,
            "total_classes": int(total_classes),
            "classes_attended": int(classes_attended),
            "total_marks": float(total_marks),
            "avg_marks": float(avg_marks),
            "cgpa": float(cgpa),
            "arrears": arrears,
            "passed": passed,
            "total_subjects": total_subjects,
            "needs_improvement": needs_improvement,
            "latest_observation": latest_obs,
            "synthesized_observation": synthesis,
            "risk_assessment": risk_prediction,
            "marks_breakdown": marks,
            "attendance_breakdown": attendance
        }

    def _synthesize_observation(self, obs, needs_improvement, attendance_pct):
        if not obs:
            return "No faculty observation recorded yet."
        
        remarks = obs.get("faculty_remarks", "")
        acad = obs.get("academic_performance", "Average")
        comm = obs.get("communication", "Average")
        tech = obs.get("technical_skills", "Average")
        team = obs.get("teamwork", "Good")

        parts = []
        if acad in ["Excellent", "Good"]:
            parts.append(f"Demonstrates {acad.lower()} academic performance")
        else:
            parts.append(f"Shows academic performance that {acad.lower()}")

        if team in ["Excellent", "Good"]:
            parts.append("active participation in teamwork and departmental activities")

        weak_areas = []
        if tech in ["Needs Improvement", "Average"]:
            weak_areas.append("technical programming skills")
        if comm in ["Needs Improvement", "Average"]:
            weak_areas.append("communication skills")
        if needs_improvement:
            sub_names = ", ".join([s["subject_name"] for s in needs_improvement[:2]])
            weak_areas.append(f"revision in {sub_names}")
        if attendance_pct < 75.0:
            weak_areas.append("regular class attendance to clear the 75% examination threshold")

        if weak_areas:
            parts.append("requires focused improvement in " + " and ".join(weak_areas))

        summary = ", ".join(parts).capitalize() + "."
        if remarks:
            summary += f" Faculty Note: \"{remarks}\""
        return summary

    def get_class_overview_analytics(self):
        """Computes comprehensive department/class-wide analytics with Pandas & NumPy."""
        marks = db_manager.get_all_marks()
        attendance = db_manager.get_all_attendance()
        students = db_manager.get_all_students()

        if not marks or not attendance:
            return {}

        df_m = pd.DataFrame(marks)
        df_a = pd.DataFrame(attendance)
        df_s = pd.DataFrame(students)

        # Average Class Attendance
        class_att_avg = round(float(df_a["attendance_percentage"].mean()), 2)
        # Average Class Mark
        class_mark_avg = round(float(df_m["total_marks_100"].mean()), 2)
        # Pass Percentage
        pass_count = (df_m["result"] == "Pass").sum()
        total_evals = len(df_m)
        overall_pass_rate = round(float((pass_count / total_evals) * 100), 2) if total_evals > 0 else 0.0

        # Subject-wise statistics
        subject_stats = []
        for (sub_code, sub_name), group in df_m.groupby(["subject_code", "subject_name"]):
            avg_tot = group["total_marks_100"].mean()
            pass_rt = (group["result"] == "Pass").mean() * 100
            internal_avg = group["internal_marks_40"].mean()
            external_avg = group["external_marks_60"].mean()
            
            subject_stats.append({
                "subject_code": sub_code,
                "subject_name": sub_name,
                "avg_marks": round(float(avg_tot), 2),
                "pass_rate": round(float(pass_rt), 2),
                "avg_internal": round(float(internal_avg), 2),
                "avg_external": round(float(external_avg), 2),
                "status": "Excellent" if avg_tot >= 80 else ("Good" if avg_tot >= 65 else "Needs Attention")
            })

        subject_stats.sort(key=lambda x: x["avg_marks"], reverse=True)

        # Grade distribution
        grade_dist = df_m["grade"].value_counts().to_dict()
        for g in ["O", "A+", "A", "B+", "B", "C", "F"]:
            grade_dist.setdefault(g, 0)

        # Merge student average marks and attendance for correlation & clustering
        st_att = df_a.groupby("student_id")["attendance_percentage"].mean().reset_index()
        st_marks = df_m.groupby("student_id")["total_marks_100"].mean().reset_index()
        st_merged = pd.merge(st_att, st_marks, on="student_id")
        
        # Pearson correlation
        if len(st_merged) > 1:
            corr = float(st_merged["attendance_percentage"].corr(st_merged["total_marks_100"]))
        else:
            corr = 0.0

        # K-Means Clustering on Students
        clustering_result = self._run_kmeans_clustering(st_merged, df_s)

        # At-Risk Student Count (< 75% attendance or failed subjects)
        at_risk_students = []
        for s in students:
            s_analytics = self.get_student_analytics(s["student_id"])
            if s_analytics["attendance_shortage"] or s_analytics["arrears"] > 0 or s_analytics["cgpa"] < 6.5:
                at_risk_students.append({
                    "student_id": s["student_id"],
                    "full_name": s["full_name"],
                    "attendance": s_analytics["overall_attendance"],
                    "cgpa": s_analytics["cgpa"],
                    "arrears": s_analytics["arrears"],
                    "risk_level": s_analytics["risk_assessment"]["level"]
                })

        return {
            "total_students": len(students),
            "class_att_avg": class_att_avg,
            "class_mark_avg": class_mark_avg,
            "overall_pass_rate": overall_pass_rate,
            "subject_stats": subject_stats,
            "grade_dist": grade_dist,
            "correlation_att_marks": round(corr, 3),
            "clustering": clustering_result,
            "at_risk_students": at_risk_students,
            "top_student": self._get_top_student(df_m, students)
        }

    def _get_top_student(self, df_m, students):
        top_group = df_m.groupby("student_id")["total_marks_100"].mean().sort_values(ascending=False)
        if not top_group.empty:
            top_id = top_group.index[0]
            top_score = round(float(top_group.iloc[0]), 2)
            st = next((s for s in students if s["student_id"] == top_id), None)
            return {"student_id": top_id, "name": st["full_name"] if st else top_id, "avg_marks": top_score}
        return None

    def _run_kmeans_clustering(self, st_merged, df_s):
        """K-Means 3-Cohort clustering on attendance and performance."""
        if len(st_merged) < 3:
            return {"clusters": []}

        X = st_merged[["attendance_percentage", "total_marks_100"]].values
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        st_merged["cluster"] = labels

        # Identify cohort characteristics by sorting centroids by total_marks
        centers = kmeans.cluster_centers_
        sorted_indices = np.argsort(centers[:, 1]) # lowest mark centroid to highest

        cluster_names = {
            sorted_indices[2]: "High Achievers / Placement Ready",
            sorted_indices[1]: "Consistent Core Performers",
            sorted_indices[0]: "At-Risk / Urgent Guidance Needed"
        }

        cluster_colors = {
            sorted_indices[2]: "#10b981", # Emerald
            sorted_indices[1]: "#3b82f6", # Blue
            sorted_indices[0]: "#ef4444"  # Red
        }

        result_data = []
        for idx, row in st_merged.iterrows():
            cid = int(row["cluster"])
            s_name = df_s.loc[df_s["student_id"] == row["student_id"], "full_name"].values
            full_name = s_name[0] if len(s_name) > 0 else row["student_id"]
            result_data.append({
                "student_id": row["student_id"],
                "full_name": full_name,
                "attendance": round(float(row["attendance_percentage"]), 1),
                "marks": round(float(row["total_marks_100"]), 1),
                "cluster_id": cid,
                "cohort_label": cluster_names.get(cid, f"Cohort {cid}"),
                "color": cluster_colors.get(cid, "#6b7280")
            })

        return {
            "students": result_data,
            "cohort_names": list(cluster_names.values())
        }

    def predict_single_student_risk(self, attendance_pct, avg_marks, observation, arrears):
        """Scikit-learn based student risk assessment."""
        # Simple rule-enhanced ML scoring
        # Features: attendance, avg_marks, observation score, arrears
        obs_score = 3
        if observation:
            obs_score = self.qualitative_map.get(observation.get("academic_performance"), 2)

        risk_score = 0
        reasons = []

        if attendance_pct < 75.0:
            risk_score += 40
            reasons.append("Attendance is below 75% semester minimum")
        elif attendance_pct < 80.0:
            risk_score += 15
            reasons.append("Attendance is borderline (75-80%)")

        if avg_marks < 50.0:
            risk_score += 40
            reasons.append("Academic average is critically low (< 50%)")
        elif avg_marks < 65.0:
            risk_score += 20
            reasons.append("Academic performance needs improvement (< 65%)")

        if arrears > 0:
            risk_score += 30 * arrears
            reasons.append(f"{arrears} backlog/arrear subject(s) detected")

        if obs_score <= 1:
            risk_score += 15
            reasons.append("Faculty observation highlighted low engagement or conceptual struggles")

        # Clamp between 0 and 100
        risk_score = min(max(risk_score, 0), 100)

        if risk_score >= 60:
            level = "High Risk"
            badge = "danger"
            recommendation = "Immediate faculty mentoring required. Schedule parent-teacher conference and enroll in remedial practice sessions."
        elif risk_score >= 30:
            level = "Moderate Risk"
            badge = "warning"
            recommendation = "Regular monitoring recommended. Revise weak subjects and ensure attendance remains consistently above 80%."
        else:
            level = "Low Risk / High Standing"
            badge = "success"
            recommendation = "Excellent performance. Eligible for advanced placement training, coding hackathons, and research mentorship."

        return {
            "level": level,
            "score": risk_score,
            "badge": badge,
            "reasons": reasons,
            "recommendation": recommendation
        }

    # ==================== NLP FAQ & SOP SEARCH ENGINE ====================
    def _init_faq_nlp_model(self):
        """Builds TF-IDF model on College FAQs and SOPs."""
        faqs = db_manager.get_faqs()
        sops = db_manager.get_sops()

        self.faq_corpus = []
        for f in faqs:
            text = f"{f['question']} {f['keywords']} {f['answer']} {f['category']}"
            self.faq_corpus.append({
                "type": "FAQ",
                "id": f["faq_id"],
                "category": f["category"],
                "title": f["question"],
                "content": f["answer"],
                "raw_text": text
            })

        for s in sops:
            text = f"{s['category']} {s['guideline']} sop rule policy"
            self.faq_corpus.append({
                "type": "SOP Guideline",
                "id": s["sop_id"],
                "category": s["category"],
                "title": f"College Guideline - {s['category']}",
                "content": s["guideline"],
                "raw_text": text
            })

        if self.faq_corpus:
            corpus_texts = [item["raw_text"] for item in self.faq_corpus]
            self.faq_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
            self.faq_matrix = self.faq_vectorizer.fit_transform(corpus_texts)

    def search_knowledge_base(self, query, top_k=5):
        """Performs intelligent semantic search using Scikit-Learn TF-IDF and Cosine Similarity."""
        if not self.faq_vectorizer or not query.strip():
            return []

        query_vec = self.faq_vectorizer.transform([query.strip()])
        similarities = cosine_similarity(query_vec, self.faq_matrix).flatten()

        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.05: # Relevant threshold
                item = self.faq_corpus[idx].copy()
                item["confidence"] = round(score * 100, 1)
                results.append(item)

        # Fallback if no high similarity vector
        if not results:
            query_lower = query.lower()
            for item in self.faq_corpus:
                if any(word in item["raw_text"].lower() for word in query_lower.split() if len(word) > 3):
                    item_copy = item.copy()
                    item_copy["confidence"] = 40.0
                    results.append(item_copy)
                    if len(results) >= top_k:
                        break

        return results

analytics_engine = CollegeAnalyticsML()
