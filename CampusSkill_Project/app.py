from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Ensure database exists
def init_db():
    if not os.path.exists("database.db"):
        with sqlite3.connect("database.db") as conn:
            conn.execute('''
                CREATE TABLE students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    skill TEXT NOT NULL,
                    want TEXT NOT NULL
                );
            ''')

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        skill = request.form['skill']
        want = request.form['want']
        with sqlite3.connect("database.db") as conn:
            conn.execute("INSERT INTO students (name, skill, want) VALUES (?, ?, ?)", (name, skill, want))
        return redirect(url_for('skills'))
    return render_template('register.html')

@app.route('/skills')
def skills():
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()
    return render_template('skills.html', students=students)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin123':
            with sqlite3.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM students")
                students = cur.fetchall()
            return render_template('admin_panel.html', students=students)
        else:
            return "Invalid Credentials"
    return render_template('admin_login.html')

@app.route('/delete/<int:id>')
def delete_entry(id):
    with sqlite3.connect("database.db") as conn:
        conn.execute("DELETE FROM students WHERE id=?", (id,))
    return redirect(url_for('admin'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students WHERE skill LIKE ? OR want LIKE ?", 
                        (f'%{keyword}%', f'%{keyword}%'))
            results = cur.fetchall()
        return render_template('skills.html', students=results)
    return redirect(url_for('skills'))

if __name__ == '__main__':
    app.run(debug=True)
