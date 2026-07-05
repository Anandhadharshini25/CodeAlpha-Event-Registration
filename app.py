from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        event TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Event Registration</title>
</head>
<body>
    <h2>Event Registration Form</h2>

    <form method="POST">
        <input type="text" name="name" placeholder="Enter Name" required><br><br>

        <input type="email" name="email" placeholder="Enter Email" required><br><br>

        <select name="event">
            <option>Python Workshop</option>
            <option>AI Seminar</option>
            <option>Web Development</option>
        </select><br><br>

        <button type="submit">Register</button>
    </form>

    <hr>

    <h3>Registered Participants</h3>

    <ul>
    {% for row in data %}
        <li>{{row[1]}} | {{row[2]}} | {{row[3]}}</li>
    {% endfor %}
    </ul>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    conn = sqlite3.connect("events.db")
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        event = request.form["event"]

        cursor.execute(
            "INSERT INTO registrations(name,email,event) VALUES(?,?,?)",
            (name, email, event)
        )
        conn.commit()

    cursor.execute("SELECT * FROM registrations")
    data = cursor.fetchall()

    conn.close()

    return render_template_string(HTML, data=data)


if __name__ == "__main__":
    app.run(debug=True)