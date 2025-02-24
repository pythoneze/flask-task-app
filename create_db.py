from app import app, db

# create the database tables if not exists
with app.app_context():
    db.create_all()