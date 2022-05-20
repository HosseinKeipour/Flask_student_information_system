# from datetime import datetime
from certifi import contents
from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///StudentsInfo.db' # /// 3 for relative path and 4 //// for absolute path
db = SQLAlchemy(app)

class ToDo(db.Model):  # ToDo is a table name that we will fill it here
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(200), nullable= True)
    age = db.Column(db.Integer, nullable= True)
    group = db.Column(db.String(200), nullable= True)
    college_name = db.Column(db.String(200), nullable= True)

    def __repr__(self):
        return '<Task %r>' %self.id

@app.route('/', methods=['POST', 'GET'])
# @app.route('/home')
def index():
    if request.method == 'POST':
        student_name = request.form['name']
        student_age = request.form['age']
        student_group = request.form['group']
        student_college_name = request.form['college_name']

        new_task = ToDo(name = student_name, age= student_age, group= student_group, college_name= student_college_name)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There is an issue in adding the task"
    else:
        tasks = ToDo.query.order_by(ToDo.name).all()
        return render_template('index.html',tasks= tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There is issue in deleting the data'

@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    task_to_update = ToDo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']
    
        try:
            # db.session.update(task_to_update)
            db.session.commit()
            return redirect('/')
        except:
            return 'There is issue in updating the data'
    else:
        return render_template('update.html', task_to_update = task_to_update)


if __name__ == "__main__":
    app.run(debug= True)