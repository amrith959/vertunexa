from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Routes

@app.route('/')
def index():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    c.execute('SELECT name, COUNT(*) FROM habits GROUP BY name')
    data = c.fetchall()

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    conn.close()

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Habit Tracker Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>Habit Tracker Dashboard</h1>
    <canvas id="habitChart" width="400" height="200"></canvas>

    <script>
        const ctx = document.getElementById('habitChart').getContext('2d');
        const habitChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {{ labels|tojson }},
                datasets: [{
                    label: 'Habit Count',
                    data: {{ values|tojson }},
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        precision: 0
                    }
                }
            }
        });
    </script>

    <p><a href="{{ url_for('add_habit') }}">Add New Habit Entry</a></p>
</body>
</html>
    """, labels=labels, values=values)


@app.route('/add', methods=['GET', 'POST'])
def add_habit():
    if request.method == 'POST':
        habit_name = request.form['habit_name']
        date = datetime.now().strftime('%Y-%m-%d')

        conn = sqlite3.connect('habits.db')
        c = conn.cursor()
        c.execute('INSERT INTO habits (name, date) VALUES (?, ?)', (habit_name, date))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Add Habit</title>
</head>
<body>
    <h1>Add Habit Entry</h1>
    <form method="POST">
        <label for="habit_name">Habit Name:</label>
        <input type="text" id="habit_name" name="habit_name" required>
        <button type="submit">Add</button>
    </form>
    <p><a href="{{ url_for('index') }}">Back to Dashboard</a></p>
</body>
</html>
    """)

# Main entry point
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
