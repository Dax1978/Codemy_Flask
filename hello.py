from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

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

# Create a class Form
# Для создания класса форм, необходимо использовать секретный ключ
# Для исключения межсайтовых атак
# В форме создается ключ, который сверяется с токеном основной страницы
# Таким образом проверяется, чтобы хакер не захватил нашу форму
# Используем TokenSerf
# https://flask-wtf.readthedocs.io/en/1.0.x/
app.config['SECRET_KEY'] = "My_super_secret_key"

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
