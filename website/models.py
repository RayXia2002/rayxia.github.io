from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Meeting(db.Model):
    __tablename__ = 'meeting'
    id = db.Column(db.Integer, primary_key = True)
    locationid = db.Column(db.Integer, db.ForeignKey('location.id'))
    start_time = db.Column(db.DateTime())
    end_time = db.Column(db.DateTime())
    purpose = db.Column(db.String(30))
    mandatory = db.Column(db.Boolean)
    remote = db.Column(db.Boolean)
    moderatorid = db.Column(db.Integer, db.ForeignKey('employee.id'))

class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(30))
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.id'))
    roleid = db.Column(db.Integer, db.ForeignKey('role.id'))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    moderator = db.Column(db.Boolean)
    attendees = db.relationship('Attendees')

class Attendees(db.Model):
    employeeid = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key = True)
    meetingid = db.Column(db.Integer, db.ForeignKey('meeting.id'), primary_key = True)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = True)
    address = db.Column(db.String(30))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    zoom = db.Column(db.String(30))
    meetings = db.relationship('Meeting')
    
class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), unique = True)
    accounts = db.relationship('Account')
