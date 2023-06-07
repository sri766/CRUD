#imports
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#initialization
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime(), default = datetime.utcnow)


    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods = ['GET','POST'])
def my_app():
    if request.method == "POST":
        Title = request.form['title']
        Desc = request.form['desc']
        todo = Todo(title = Title, desc = Desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo = allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/update/<int:sno>", methods = ['GET','POST'])
def update(sno):
    if request.method == "POST":
        Title = request.form['title']
        Desc = request.form['desc']
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = Title
        todo.desc = Desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    
    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html',todo = todo)


with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run()