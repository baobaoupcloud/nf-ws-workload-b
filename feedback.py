import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Create Database Table
def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER,
            mood TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/workload-b', methods=['GET', 'POST'])
def workload_b():
    if request.method == 'POST':
        data = request.json
        rating = data.get("rating")
        mood = data.get("mood")

        if not rating or not mood:
            return jsonify({"error": "Invalid input"}), 400

        conn = sqlite3.connect('feedback.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (rating, mood) VALUES (?, ?)", (rating, mood))
        conn.commit()
        conn.close()

        return jsonify({"message": "Feedback submitted successfully!"})

    return render_template('feedback.html')

@app.route('/view-feedback')
def view_feedback():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM feedback")
    feedbacks = cursor.fetchall()
    conn.close()
    return jsonify(feedbacks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
