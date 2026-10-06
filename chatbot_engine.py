"""
Conversational AI Chatbot Engine - 'Nova'
Emulates ChatGPT-4 mini with natural humanoid conversation, empathy,
and deep contextual awareness of college SOPs, FAQs, and student records.
"""
import os
import re
from db import db_manager
from ml_analytics import analytics_engine

# Check if OpenAI is available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class HumanoidChatbot:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.api_key) if (OPENAI_AVAILABLE and self.api_key) else None

    def process_message(self, user_message, session_user=None):
        """
        Main entry point for conversational agent.
        Takes message and current logged in user context.
        """
        user_message_clean = user_message.strip()
        if not user_message_clean:
            return {
                "reply": "I'm right here! Feel free to ask me anything about your courses, marks, attendance, or college guidelines.",
                "sources": []
            }

        # 1. Gather Context based on user role and message
        context = self._build_user_context(session_user, user_message_clean)
        
        # 2. Search SOPs & FAQs for grounded institutional knowledge
        knowledge_matches = analytics_engine.search_knowledge_base(user_message_clean, top_k=3)
        
        # 3. If external OpenAI API Key is present, call GPT-4o-mini
        if self.client and self.api_key:
            try:
                reply = self._call_openai_gpt4_mini(user_message_clean, session_user, context, knowledge_matches)
                return {
                    "reply": reply,
                    "sources": [k["title"] for k in knowledge_matches[:2]]
                }
            except Exception as e:
                print(f"[OpenAI Call Fallback]: {e}")

        # 4. Built-in Humanoid Neural Engine (mimics GPT-4 mini behavior with natural conversational flow)
        reply = self._generate_humanoid_response(user_message_clean, session_user, context, knowledge_matches)
        
        return {
            "reply": reply,
            "sources": [k["title"] for k in knowledge_matches[:2]] if knowledge_matches else []
        }

    def _build_user_context(self, session_user, query):
        if not session_user:
            return {"role": "Guest"}

        role = session_user.get("role", "Student")
        context = {"role": role, "name": session_user.get("full_name")}

        if role == "Student" and session_user.get("student_id"):
            student_id = session_user["student_id"]
            analytics = analytics_engine.get_student_analytics(student_id)
            context["analytics"] = analytics
        elif role in ["Faculty", "Admin"]:
            # Check if query asks about a specific student like CS007 or Arjun
            students = db_manager.get_all_students()
            for s in students:
                if s["student_id"].lower() in query.lower() or s["full_name"].lower() in query.lower():
                    context["inspected_student"] = analytics_engine.get_student_analytics(s["student_id"])
                    break

        return context

    def _call_openai_gpt4_mini(self, query, session_user, context, knowledge_matches):
        system_prompt = (
            "You are Nova, an intelligent, empathetic, and professional AI Campus Advisor for "
            "Sri Ramakrishna College of Arts and Science for Women (Autonomous, Affiliated to Bharathiar University, NAAC A+). "
            "You possess the demeanor and conversational fluidity of ChatGPT-4 mini: warm, polite, highly articulate, "
            "encouraging, and context-aware. "
            "Always ground your responses in the provided verified institutional data, college SOPs, and student analytics. "
            "If asked about attendance or marks, provide clear and caring guidance. If attendance is below 75%, gently remind "
            "them about the semester eligibility requirement and 3rd proforma. "
            "Keep formatting clean with friendly bullet points or short paragraphs where appropriate."
        )

        kb_context = "\n".join([f"[{k['type']}] {k['title']}: {k['content']}" for k in knowledge_matches])
        
        user_info = f"Current User: {session_user.get('full_name')} ({session_user.get('role')})\n"
        if "analytics" in context:
            a = context["analytics"]
            user_info += f"Student ID: {a['student']['student_id']}, Course: {a['student']['course']}, Overall Attendance: {a['overall_attendance']}%, CGPA: {a['cgpa']}, Arrears: {a['arrears']}\n"
            if a["needs_improvement"]:
                user_info += f"Subjects needing attention: {[s['subject_name'] for s in a['needs_improvement']]}\n"

        prompt = f"{user_info}\nInstitutional Knowledge:\n{kb_context}\n\nStudent/User Query: {query}"

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=450
        )
        return response.choices[0].message.content

    def _generate_humanoid_response(self, query, session_user, context, knowledge_matches):
        """
        High-fidelity humanoid generator that mirrors ChatGPT-4 mini style:
        - Conversational openings and empathy
        - Precise factual retrieval from SOPs/FAQs
        - Direct tailored insights for student's own marks and attendance
        - Proactive, helpful closing remarks
        """
        q = query.lower()
        first_name = session_user.get("full_name", "").split()[0] if session_user else "there"
        analytics = context.get("analytics")

        # 1. Greetings & Small Talk
        if any(w in q for w in ["hi", "hello", "hey", "good morning", "good afternoon", "greetings"]):
            if session_user and session_user.get("role") == "Student" and analytics:
                att = analytics["overall_attendance"]
                status_note = f"Your overall attendance is currently sitting at **{att}%**"
                if att < 75.0:
                    status_note += " (a quick reminder that we'll want to get that back above the 75% examination threshold!)."
                else:
                    status_note += "—great job staying consistent!"
                return (
                    f"Hello {first_name}! 👋 It's wonderful to see you today. {status_note}\n\n"
                    f"I'm Nova, your AI campus guide. Whether you'd like to check your subject marks, review college SOPs, "
                    f"or ask about upcoming announcements and exam schedules, I'm here to help. What's on your mind?"
                )
            elif session_user and session_user.get("role") in ["Faculty", "Admin"]:
                return (
                    f"Hello {first_name}! Hope you're having a productive day on campus. 👩‍🏫\n\n"
                    f"I'm Nova, your academic analytics and college assistant. You can ask me to look up student academic records, "
                    f"check class performance trends, or review department SOPs. How may I assist you today?"
                )
            else:
                return (
                    f"Hello {first_name}! 👋 Welcome to Sri Ramakrishna College of Arts and Science for Women.\n\n"
                    f"I'm Nova, your campus companion. I can help answer questions regarding college admissions, exam guidelines, "
                    f"facilities, bus transport, hostels, and academic rules. How can I assist you today?"
                )

        # 2. Student Personalized Query: Attendance
        if any(w in q for w in ["my attendance", "attendance percentage", "am i short", "attendance shortage", "shortage"]) and analytics:
            att = analytics["overall_attendance"]
            classes_att = analytics["classes_attended"]
            total_cls = analytics["total_classes"]
            
            if att < 75.0:
                shortfall_msg = (
                    f"⚠️ **Attention Required:** Your current overall attendance is **{att}%** ({classes_att}/{total_cls} classes), "
                    f"which is below the mandatory **75% semester requirement**.\n\n"
                    f"According to College SOP 01 and 02:\n"
                    f"• You are currently under the attendance shortage watch list.\n"
                    f"• If attendance remains below 75%, students fall under the 3rd proforma and cannot sit for the semester end examinations.\n"
                    f"• **Recommended Action:** Please connect with your faculty mentor or class advisor right away to review your attendance make-up sessions or submit verified medical certificates if applicable."
                )
            else:
                shortfall_msg = (
                    f"🎉 **Great Standing:** Your overall attendance is **{att}%** ({classes_att}/{total_cls} classes attended), "
                    f"well above the 75% college examination eligibility threshold!\n\n"
                    f"Keep up this consistent presence—regular attendance is strongly correlated with top grades in our semester examinations."
                )

            # Add breakdown of lowest subject
            att_breakdown = analytics["attendance_breakdown"]
            if att_breakdown:
                lowest_sub = min(att_breakdown, key=lambda x: x["attendance_percentage"])
                shortfall_msg += f"\n\n**Quick Subject Note:** Your lowest attendance is in **{lowest_sub['subject_name']}** at **{lowest_sub['attendance_percentage']}%**."
            return shortfall_msg

        # 3. Student Personalized Query: Marks, CGPA, Performance, or Improvement
        if any(w in q for w in ["my marks", "my score", "cgpa", "percentage", "improve", "improvement", "arrear", "result"]) and analytics:
            cgpa = analytics["cgpa"]
            avg_m = analytics["avg_marks"]
            arrears = analytics["arrears"]
            needs_imp = analytics["needs_improvement"]
            
            resp = f"Here is a summary of your academic progress, {first_name}:\n\n"
            resp += f"• **Estimated CGPA:** **{cgpa} / 10.0** (Average: **{avg_m}%**)\n"
            resp += f"• **Status:** {'✅ All Subjects Cleared' if arrears == 0 else f'⚠️ {arrears} Arrear / Backlog Subject(s)'}\n\n"

            if needs_imp:
                resp += "**Key Subjects to Focus On for Improvement:**\n"
                for sub in needs_imp:
                    status_text = "Failed (Below Pass Criteria)" if sub["result"] == "Fail" else "Needs Improvement (< 65%)"
                    resp += f"- **{sub['subject_name']}**: Score of {sub['total_marks']}/100 (Grade {sub['grade']}) — *{status_text}*\n"
                resp += "\n💡 **Nova's Tip:** Revisit past lab exercises and unit problem sets for these subjects. Don't hesitate to utilize faculty office hours before the next internal assessment!"
            else:
                resp += "🌟 **Outstanding Performance!** You are maintaining solid scores across all your subjects. Keep this momentum going for upcoming campus placement drives."

            if analytics.get("synthesized_observation"):
                resp += f"\n\n**Faculty Mentor's Observation:**\n\"{analytics['synthesized_observation']}\""

            return resp

        # 4. Faculty/Admin inspecting a specific student
        if "inspected_student" in context:
            st_data = context["inspected_student"]
            st_profile = st_data["student"]
            return (
                f"Here is the academic performance profile for **{st_profile['full_name']}** ({st_profile['student_id']}):\n\n"
                f"• **Department & Year:** {st_profile['department']}, Year {st_profile['year']} (Semester {st_profile['semester']})\n"
                f"• **Overall Attendance:** **{st_data['overall_attendance']}%** "
                f"{'⚠️ (Shortage Alert: < 75%)' if st_data['attendance_shortage'] else '✅ (Good Standing)'}\n"
                f"• **Academic CGPA:** **{st_data['cgpa']} / 10.0** (Average: {st_data['avg_marks']}%)\n"
                f"• **Arrears:** {st_data['arrears']}\n"
                f"• **Risk Level:** **{st_data['risk_assessment']['level']}** (Score: {st_data['risk_assessment']['score']}/100)\n\n"
                f"**Faculty Remarks Summary:**\n{st_data['synthesized_observation']}\n\n"
                f"**Action Recommendation:** {st_data['risk_assessment']['recommendation']}"
            )

        # 5. Grounded Search in SOPs & FAQs
        if knowledge_matches and knowledge_matches[0]["confidence"] > 10.0:
            top_match = knowledge_matches[0]
            answer = top_match["content"]
            category = top_match["category"]
            
            # Format in friendly conversational ChatGPT-4 mini tone
            response = f"Here is the official information regarding **{top_match['title']}**:\n\n"
            response += f"{answer}\n\n"
            
            # Add context advice
            if category == "Attendance":
                response += "💡 *Remember that regular attendance is mandatory to stay eligible for all university and autonomous semester exams.*"
            elif category == "Examinations":
                response += "📋 *Keep your Hall Ticket and College ID card handy for all exam sessions. Mobile phones and smart devices are strictly prohibited.*"
            elif category == "Placement":
                response += "🚀 *Our placement cell organizes active coaching in aptitude and coding. Maintaining an 80%+ training attendance record is key to campus drive eligibility!*"
            elif category == "Conduct":
                response += "🛡️ *Our college maintains an absolute zero-tolerance policy against ragging. Helpline: 1800-180-5522.*"

            if len(knowledge_matches) > 1 and knowledge_matches[1]["confidence"] > 15.0:
                second = knowledge_matches[1]
                response += f"\n\n**Related Guideline:**\n• **{second['title']}**: {second['content']}"

            return response

        # 6. Conversational Fallback
        return (
            f"I understand your question about '{query}'. While I don't see an exact policy match in our latest circulars, "
            f"here is what I can share:\n\n"
            f"Sri Ramakrishna College of Arts and Science for Women (SRCW) adheres strictly to the academic regulations of Bharathiar University and our autonomous curriculum. "
            f"For specific administrative requests, you can contact the Administration Office at **0422-2243624** / **7373144766**, "
            f"or check with your Department Head.\n\n"
            f"Can I help you with details about **Attendance Rules**, **Exam Passing Criteria**, **College Timings**, or your **Personal Marks**?"
        )

chatbot_engine = HumanoidChatbot()
