import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
import pymysql.cursors
import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__) 
app.secret_key = os.getenv('SECRET_KEY', 'super_secret_key')

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'registration'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    filter_type = request.args.get('filter', 'all')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            
            cursor.execute("SELECT COUNT(*) AS open_count FROM todos WHERE user_id = %s AND is_done = FALSE", (session['user_id'],))
            open_count_result = cursor.fetchone()
            open_count = open_count_result['open_count'] if open_count_result else 0

            if filter_type == 'active':
                sql = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s AND is_done = FALSE ORDER BY todo_id DESC"
            elif filter_type == 'completed':
                sql = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s AND is_done = TRUE ORDER BY todo_id DESC"
            else:
                sql = "SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC"
                
            cursor.execute(sql, (session['user_id'],))
            todos = cursor.fetchall()
            return render_template('index.html', name=session['name'], todos=todos, current_filter=filter_type, open_count=open_count)
    finally:
        conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not name or not email or not password or not confirm_password:
            return render_template('register.html', error="All fields are required")
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")

        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)"
                cursor.execute(sql, (email, name, hashed_pw))
                conn.commit()
                
                user_id = cursor.lastrowid
                session['user_id'] = user_id
                session['name'] = name
                return redirect(url_for('index'))
        except pymysql.MySQLError as e:
            if e.args[0] == 1062:
                return render_template('register.html', error="Email Already Exists")
            return render_template('register.html', error="Database error occurred")
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template('login.html', error="Email and password are required")
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT user_id, name, password_hash FROM users WHERE email = %s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()

                if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    session['user_id'] = user['user_id']
                    session['name'] = user['name']
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', error="Invalid email or password")
        finally:
            conn.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_todo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form.get('title', '').strip()
    if not title:
        flash("Title is required")
        return redirect(url_for('index'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO todos (user_id, title) VALUES (%s, %s)"
            cursor.execute(sql, (session['user_id'], title))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "UPDATE todos SET is_done = NOT is_done WHERE todo_id = %s AND user_id = %s"
            cursor.execute(sql, (todo_id, session['user_id']))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM todos WHERE todo_id = %s AND user_id = %s"
            cursor.execute(sql, (todo_id, session['user_id']))
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit_todo(todo_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_title = request.form.get('title', '').strip()
    
    if not new_title:
        flash('Title is required (an empty title or only spaces)')
        return redirect(url_for('index'))
        
    if len(new_title) > 200:
        flash('Title is too long (200 characters at most)')
        return redirect(url_for('index'))

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
                (new_title, todo_id, session['user_id'])
            )
            conn.commit()
    finally:
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__': 
    app.run(debug=True, port=5000)