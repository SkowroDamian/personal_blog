# import logging
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_required, login_user, logout_user, current_user
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash #biblioteka do sprawdzania i generowania hashy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'testkey123'


# app.logger.setLevel(logging.DEBUG) # ustawienia debugowania

# login manager
login_manager = LoginManager(app)
login_manager.login_view ='login' # ustawia nazwę funkcji któa obsługuje logowanie
# login_manager.init_app(app)

db = SQLAlchemy(app) #initializes db

#create database model
class Posts(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True) # sets id column to be primary key
    title = db.Column("title", db.String(100), nullable= False)
    content = db.Column("content", db.String(500))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #
    def __repr__(self):
        return '<Name %r>' % self.title
    
class User(UserMixin, db.Model): # user mixin dodaje atrybuty flask-login do modelu 
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


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

### authorization
@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', name=current_user.name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    name = request.form['name']
    password = request.form['password']

    user = User.query.filter_by(name=name).first() # query user with provided name from database to check if he exists
    if not user or not check_password_hash(user.password, password):
        
        flash("Check your credentials")
        
        
        return redirect(url_for('login'))
    #login code 
    # app.logger.debug('account valid') # 
    login_user(user)
    return redirect(url_for('admin'))

    # new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


#login manager load user implementation
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))