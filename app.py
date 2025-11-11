from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    streak INTEGER DEFAULT 0,
                    last_completed TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = [{'id': row[0], 'name': row[1], 'streak': row[2], 'last_completed': row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    name = data['name']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added'})

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    now = datetime.utcnow()
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT streak, last_completed FROM tasks WHERE id = ?', (task_id,))
    row = c.fetchone()
    if row:
        streak, last_completed_str = row
        if last_completed_str:
            last_completed = datetime.fromisoformat(last_completed_str)
            time_diff = now - last_completed
            if time_diff > timedelta(hours=24):
                streak = 0  # Reset streak if more than 24 hours
        streak += 1
        c.execute('UPDATE tasks SET streak = ?, last_completed = ? WHERE id = ?', (streak, now.isoformat(), task_id))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Task completed', 'new_streak': streak})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)