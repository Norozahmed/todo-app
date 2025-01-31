from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# Define the Task model (database table)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create the database
with app.app_context():
    db.create_all()

# Route to add and display tasks
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    else:
        tasks = Task.query.all()
        return render_template('index.html', tasks=tasks)

# Route to delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/') 

@app.route('/clear', methods=['POST'])
def clear():
    Task.query.delete()
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False)  
