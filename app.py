from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #initializes db

#create database model
class Posts(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True) # sets id column to be primary key
    title = db.Column("title", db.String(100), nullable= False)
    content = db.Column("content", db.String(500))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #create a string
    def __repr__(self):
        return '<Name %r>' % self.title
    
@app.route('/')
def home():
    posts = Posts.query.order_by(Posts.date_added)
    return render_template('blog.html', posts=posts)

@app.route('/add', methods=['Get', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post = Posts(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('add'))
    return render_template('add.html')