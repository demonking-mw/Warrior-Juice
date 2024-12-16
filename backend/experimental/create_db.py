"""
Database builder on local machine
"""
from api import app, db

with app.app_context():
    db.create_all()
