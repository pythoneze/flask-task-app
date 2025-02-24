from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
