from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime

# app setup
app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
db = SQLAlchemy(app)

# models
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(50), nullable=False)
    complete = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Task {self.id}>'

# roots to webpages
@app.route('/')
def home():
    return render_template('index.html')

# run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create the database tables if not exists
    app.run(debug=True)
