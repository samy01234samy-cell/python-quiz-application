================================================================
  ⚡ QUIZ APP PRO — Setup Guide
  Database Management System | Operating Systems Quiz App
================================================================

REQUIREMENTS
─────────────
• Python 3.8 or higher
• Command Prompt (Windows) or Terminal

QUICK START (Windows — Notepad + Command Prompt)
─────────────────────────────────────────────────

Step 1: Install Flask
  Open Command Prompt and type:
    pip install flask

Step 2: Run the App
  Navigate to the quiz_app folder:
    cd path\to\quiz_app

  Then run:
    python app.py

Step 3: Open in Browser
  Go to: http://127.0.0.1:5000

═══════════════════════════════════════════════════
  LOGIN CREDENTIALS
═══════════════════════════════════════════════════

  ADMIN LOGIN
  ────────────
  Username : admin
  Password : admin123

  STUDENT LOGIN
  ──────────────
  Register a new account at /register
  Then login at /register

═══════════════════════════════════════════════════
  FEATURES
═══════════════════════════════════════════════════

  ✅ Admin Panel
     • View all registered students
     • Add / Delete questions
     • View all student scores
     • Pre-loaded with 50 real questions per category

  ✅ Student Panel
     • Register / Login with personal account
     • Take DBMS or OS quiz (10 shuffled questions)
     • See result with percentage & grade
     • View personal attempt history

  ✅ Leaderboard
     • Top 20 students ranked by best score %

  ✅ Beautiful UI
     • Dark mode cyberpunk design
     • Animated cards and transitions
     • Progress bars, badges, and score circles
     • Fully responsive for mobile

═══════════════════════════════════════════════════
  DATABASE
═══════════════════════════════════════════════════

  File  : quiz.db  (SQLite — auto-created on first run)
  Tables:
    users      — student and admin accounts
    categories — DBMS, OS
    questions  — question bank (50 per category)
    attempts   — score history for all students

  Foreign key constraints are enforced for consistency.
  No data is lost — all attempts are permanently recorded.

═══════════════════════════════════════════════════
  FOLDER STRUCTURE
═══════════════════════════════════════════════════

  quiz_app/
  ├── app.py                  ← Main application (Python/Flask)
  ├── requirements.txt        ← Python packages needed
  ├── README.txt              ← This file
  ├── quiz.db                 ← SQLite database (auto-created)
  ├── static/
  │   └── css/
  │       └── style.css       ← All styling (dark mode UI)
  └── templates/
      ├── login.html
      ├── register.html
      ├── student_dashboard.html
      ├── quiz.html
      ├── result.html
      ├── leaderboard.html
      ├── admin_dashboard.html
      ├── admin_questions.html
      ├── admin_scores.html
      └── add_question.html

================================================================
