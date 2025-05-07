from flask import Flask, render_template, request, redirect, session
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# قاعدة البيانات
def init_db():
    conn = sqlite3.connect('hotel.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# صفحة الرئيسية
@app.route('/')
def home():
    if 'user' in session:
        return redirect('/dashboard')
    return redirect('/login')

# صفحة تسجيل الدخول
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect('/dashboard')
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# صفحة إنشاء حساب جديد
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

# صفحة التواصل مع العملاء
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        user_name = request.form['username']
        message = request.form['message']
        conn = sqlite3.connect('hotel.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (user_name, message) VALUES (?, ?)", (user_name, message))
        conn.commit()
        conn.close()
        return render_template('contact.html', success="Message sent successfully!")
    return render_template('contact.html')

# صفحة لوحة التحكم بعد الدخول
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['user'])

# تسجيل الخروج
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
