from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"

db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/')
def todo_show():
    allrows = Todo.query.all()
    if len(allrows) == 0:
            return render_template('empty.html')
    return render_template('showtodo.html', alltodos=allrows)


@app.route('/add', methods=['GET', 'POST'])
def todo_add():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        newrow = Todo(title=title, desc=desc)
        db.session.add(newrow)
        db.session.commit()
        return redirect('/')
    return render_template('addtodo.html')

@app.route('/search', methods=['GET', 'POST'])
def todo_search():
    if request.method == 'POST':
        title = request.form['title']
    allrows = Todo.query.filter_by(title=title).all()
    if len(allrows) == 0:
            return render_template('empty.html')
    return render_template('showTodo.html', alltodos=allrows)

@app.route('/delete/<int:sno>')
def todo_delete(sno):
    delrow =  Todo.query.filter_by(sno=sno).first()
    db.session.delete(delrow)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'] )
def todo_update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        row =  Todo.query.filter_by(sno=sno).first()
        row.title = title
        row.desc = desc
        db.session.commit()
        return redirect('/')
        
    row =  Todo.query.filter_by(sno=sno).first()
    return render_template('updatetodo.html', todo=row)


if __name__ == '__main__':
    app.run(debug=True)
