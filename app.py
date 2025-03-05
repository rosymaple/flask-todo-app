# Importing the modules here
# Render_template - Renders the HTML and request handles form data 
# Redirect and url_for directs users to route in the website navigation
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLalchemy
from datetime import datetime

# Create a new flask app
# The syntax for __name__ tells main to run
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)

# Define Todo Model Class (models a to do list item that is stored in the database)
# Defines the columns (attributes) for the class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    done = db.Column(db.Boolean, default = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    # Add the repr method
    # A special method that returns a string representing the object
    def __repr__(self): 
        return f'<todo id="{self.id}" title="{self.title}" done="{self.done}" created_at="{self.created_at}">'

# Create the database and table to hold the "To Do"
with app.app_context():
    db.create_all()

# Create a home route that displays the To Do list
@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)
# This will be returned to the browser display

# Create a route for adding a new To Do item to the database
@app.route('/add', methods=['POST'])
def add():
    # Get the title of the to do item from the HTML form on the web page
    title = request.form.get('title')
    # If the title IS NOT NULL, then create a new To Do List item record in the database
    # Else, redirect the user to the index page (home page)
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

# Create a route for marking a To Do List item as done
@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    # Update the database record and mark the To Do List item as done
    # If something goes wrong and the todo list item doesn't exist, display 404 erorr
    todo = Todo.query.get_or_404(todo_id)
    # Mark the todo list item as done in the database
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for('index'))

# Create a route to delete the To Do item
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    # Check if a database record exists with the ID number
    # and if there is no matching record, show a 404 error
    todo = Todo.query.get_or_404(todo_id)
    # Now we know if the item exists...
    # Delete the record in the database for the todo item
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# Start the Flask app in debug mode
# Flask provides a debugger that shows a stack tract if an error occurs
# Debug mode also reloads the page automatically when changes are made
# You do not need to restart the server.
if __name__ == '__main__':
    app.run(debug=True)

