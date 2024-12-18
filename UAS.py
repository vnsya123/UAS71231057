from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

@app.route('/success/<name>', methods=['GET'])
def success(name):
    return f'Proses data user : {name} berhasil'

@app.route('/userlist')
def userList():
    users = getAllUser()
    return render_template('userlist.html', title='Daftar User', listuser=users)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute("SELECT password FROM user WHERE username=?", (username,))
        result = cursor.fetchone()
        connection.close()

        if result and check_password_hash(result[0], password):
            session['user'] = username  # Store the username in session
            flash('Login successful', 'success')
            return redirect(url_for('success', name=username))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route("/registeruser", methods=['GET', 'POST'])
def registeruser():
    if request.method == 'POST':
        realname = request.form['realname']
        username = request.form['username']
        password = request.form['password']

        # Validate password strength
        if len(password) < 8:
            flash('Password must be at least 8 characters long', 'danger')
            return render_template('register.html')

        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='sha256')

        # Insert into the database
        connection = sqlite3.connect("user.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO user (realname, username, password) VALUES (?, ?, ?)", 
                       (realname, username, hashed_password))
        connection.commit()
        connection.close()

        flash('User registered successfully', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

def getAllUser():
    try:
        with sqlite3.connect("user.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT realname, pob, username, password FROM user;")
            desc = cursor.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
            return data
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

if __name__ == '__main__':
    app.run(debug=True)
