from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import psycopg2
import psycopg2.extras
from . import conn
from .models import Location, Account

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def calendar():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Meeting JOIN Attendees ON (Meeting.ID = Attendees.meetingid) WHERE Attendees.employeeID = %s ORDER BY Meeting.ID", [current_user.employeeid])
    calendar = cur.fetchall()
    return render_template('calendar.html', calendar = calendar)

@views.route('/mandatory')
@login_required
def mandatory():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Meeting JOIN Attendees ON (Meeting.ID = Attendees.meetingid) WHERE Attendees.employeeID = %s AND mandatory = true ORDER BY Meeting.ID", [current_user.employeeid])
    calendar = cur.fetchall()
    return render_template('calendar.html', calendar = calendar)

@views.route('/optional')
@login_required
def optional():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Meeting WHERE Meeting.mandatory = false ORDER BY Meeting.ID")
    calendar = cur.fetchall()
    return render_template('calendar.html', calendar = calendar)



@views.route("/insert", methods=["POST","GET"])
def insert():
    if (current_user.roleid == 1):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == 'POST':
            purpose = request.form['purpose']
            start = request.form['start']
            end = request.form['end']
            locationname = request.form['locationname']
            location = Location.query.filter_by(name=locationname).first()
            locationid = location.id
            mandatory = request.form['mandatory']
            remote = request.form['mandatory']
            moderatorusername = request.form['moderatorusername']
            moderator = Account.query.filter_by(username=moderatorusername).first()
            moderatorid = moderator.employeeid
            
            cur.execute("INSERT INTO Meeting (purpose, start_time, end_time, locationid, mandatory, remote, moderatorid) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id", [purpose, start, end, locationid, mandatory, remote, moderatorid])
            meetingid = cur.fetchone()["id"]
            conn.commit()
            cur.execute("INSERT INTO Attendees (employeeid, meetingid) VALUES (%s,%s)", [moderatorid, meetingid])
            conn.commit()
            cur.close()
            msg = 'success'
        return jsonify(msg)

@views.route("/update", methods=["POST","GET"])
def update():
    if (current_user.roleid == 1):
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
    if (current_user.roleid == 1):
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == 'POST':
            id = request.form['id']
            cur.execute("DELETE FROM attendees WHERE meetingid = {0}".format(id))
            cur.execute("DELETE FROM meeting WHERE id = {0}".format(id))
            conn.commit()
            cur.close()
            msg = 'Record deleted sucessfully'
        return jsonify(msg)