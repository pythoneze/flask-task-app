from flask import Flask, render_template, redirect, request
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
# home page
@app.route('/', methods=["POST", "GET"])
def home():
    # add task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'An error occurred: {e}')
            return 'Failed to add task'
    # see all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.date).all()
        return render_template('index.html', tasks=tasks)

# delete an item
@app.route('/delete/<int:id>')
def delete_task(id:int):
    task = MyTask.query.get_or_404(id) 
    try:
        db.session.delete(task) 
        db.session.commit()
        return redirect('/') 
    except Exception as e:
        return f"Error:{e}"

# edit an item
@app.route('/edit/<int:id>', methods=["GET", "POST"])
def edit_task(id:int):
    task = MyTask.query.get_or_404(id) 
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/') 
        except Exception as e:
            return f"Error:{e}"
    else: 
        return render_template('edit.html', task=task)

# run the app
if __name__ == '__main__':
    app.run(debug=True)
