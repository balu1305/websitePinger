from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def dashboard():
    conn = sqlite3.connect("network_monitor.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM server_status ORDER BY timestamp DESC")
    data = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)