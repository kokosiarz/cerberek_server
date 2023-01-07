from flask import Flask, request

app = Flask(__name__)

import sqlite3

index="events"

@app.route("/")
def home():
    conn = sqlite3.connect('db.sqlite')    
    c = conn.cursor()
    c.execute(f'SELECT * FROM {index}')
    output = c.fetchall()
    rows = """<tr>
            <th>timestamp</th>
            <th>activity</th>
            <th>armed</th>
            <th>engaged</th>
        </tr>
    """
    for row in output:
        row_html = "\n".join(map(lambda cell: f'<td>{cell}</td>', row))
        rows += f'<tr>{row_html}</tr>'

    conn.close()

    # return "<p>Hello, World!</p>"
    print(rows)
    # print("\n".join(output))
    return f'<table>{rows}</table>'

@app.route('/report-activity', methods=['POST'])
def report_activity():
    request_data = request.get_json()
    print("report activity!")
    print(request_data)
    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
    c.execute(f'CREATE TABLE IF NOT EXISTS {index} (timestamp VARCHAR(255) NOT NULL, activity VARCHAR(255) NOT NULL, armed BOOLEAN NOT NULL,engaged BOOLEAN NOT NULL)',)
    c.execute(f'insert into {index} values (?,?,?,?)',[
        request_data['timestamp'],
        request_data['activity'],
        request_data['armed'],
        request_data['engaged'],
        ])
    conn.commit()
    conn.close()
    return "OK"

