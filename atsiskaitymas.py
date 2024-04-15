from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('tasks.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT,
                user TEXT
             )''')

conn.commit()
conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        user = request.form['user']
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (name, description, status, user) VALUES (?, ?, ?, ?)", (name, description, status, user))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return ''


@app.route('/edit_task/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        user = request.form['user']
        c.execute("UPDATE tasks SET name=?, description=?, status=?, user=? WHERE id=?", (name, description, status, user, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM tasks WHERE id=?", (id,))
        task = c.fetchone()
        conn.close()
        return render_template('edit_task.html', task=task)



@app.route('/delete_task/<int:id>')
def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
