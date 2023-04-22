from flask import Flask, render_template

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
