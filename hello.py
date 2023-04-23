from datetime import datetime

from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Перед первым запуском, в командной строке:
# set FLASK_ENV=development
# set FLASK_APP=hello.py
# Потом уже:
# flask run
# Вышеуказанное не работает (возможно только в Windows)
# https://stackoverflow.com/questions/29882642/how-to-run-a-flask-application
# flask --app hello --debug run

# Create a Flask Instance
app = Flask(__name__)

# Add Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usersname:password@localhost/db_name'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/users'

# Create a class Form
# Для создания класса форм, необходимо использовать секретный ключ
# Для исключения межсайтовых атак
# В форме создается ключ, который сверяется с токеном основной страницы
# Таким образом проверяется, чтобы хакер не захватил нашу форму
# Используем TokenSerf
# https://flask-wtf.readthedocs.io/en/1.0.x/
app.config['SECRET_KEY'] = "My_super_secret_key"

# Initialize The Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# flask --app hello db init
# flask --app hello db    - получим список команд
# flask --app hello db migrate -m 'Initial migration'
# flask --app hello db upgrade


# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name
    
# В терминале запускаем python
# from hello import app
# from hello import db
# with app.app_context():
#   db.create_all()
# exit()

# Форма для пользователя
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite color")
    submit = SubmitField("Submit")


# Форма для отправки имени
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a route decorator
@app.route('/')
def index():
    first_name : str = 'John'
    stuff = "This is <strong>Bold</strong> Text"
    stuff2 = "This is bold text"
    favorite_pizza = ['Pepperoni', 'Cheese', 'Mushrooms', 41]
    return render_template('index.html',
                           first_name = first_name, 
                           stuff = stuff, 
                           stuff2 = stuff2,
                           favorite_pizza = favorite_pizza)

# https://jinja.palletsprojects.com/en/3.1.x/
# Фильтры:
# https://jinja.palletsprojects.com/en/3.1.x/templates/#filters

# localhost:5000/user/John
@app.route('/user/<name>')
def user(name : str):
    # return f'<h1>hello {name}!</h1>'
    return render_template('user.html', name=name)


# Пользователи
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
            flash("User added successfully!", "success")
        else:
            flash("Пользователь с таким email существует!", "warning")
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''       
    our_users = Users.query.order_by(Users.date_added)

    return render_template('add_user.html', name = name, form = form, our_users=our_users)


# Update Database Record
@app.route('/user/update/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User updated successfully", "success")
        except:
            flash("Looks like there was a problem...try again!", "error")
    return render_template("update_user.html", form = form, name_to_update = name_to_update)


# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


# Create Name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        # Форма отправлена
        flash("Form submitted successfully", "success")
        flash("Form submitted warning", "warning")
        flash("Form submitted error", "error")

    return render_template('name.html', name = name, form = form)
