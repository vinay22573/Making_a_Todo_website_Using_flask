from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Create a Flask application
app = Flask(__name__)

# Configuration for the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Model definition
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    descp = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    done = db.Column(db.Boolean, default=False)  # Add a boolean field for the done status

    def __repr__(self) -> str:
        return f'<Todo {self.sno}-{self.title}>'


@app.cli.command('create-db')# Custom Flask command to create the database
def create_db():
    """Creates the database."""
    db.create_all()
    print('Database created.')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['descp']
        new_todo = Todo(title=title, descp=description)
        db.session.add(new_todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)






@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['descp']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.descp = description
        db.session.commit()  # Remember to commit the changes to the database
        return redirect('/')  # Redirect to the index page after updating
    else:
        todo = Todo.query.filter_by(sno=sno).first()
        return render_template('update.html', todo=todo)




@app.route('/delete/<int:sno>')#whenever a query takes some input then in this form we need to write it
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')





@app.route('/show')
def products(): 
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'




# Run the application if this script is executed
if __name__ == '__main__':
    app.run(debug=True)#When you are doing some development then set debug to true to see what is the error but if you are deploying it then set it to false so that the user can not see what exactly is the error he/she will jus see "Internal Server Error"
    
