from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

DB = 'malaeby.db'
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stadium TEXT,
        gov TEXT,
        date TEXT,
        time TEXT,
        duration TEXT,
        price INTEGER,
        payment TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/api/booking', methods=['POST'])
def create_booking():
    data = request.json
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO bookings (stadium,gov,date,time,duration,price,payment) VALUES (?,?,?,?,?,?,?)',
        (data['stadium'],data['gov'],data['date'],data['time'],data['duration'],data['price'],data['payment']))
    conn.commit()
    booking_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'booking_id': booking_id})

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    rows = c.fetchall()
    conn.close()
    bookings = [{'id':r[0],'stadium':r[1],'gov':r[2],'date':r[3],'time':r[4],'duration':r[5],'price':r[6],'payment':r[7]} for r in rows]
    return jsonify(bookings)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
