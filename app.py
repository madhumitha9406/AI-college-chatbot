from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import sqlite3
import re

app = Flask(__name__, template_folder="templates", static_folder="static")

DATABASE = "college_bot.db"

FAQS = [
    {
        "icon": "📚",
        "category": "Attendance",
        "question": "What is the minimum attendance requirement?",
        "keywords": ("attendance", "absent", "present"),
        "answer": (
            "📚 Attendance Information\n\n"
            "Attendance requirements are set by your college and university. "
            "Check your student handbook or ask the academic office for the "
            "current minimum and how to report an absence."
        ),
    },
    {
        "icon": "📝",
        "category": "Examinations",
        "question": "Where can I find the exam timetable?",
        "keywords": ("exam", "exams", "examination", "examinations", "semester", "internal", "timetable"),
        "answer": (
            "📝 Examination Information\n\n"
            "The examination section publishes timetables and instructions "
            "through official college notices or the student portal. Check "
            "those channels for the latest schedule."
        ),
    },
    {
        "icon": "📖",
        "category": "Library",
        "question": "How can I find library hours and resources?",
        "keywords": ("library", "book", "books"),
        "answer": (
            "📖 Library Information\n\n"
            "The library provides textbooks, reference books and digital "
            "learning resources. For current opening hours, borrowing rules "
            "or renewals, check the library notice or ask the library desk."
        ),
    },
    {
        "icon": "💼",
        "category": "Placements",
        "question": "How do I register for campus placements?",
        "keywords": ("placement", "placements", "job", "jobs", "company", "companies", "interview", "interviews", "recruitment"),
        "answer": (
            "💼 Placement Information\n\n"
            "Contact the placement cell to register, check eligibility and "
            "learn about upcoming recruitment drives. Keep your resume and "
            "student details up to date."
        ),
    },
    {
        "icon": "💳",
        "category": "Fees",
        "question": "How can I pay my college fees?",
        "keywords": ("fee", "fees", "payment", "tuition"),
        "answer": (
            "💳 Fee Information\n\n"
            "Use the official college fee portal or contact the accounts "
            "office for payment options and deadlines. Keep your payment "
            "receipt for reference."
        ),
    },
    {
        "icon": "🏠",
        "category": "Hostel",
        "question": "How do I apply for a hostel room?",
        "keywords": ("hostel", "room", "mess", "warden"),
        "answer": (
            "🏠 Hostel Information\n\n"
            "Contact the hostel office or warden for applications, room "
            "availability, fees and mess information. They can also provide "
            "the current hostel rules."
        ),
    },
    {
        "icon": "🚌",
        "category": "Transport",
        "question": "Where can I check bus routes and timings?",
        "keywords": ("bus", "transport", "route", "routes"),
        "answer": (
            "🚌 Transport Information\n\n"
            "The transport department manages campus bus routes and timings. "
            "Contact them for the current route list, pickup points and any "
            "schedule changes."
        ),
    },
    {
        "icon": "🎓",
        "category": "Scholarships",
        "question": "How can I apply for a scholarship?",
        "keywords": ("scholarship", "scholarships", "financial aid", "grant"),
        "answer": (
            "🎓 Scholarship Information\n\n"
            "Ask the scholarship or student welfare office about current "
            "scholarships, eligibility, deadlines and required documents. "
            "Use official college or government application links."
        ),
    },
    {
        "icon": "🏫",
        "category": "Departments",
        "question": "How can I find my department or faculty?",
        "keywords": ("department", "departments", "faculty", "computer", "course", "courses"),
        "answer": (
            "🏫 Department Information\n\n"
            "Check the college department directory or contact your "
            "department office for faculty details, course information and "
            "room locations."
        ),
    },
    {
        "icon": "☎️",
        "category": "Contact",
        "question": "How can I contact the college office?",
        "keywords": ("contact", "office", "phone", "email", "address"),
        "answer": (
            "☎️ Contact Information\n\n"
            "For official phone numbers, email addresses and office hours, "
            "check the college website or contact the administrative office."
        ),
    },
]


# ---------------- DATABASE ----------------

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ---------------- AI CHATBOT ----------------

def get_answer(question):

    question = question.lower().strip()

    # Greeting
    if re.search(r"\b(hello|hi|hey|hai)\b", question):

        return (
            "Hello! 👋 I am CampusAI. "
            "How can I help you today?"
        )

    for faq in FAQS:
        if any(
            re.search(r"\b" + re.escape(keyword) + r"\b", question)
            for keyword in faq["keywords"]
        ):
            return faq["answer"]

    # Unknown question
    return (
        "🤔 I don't have an answer for that yet.\n\n"
        "Try one of the 10 college topics below, or contact the relevant "
        "college office for a specific answer."
    )


# ---------------- HOME PAGE ----------------

@app.route("/")
def home():

    return render_template("index.html", faqs=FAQS)


# ---------------- CHAT API ----------------

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Send your message as JSON."
        }), 400

    message = data.get("message", "")

    if not isinstance(message, str):
        return jsonify({
            "error": "Your message must be text."
        }), 400

    question = message.strip()

    if not question:
        return jsonify({
            "error": "Please type your question."
        }), 400

    answer = get_answer(question)

    connection = get_db()

    connection.execute(
        """
        INSERT INTO queries
        (question, answer, created_at)
        VALUES (?, ?, ?)
        """,
        (
            question,
            answer,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )

    connection.commit()
    connection.close()

    return jsonify({
        "answer": answer
    })


# ---------------- STATISTICS ----------------

@app.route("/api/stats")
def stats():

    connection = get_db()

    total = connection.execute(
        "SELECT COUNT(*) AS count FROM queries"
    ).fetchone()["count"]

    connection.close()

    return jsonify({
        "queries": total,
        "answered": total,
        "topics": len(FAQS)
    })


# ---------------- ADMIN ----------------

@app.route("/admin")
def admin():

    connection = get_db()

    queries = connection.execute(
        """
        SELECT id, question, answer, created_at
        FROM queries
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template(
        "admin.html",
        queries=queries
    )


@app.route("/admin/delete/<int:query_id>", methods=["POST"])
def delete_query(query_id):

    connection = get_db()
    cursor = connection.execute(
        "DELETE FROM queries WHERE id = ?",
        (query_id,)
    )
    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return "Question not found.", 404

    return redirect(url_for("admin"))


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":

    init_database()

    app.run(debug=True)