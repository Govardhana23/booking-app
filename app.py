from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, instance_relative_config=True)
DB_PATH = app.instance_path + '/bookings.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slot TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        slot = request.form['slot']
        conn = get_db_connection()
        conn.execute('INSERT INTO bookings (name, slot) VALUES (?, ?)', (name, slot))
        conn.commit()
        conn.close()
        return redirect(url_for('bookings'))
    return render_template('index.html')

@app.route('/bookings')
def bookings():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

if __name__ == "__main__":
    import os
    os.makedirs(app.instance_path, exist_ok=True)
    init_db()
    app.run(debug=True)
