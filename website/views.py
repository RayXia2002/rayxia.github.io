from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json
import psycopg2
import psycopg2.extras
from . import conn

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def calendar():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM meeting ORDER BY ID")
    calendar = cur.fetchall()
    return render_template('calendar.html', calendar = calendar)

@views.route("/insert", methods=["POST","GET"])
def insert():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        purpose = request.form['purpose']
        start = request.form['start']
        end = request.form['end']
        locationid = request.form['locationid']
        mandatory = request.form['mandatory']
        remote = request.form['mandatory']
        moderatorid = request.form['moderatorid']
        cur.execute("INSERT INTO Meeting (purpose, start_time, end_time, locationid, mandatory, remote, moderatorid) VALUES (%s,%s,%s,%s,%s,%s,%s)", [purpose, start, end, locationid, mandatory, remote, moderatorid])
        conn.commit()
        cur.close()
        msg = 'success'
    return jsonify(msg)

@views.route("/update", methods=["POST","GET"])
def update():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        purpose = request.form['purpose']
        start = request.form['start']
        end = request.form['end']
        id = request.form['id']
        cur.execute("UPDATE Meeting SET purpose = %s, start_time = %s, end_time = %s WHERE id = %s", [purpose, start, end, id])
        conn.commit()
        cur.close()
        msg = 'success'
    return jsonify(msg)

@views.route("/delete", methods=["POST","GET"])
def delete():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        id = request.form['id']
        cur.execute("DELETE FROM meeting WHERE id = {0}".format(id))
        conn.commit()
        cur.close()
        msg = 'Record deleted sucessfully'
    return jsonify(msg)