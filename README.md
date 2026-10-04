# CampusAI — College Chatbot

CampusAI is a Flask-based college information chatbot. Students can ask questions in a chat interface, choose from ten common college topics, and review answers. Student questions and responses are stored in a local SQLite database and shown in the Admin history page.

## Features

- Interactive, responsive dashboard and chat interface.
- Ten built-in FAQ topics:
  - Attendance
  - Examinations
  - Library
  - Placements
  - Fees
  - Hostel
  - Transport
  - Scholarships
  - Departments
  - College contact information
- Free-text questions, with a helpful fallback when the chatbot does not recognize a topic.
- Dashboard statistics for total questions, answered questions, and topics.
- Admin page showing saved questions, answers, and timestamps, with an option to delete individual history entries.
- SQLite database created locally as `college_bot.db`.

> The chatbot uses predefined keyword-based answers; it does not connect to an external AI service. For official policies, dates, contact details, or other current information, students should confirm with the relevant college office.

## Requirements

- Python 3.10 or later
- pip

## Setup and run

From the project directory, create and activate a virtual environment, install Flask, and start the development server:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

The first run creates `college_bot.db` in the project directory. The database is local and excluded from Git, so saved question history is not included when the project is cloned.

## Pages and API

| Path | Description |
| --- | --- |
| `/` | Student dashboard and chatbot |
| `/admin` | Saved student question and answer history |
| `POST /api/chat` | Accepts JSON such as `{"message": "Where can I find the exam timetable?"}` and returns a JSON answer |
| `GET /api/stats` | Returns dashboard counts |

The admin page currently has no authentication. Run this development application only in a trusted environment; add access controls before exposing it to a network or deploying it publicly.

## Project structure

```text
.
├── app.py
├── requirements.txt
├── static/
│   ├── script.js
│   └── style.css
└── templates/
    ├── admin.html
    └── index.html
```
