from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Camera(db.Model):
    __tablename__ = 'cameras'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(64))
    max_capacity = db.Column(db.Integer, default=0)
    current_capacity = db.Column(db.Integer, default=0)
    cleaning_schedule = db.Column(db.Text)   # JSON/text
    maintenance_schedule = db.Column(db.Text)
    security_level = db.Column(db.Integer, default=1)
    equipment_list = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ObjectItem(db.Model):
    __tablename__ = 'objects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    classification = db.Column(db.String(64))  # Safe / Dangerous / Paranormal
    description = db.Column(db.Text)
    storage_requirements = db.Column(db.Text)
    camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id'), nullable=True)
    status = db.Column(db.String(64), default='stored')
    history_of_movements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(64), default='user')  # 'admin' or 'user' (extensible)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
    camera_id = db.Column(db.Integer, db.ForeignKey('cameras.id'), nullable=True)
    object_id = db.Column(db.Integer, db.ForeignKey('objects.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
