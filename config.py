import os
class Config:
    SECRET_KEY = 'gram-panchayat-secret-key-2026'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gram_complaints.db'  # Root level - NO instance/
    SQLALCHEMY_TRACK_MODIFICATIONS = False
