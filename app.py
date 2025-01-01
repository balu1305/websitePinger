from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import time

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/data")
def get_data():
    conn = sqlite3.connect("network_monitor.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM server_status ORDER BY timestamp DESC")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

def log_status(host, status):
    conn = sqlite3.connect("network_monitor.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS server_status (host TEXT, status TEXT, timestamp TEXT)")
    cursor.execute("INSERT INTO server_status (host, status, timestamp) VALUES (?, ?, ?)",
                   (host, status, time.strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    socketio.emit('update_data', broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)