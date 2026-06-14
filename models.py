from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# =========================
# USER MODEL
# =========================
class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    role = db.Column(db.String(20), default='citizen', nullable=False)

    # Consistent Naive UTC
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    complaints = db.relationship('Complaint', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

# =========================
# COMPLAINT MODEL
# =========================
class Complaint(db.Model):
    __tablename__ = 'complaint'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    ward_no = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    
    resolution_photo = db.Column(db.String(200), nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)

    # --- FEEDBACK COLUMNS ---
    feedback_rating = db.Column(db.Integer, nullable=True) # 1 to 5 Stars
    feedback_msg = db.Column(db.Text, nullable=True)      # Citizen's comment

    status = db.Column(
        db.String(20),
        default='Pending',
        index=True
    )

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    
    # Consistent Naive UTC
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        db.Index('idx_status_created', 'status', 'created_at'),
        db.Index('idx_user_category', 'user_id', 'category'),
    )

    def __repr__(self):
        return f"<Complaint {self.id} - {self.status}>"

# =========================
# NOTICE MODEL
# =========================
class Notice(db.Model):
    __tablename__ = 'notice'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Consistent Naive UTC
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notice {self.title}>"