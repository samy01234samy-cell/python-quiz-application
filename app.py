from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'quizapp_secret_2024'
DB = 'quiz.db'

# ─────────────────────────────────────────────
#  DATABASE HELPERS
# ─────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL UNIQUE,
            password  TEXT    NOT NULL,
            role      TEXT    NOT NULL DEFAULT 'student',
            created   TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS categories (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS questions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL REFERENCES categories(id),
            question    TEXT    NOT NULL,
            opt_a       TEXT    NOT NULL,
            opt_b       TEXT    NOT NULL,
            opt_c       TEXT    NOT NULL,
            opt_d       TEXT    NOT NULL,
            answer      TEXT    NOT NULL,
            created_by  INTEGER REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS attempts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL,
            category_id INTEGER NOT NULL REFERENCES categories(id),
            score       INTEGER NOT NULL,
            total       INTEGER NOT NULL,
            taken_at    TEXT    NOT NULL
        );
    """)

    # Seed admin
    c.execute("SELECT id FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users(username,password,role,created) VALUES(?,?,?,?)",
                  ('admin','admin123','admin', datetime.now().strftime('%Y-%m-%d %H:%M')))

    # Seed categories
    for cat in ['DBMS', 'OS']:
        c.execute("SELECT id FROM categories WHERE name=?", (cat,))
        if not c.fetchone():
            c.execute("INSERT INTO categories(name) VALUES(?)", (cat,))

    conn.commit()

    # Seed questions if empty
    c.execute("SELECT COUNT(*) AS cnt FROM questions")
    if c.fetchone()['cnt'] == 0:
        seed_questions(conn)

    conn.close()

def seed_questions(conn):
    c = conn.cursor()
    c.execute("SELECT id FROM categories WHERE name='DBMS'")
    dbms_id = c.fetchone()['id']
    c.execute("SELECT id FROM categories WHERE name='OS'")
    os_id = c.fetchone()['id']

    dbms_questions = [
        ("What does DBMS stand for?","Database Management System","Data Backup Management System","Dynamic Base Management System","Database Monitoring System","A"),
        ("Which language is used to query a relational database?","SQL","HTML","XML","JSON","A"),
        ("What is a primary key?","A unique identifier for each record","A key used for encryption","The first column in a table","A foreign reference","A"),
        ("What is a foreign key?","A key that links two tables","A primary key in another database","An encrypted key","A backup key","A"),
        ("Which of these is NOT a type of SQL command?","COMPILE","SELECT","INSERT","UPDATE","A"),
        ("What does DDL stand for?","Data Definition Language","Data Deletion Language","Database Design Logic","Data Display Language","A"),
        ("What does DML stand for?","Data Manipulation Language","Data Management Language","Dynamic Manipulation Logic","Database Modeling Language","A"),
        ("Which command is used to create a table?","CREATE TABLE","MAKE TABLE","NEW TABLE","BUILD TABLE","A"),
        ("Which command removes all rows from a table without deleting the table?","TRUNCATE","DELETE","DROP","REMOVE","A"),
        ("What is normalization in DBMS?","Organizing data to reduce redundancy","Encrypting the database","Backing up data","Sorting records","A"),
        ("Which normal form removes partial dependencies?","Second Normal Form (2NF)","First Normal Form (1NF)","Third Normal Form (3NF)","BCNF","A"),
        ("What is a tuple in a relational database?","A row/record","A column","A table","A database","A"),
        ("What is an attribute in DBMS?","A column in a table","A row in a table","A database name","A table index","A"),
        ("Which SQL clause filters results?","WHERE","HAVING","ORDER BY","GROUP BY","A"),
        ("What is a JOIN in SQL?","Combining rows from two or more tables","Deleting duplicate rows","Adding a new table","Sorting results","A"),
        ("Which JOIN returns all rows from both tables?","FULL OUTER JOIN","INNER JOIN","LEFT JOIN","RIGHT JOIN","A"),
        ("What does ACID stand for in databases?","Atomicity Consistency Isolation Durability","Auto Consistency Index Durability","Atomic Control Integrity Design","Advanced Control Index Database","A"),
        ("What is a transaction in DBMS?","A unit of work performed on a database","A type of SQL query","A database backup","A security protocol","A"),
        ("What does 'Atomicity' mean in ACID?","All operations complete or none do","Data is always consistent","Operations are isolated","Data is permanently saved","A"),
        ("Which SQL command saves a transaction permanently?","COMMIT","ROLLBACK","SAVEPOINT","END","A"),
        ("What is an index in a database?","A structure to speed up data retrieval","A list of table names","A type of join","A constraint","A"),
        ("What is a view in SQL?","A virtual table based on a query","A physical backup table","A stored procedure","A trigger","A"),
        ("What is a stored procedure?","A prepared SQL code saved in the database","A view with parameters","An index on multiple columns","A database backup","A"),
        ("What is a trigger in DBMS?","Automatic action on database event","A manual SQL query","A type of index","A stored backup","A"),
        ("Which SQL function counts rows?","COUNT()","SUM()","AVG()","MAX()","A"),
        ("What is the result of SELECT DISTINCT?","Unique values only","All rows including duplicates","Sorted results","Filtered results","A"),
        ("Which clause is used with aggregate functions?","GROUP BY","ORDER BY","WHERE","HAVING","A"),
        ("What does ER model stand for?","Entity-Relationship model","Electronic Record model","Extended Relational model","Entity Record model","A"),
        ("What is cardinality in ER model?","Number of relationships between entities","Number of tables","Number of columns","Number of rows","A"),
        ("What is a deadlock in DBMS?","Two transactions waiting for each other indefinitely","A crashed database server","A corrupted table","A slow query","A"),
        ("Which command is used to modify table structure?","ALTER TABLE","MODIFY TABLE","CHANGE TABLE","UPDATE TABLE","A"),
        ("What is the purpose of HAVING clause?","Filter groups after GROUP BY","Filter rows before grouping","Sort results","Join tables","A"),
        ("What is data integrity?","Accuracy and consistency of data","Speed of data retrieval","Backup of data","Encryption of data","A"),
        ("Which isolation level prevents dirty reads?","Read Committed","Read Uncommitted","Repeatable Read","Serializable","A"),
        ("What is a composite key?","A primary key made of multiple columns","A key with special characters","An encrypted primary key","A foreign key reference","A"),
        ("What does DCL stand for?","Data Control Language","Data Creation Language","Dynamic Control Logic","Database Control Layer","A"),
        ("Which command grants permissions to a user?","GRANT","ALLOW","PERMIT","GIVE","A"),
        ("Which command removes permissions from a user?","REVOKE","DENY","REMOVE","TAKE","A"),
        ("What is concurrency control?","Managing simultaneous database access","Speeding up queries","Compressing data","Encrypting transactions","A"),
        ("What is the difference between DELETE and DROP?","DELETE removes rows, DROP removes table","They are the same","DROP removes rows, DELETE removes table","DELETE removes the database","A"),
        ("What is a schema in DBMS?","The logical structure of the database","The physical storage of data","A type of query","A backup file","A"),
        ("Which SQL keyword is used for pattern matching?","LIKE","MATCH","SIMILAR","FIND","A"),
        ("What is referential integrity?","Foreign key must reference existing primary key","All data must be unique","No null values allowed","All tables must be joined","A"),
        ("What is the purpose of ORDER BY clause?","Sort query results","Filter results","Group results","Join tables","A"),
        ("Which aggregate function finds the average?","AVG()","MEAN()","AVERAGE()","SUM()/COUNT()","A"),
        ("What is a self-join?","A table joined with itself","Joining two identical tables","A recursive query","A circular reference","A"),
        ("What does NULL represent in SQL?","An unknown or missing value","Zero","Empty string","False","A"),
        ("What is the purpose of the BETWEEN operator?","Filter values within a range","Check for NULL values","Pattern matching","Joining tables","A"),
        ("What is a subquery?","A query nested inside another query","A stored procedure","A type of view","A database trigger","A"),
        ("What is database replication?","Copying database to multiple servers","Backing up one table","Encrypting the database","Removing duplicate records","A"),
    ]

    os_questions = [
        ("What is an Operating System?","Software that manages hardware and software resources","A type of hardware","A programming language","A database system","A"),
        ("What does CPU stand for?","Central Processing Unit","Central Programming Unit","Computer Processing Unit","Core Processing Utility","A"),
        ("What is a process in OS?","A program in execution","A file on disk","A hardware component","A network connection","A"),
        ("What is a thread?","Lightweight unit of process execution","A heavy process","A type of file","A memory block","A"),
        ("What is multiprogramming?","Running multiple programs simultaneously","Running one program at a time","A type of memory","A scheduling algorithm","A"),
        ("What is time-sharing OS?","Multiple users share CPU time","One user uses all resources","A real-time system","A batch system","A"),
        ("What is the kernel?","Core part of the OS","The user interface","A type of process","A file system","A"),
        ("What is virtual memory?","Using disk space as RAM extension","Physical RAM only","Cache memory","Register memory","A"),
        ("What is paging in OS?","Dividing memory into fixed-size pages","Sorting files","A scheduling method","A type of interrupt","A"),
        ("What is segmentation in OS?","Dividing memory into variable-size segments","A paging technique","A type of process","File organization","A"),
        ("What is a deadlock?","Processes waiting for each other's resources forever","A crashed process","A slow CPU","Memory overflow","A"),
        ("What is the Banker's Algorithm?","A deadlock avoidance algorithm","A CPU scheduling algorithm","A memory allocation method","A file system check","A"),
        ("Which scheduling algorithm gives each process equal CPU time?","Round Robin","FCFS","SJF","Priority Scheduling","A"),
        ("What does FCFS stand for?","First Come First Served","Fast CPU First Served","First Core First Scheduled","Fastest CPU First Served","A"),
        ("What is SJF scheduling?","Shortest Job First","Shortest Job Finished","Scheduled Job First","Slowest Job First","A"),
        ("What is thrashing in OS?","Excessive paging causing performance drop","A type of virus","CPU overheating","Memory corruption","A"),
        ("What is a semaphore?","A synchronization tool for processes","A type of scheduler","A memory page","A file system","A"),
        ("What is a mutex?","Mutual exclusion lock","A type of semaphore without limits","A CPU register","A memory segment","A"),
        ("What is context switching?","Saving and loading process states","Switching between users","Changing file permissions","Memory defragmentation","A"),
        ("What is the purpose of the scheduler?","Decide which process runs next","Manage memory allocation","Handle file operations","Control network access","A"),
        ("What is a file system?","Method for organizing and storing files","A type of process","A CPU component","A memory type","A"),
        ("Which file system is commonly used in Windows?","NTFS","ext4","FAT16","HFS+","A"),
        ("What is the difference between process and program?","Process is active, program is static","They are the same","Program is active, process is static","Process is stored on disk","A"),
        ("What is IPC (Inter-Process Communication)?","Methods for processes to communicate","A type of interrupt","A scheduling algorithm","A memory technique","A"),
        ("What is a system call?","Request from process to OS kernel","A regular function call","A hardware interrupt","A file operation","A"),
        ("What is demand paging?","Pages loaded only when needed","Loading all pages at start","A type of segmentation","Memory compression","A"),
        ("What is the page replacement algorithm LRU?","Least Recently Used page is replaced","Least Random Used","Last Required Unused","Lowest Remaining Utility","A"),
        ("What is spooling in OS?","Storing data in buffer for slow devices","A type of scheduling","Memory management","Process synchronization","A"),
        ("What is a real-time OS?","OS that guarantees response within time limits","OS with fastest CPU","OS for gaming","OS with large memory","A"),
        ("What is the difference between preemptive and non-preemptive scheduling?","Preemptive can interrupt running process, non-preemptive cannot","They are the same","Non-preemptive is faster","Preemptive uses less memory","A"),
        ("What is disk scheduling?","Algorithm to order disk I/O requests","Memory allocation method","CPU scheduling","File organization","A"),
        ("What does SSTF stand for in disk scheduling?","Shortest Seek Time First","Slowest Seek Time First","Sequential Seek Time First","System Seek Time First","A"),
        ("What is fragmentation in OS?","Unused memory gaps that waste space","A type of virus","CPU slowdown","File corruption","A"),
        ("What is compaction in memory management?","Moving processes to eliminate fragmentation","Compressing files","Reducing CPU usage","Combining processes","A"),
        ("What is a zombie process?","A process that completed but entry remains in process table","A malicious process","A sleeping process","A high-priority process","A"),
        ("What is an orphan process?","A process whose parent has terminated","A child process","A sleeping process","A zombie process","A"),
        ("What is a page fault?","Accessing a page not currently in memory","A CPU error","A disk failure","A network error","A"),
        ("What is the working set model?","Set of pages a process is actively using","All pages in memory","Pages on disk","Cached pages","A"),
        ("What does RAID stand for?","Redundant Array of Independent Disks","Random Access Independent Drives","Rapid Array of Integrated Drives","Redundant Access Independent Data","A"),
        ("What is a device driver?","Software that controls hardware devices","A type of process","A file system","A scheduling algorithm","A"),
        ("What is the boot process?","Loading the OS when computer starts","Shutting down the computer","Installing software","Formatting the disk","A"),
        ("What is swapping in OS?","Moving process between RAM and disk","Exchanging data between processes","Switching CPU cores","Changing file permissions","A"),
        ("What is a critical section?","Code that accesses shared resources","A high-priority process","A type of interrupt","A system call","A"),
        ("What is the producer-consumer problem?","Classic synchronization problem with shared buffer","A scheduling algorithm","A memory leak issue","A deadlock example","A"),
        ("What is an interrupt in OS?","Signal to CPU that an event needs attention","A type of process","A scheduling method","A file operation","A"),
        ("What is the difference between user mode and kernel mode?","Kernel mode has full hardware access, user mode is restricted","They are the same","User mode has more privileges","Kernel mode is slower","A"),
        ("What is address space?","Range of memory addresses available to a process","Physical RAM size","Disk storage space","Cache size","A"),
        ("What is the purpose of TLB (Translation Lookaside Buffer)?","Speed up virtual to physical address translation","Store process data","Cache disk data","Buffer network packets","A"),
        ("What is a pipe in OS?","A method for IPC between related processes","A type of file","A network connection","A hardware component","A"),
        ("What is the fork() system call?","Creates a new child process","Terminates a process","Loads a program","Allocates memory","A"),
    ]

    for q in dbms_questions:
        c.execute("INSERT INTO questions(category_id,question,opt_a,opt_b,opt_c,opt_d,answer) VALUES(?,?,?,?,?,?,?)",
                  (dbms_id,) + q)
    for q in os_questions:
        c.execute("INSERT INTO questions(category_id,question,opt_a,opt_b,opt_c,opt_d,answer) VALUES(?,?,?,?,?,?,?)",
                  (os_id,) + q)
    conn.commit()

# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('login'))

# ── AUTH ──────────────────────────────────────

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        uname = request.form.get('username','').strip()
        pwd   = request.form.get('password','').strip()
        conn  = get_db()
        user  = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (uname,pwd)).fetchone()
        conn.close()
        if user:
            session['user_id']   = user['id']
            session['username']  = user['username']
            session['role']      = user['role']
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('student_dashboard'))
        error = "Invalid username or password."
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        uname = request.form.get('username','').strip()
        pwd   = request.form.get('password','').strip()
        if not uname or not pwd:
            error = "All fields are required."
        else:
            conn = get_db()
            existing = conn.execute("SELECT id FROM users WHERE username=?", (uname,)).fetchone()
            if existing:
                error = "Username already taken."
                conn.close()
            else:
                conn.execute("INSERT INTO users(username,password,role,created) VALUES(?,?,?,?)",
                             (uname, pwd, 'student', datetime.now().strftime('%Y-%m-%d %H:%M')))
                conn.commit()
                conn.close()
                return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── STUDENT ──────────────────────────────────

@app.route('/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    conn = get_db()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    attempts   = conn.execute("""
        SELECT a.*, c.name AS cat_name
        FROM attempts a JOIN categories c ON a.category_id=c.id
        WHERE a.username=? ORDER BY a.taken_at DESC LIMIT 10
    """, (session['username'],)).fetchall()
    conn.close()
    return render_template('student_dashboard.html', categories=categories, attempts=attempts)

@app.route('/quiz/<int:cat_id>', methods=['GET','POST'])
def quiz(cat_id):
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    conn = get_db()
    cat = conn.execute("SELECT * FROM categories WHERE id=?", (cat_id,)).fetchone()
    if not cat:
        conn.close()
        return redirect(url_for('student_dashboard'))

    if request.method == 'POST':
        # Score the quiz
        score = 0
        total = 0
        questions = conn.execute("SELECT * FROM questions WHERE category_id=?", (cat_id,)).fetchall()
        q_map = {str(q['id']): q for q in questions}
        for key, val in request.form.items():
            if key.startswith('q_'):
                qid = key[2:]
                total += 1
                if qid in q_map and q_map[qid]['answer'] == val:
                    score += 1
        conn.execute("INSERT INTO attempts(username,category_id,score,total,taken_at) VALUES(?,?,?,?,?)",
                     (session['username'], cat_id, score, total, datetime.now().strftime('%Y-%m-%d %H:%M')))
        conn.commit()
        conn.close()
        return redirect(url_for('result', score=score, total=total, cat_name=cat['name']))

    # GET: show quiz
    all_qs = conn.execute("SELECT * FROM questions WHERE category_id=?", (cat_id,)).fetchall()
    conn.close()
    questions = random.sample(list(all_qs), min(10, len(all_qs)))
    return render_template('quiz.html', questions=questions, cat=cat)

@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    score    = request.args.get('score', 0, type=int)
    total    = request.args.get('total', 0, type=int)
    cat_name = request.args.get('cat_name', '')
    pct      = round((score/total)*100) if total else 0
    return render_template('result.html', score=score, total=total, pct=pct, cat_name=cat_name)

@app.route('/leaderboard')
def leaderboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    board = conn.execute("""
        SELECT a.username,
               c.name AS cat_name,
               MAX(a.score) AS best_score,
               a.total,
               ROUND(MAX(a.score)*100.0/a.total,1) AS pct
        FROM attempts a
        JOIN categories c ON a.category_id=c.id
        GROUP BY a.username, a.category_id
        ORDER BY pct DESC LIMIT 20
    """).fetchall()
    conn.close()
    return render_template('leaderboard.html', board=board)

# ── ADMIN ─────────────────────────────────────

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    users      = conn.execute("SELECT * FROM users WHERE role='student'").fetchall()
    q_count    = conn.execute("SELECT COUNT(*) AS cnt FROM questions").fetchone()['cnt']
    a_count    = conn.execute("SELECT COUNT(*) AS cnt FROM attempts").fetchone()['cnt']
    conn.close()
    return render_template('admin_dashboard.html',
                           categories=categories, users=users,
                           q_count=q_count, a_count=a_count)

@app.route('/admin/questions/<int:cat_id>')
def admin_questions(cat_id):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    cat       = conn.execute("SELECT * FROM categories WHERE id=?", (cat_id,)).fetchone()
    questions = conn.execute("SELECT * FROM questions WHERE category_id=?", (cat_id,)).fetchall()
    conn.close()
    return render_template('admin_questions.html', questions=questions, cat=cat)

@app.route('/admin/add_question', methods=['GET','POST'])
def add_question():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    error = None
    if request.method == 'POST':
        cat_id   = request.form.get('category_id')
        question = request.form.get('question','').strip()
        opt_a    = request.form.get('opt_a','').strip()
        opt_b    = request.form.get('opt_b','').strip()
        opt_c    = request.form.get('opt_c','').strip()
        opt_d    = request.form.get('opt_d','').strip()
        answer   = request.form.get('answer','').strip()
        if not all([cat_id, question, opt_a, opt_b, opt_c, opt_d, answer]):
            error = "All fields are required."
        else:
            conn.execute("INSERT INTO questions(category_id,question,opt_a,opt_b,opt_c,opt_d,answer,created_by) VALUES(?,?,?,?,?,?,?,?)",
                         (cat_id, question, opt_a, opt_b, opt_c, opt_d, answer, session['user_id']))
            conn.commit()
            conn.close()
            return redirect(url_for('admin_dashboard'))
    conn.close()
    return render_template('add_question.html', categories=categories, error=error)

@app.route('/admin/delete_question/<int:qid>', methods=['POST'])
def delete_question(qid):
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    q = conn.execute("SELECT category_id FROM questions WHERE id=?", (qid,)).fetchone()
    conn.execute("DELETE FROM questions WHERE id=?", (qid,))
    conn.commit()
    cat_id = q['category_id'] if q else None
    conn.close()
    if cat_id:
        return redirect(url_for('admin_questions', cat_id=cat_id))
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/scores')
def admin_scores():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    scores = conn.execute("""
        SELECT a.username, c.name AS cat_name, a.score, a.total,
               ROUND(a.score*100.0/a.total,1) AS pct, a.taken_at
        FROM attempts a
        JOIN categories c ON a.category_id=c.id
        ORDER BY a.taken_at DESC
    """).fetchall()
    conn.close()
    return render_template('admin_scores.html', scores=scores)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
