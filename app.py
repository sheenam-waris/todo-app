
from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from random import randint


#project_root = os.path.abspath(os.path.dirname(__file__))
#db_path = "C:\Users\sheen\Downloads\ToDo-App-main\ToDo-App-main\instance\todos.db"

#flask_app.config["SQLALCHEMY_DATABASE_URI"] = 


flask_app = Flask(__name__)
flask_app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///newtodo.db'
flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
flask_app.secret_key = "123"
db = SQLAlchemy(flask_app)
flask_app.app_context().push()

@flask_app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    todos = db.relationship("Todo", backref="user", lazy=True)

    # def __init__(self,name,email):
    #     self.name = name
    #     self.email = email


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow())
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class DeletedTodo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

class TodoHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    title_previous = db.Column(db.String(200), nullable=False)
    title_updated = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow())

users_session = []


@flask_app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("A user with this email already exists. Please log in or use a different email.", "danger")
            return redirect(url_for("register"))  # Redirect back to the registration page
        new_user = User(email=email, password=password,name=name)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@flask_app.route("/logout")
def logout():
    session.pop("user_id")
    return redirect(url_for("login"))


@flask_app.route("/", methods=["GET", "POST"])
def login():
    if 'user_id' in session:
        # User is already authenticated, redirect to the 'todo' page
        return redirect(url_for('todo'))
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session["user_id"] = user.id
            session["user_email"] = user.email
            users_session.append(user.id)

            return redirect(url_for("todo"))

        else:
            flash("Login failed. Please check your email and password.", "danger")
    return render_template("login.html")


@flask_app.route("/todo", methods=["GET", "POST"])
def todo():
    user_id = session.get("user_id")
    user_email = session.get("user_email")
    if not user_id:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        todo = Todo(title=title, user_id=user_id)
        try:
            db.session.add(todo)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while adding the todo: " + str(e), "danger")
        return redirect(url_for("todo"))

    user = User.query.get(user_id)
    todos = user.todos
    return render_template(
        "first.html",
        todos=todos,
        allTodo=todos,
        user_name = user.name,
        user_email=user_email,
        users_session=users_session,
    )

@flask_app.route('/update_todo_status/<int:todo_id>', methods=['POST'])
def update_todo_status(todo_id):
    # Retrieve the TODO item with the given ID from the database
    todo = Todo.query.get(todo_id)

    if todo is not None:
        completed_str = request.form.get('completed')
        completed = completed_str.lower() == 'true'
        todo.completed = completed
        db.session.commit()
        return jsonify({"message": "TODO status updated successfully"})
    else:
        return jsonify({"error": "TODO item not found"}), 404


@flask_app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    todo = Todo.query.get(id)
    if not todo:
        flash("Todo not found.", "danger")
        return redirect(url_for("todo"))
    if todo:
        if request.method == 'POST':
            title = request.form['title']
            # Create a record in TodoHistory to store the previous and updated data
            history_record = TodoHistory(
                todo_id=todo.id,
                title_previous=todo.title,
                title_updated=title
                
            )
            db.session.add(history_record)
            
            # Update the original todo
            todo.title = title
            
            db.session.commit()
            
            return redirect(url_for('todo'))
    return render_template('update.html', todo=todo)


@flask_app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    if not todo:
        flash("Todo not found.", "danger")
        return redirect(url_for("todo"))
    if todo:
        # Create a new DeletedTodo record with the deleted todo's data
        deleted_todo = DeletedTodo(
            title=todo.title,
            user_id=todo.user_id
        )
        db.session.add(deleted_todo)
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("todo"))


@flask_app.route("/switch_profile", methods=["POST"])
def switch_profile():
    selected_user_id = int(request.form["selected_user"])
    session["user_id"] = selected_user_id

    # Redirect to the 'todo' page with the selected user's profile
    return redirect(url_for("todo"))


if __name__ == "__main__":
    db.create_all()
    flask_app.run(debug=True)
