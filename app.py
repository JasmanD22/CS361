from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    details = db.Column(db.String(200))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    end_time = db.Column(db.Time, nullable=True)
    priority = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        # Convert string values from form to appropriate Python objects
        date_obj = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        time_obj = datetime.strptime(request.form['time'], '%H:%M').time() if request.form['time'] else None
        end_time_obj = datetime.strptime(request.form['end_time'], '%H:%M').time() if request.form['end_time'] else None
        new_task = Task(title=request.form['title'], details=request.form['details'],
                        date=date_obj, time=time_obj, end_time=end_time_obj,
                        priority=int(request.form['priority']), completed=False)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_task.html')

@app.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.details = request.form['details']
        task.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        task.time = datetime.strptime(request.form['time'], '%H:%M').time() if request.form['time'] else None
        task.end_time = datetime.strptime(request.form['end_time'], '%H:%M').time() if request.form['end_time'] else None
        task.priority = int(request.form['priority'])
        task.completed = 'completed' in request.form
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
