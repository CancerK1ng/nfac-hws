from flask import Flask, render_template, request, redirect, url_for
from models import db, Car

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
db.init_app(app)

# Список всех машин
@app.route("/cars")
def cars_list():
    cars = Car.query.all()
    return render_template("cars/list.html", cars=cars)

# 🚗 Поиск машин
@app.route("/cars/search")
def search_car():
    car_name = request.args.get("car_name", "")
    cars = Car.query.filter(Car.name.ilike(f"%{car_name}%")).all()
    return render_template("cars/search.html", cars=cars, car_name=car_name)

# 📄 Отображение формы добавления машины
@app.route("/cars/new", methods=["GET"])
def new_car_form():
    return render_template("cars/new.html")

# ➕ Обработка POST-запроса на добавление
@app.route("/cars/new", methods=["POST"])
def add_car():
    name = request.form["name"]
    year = request.form["year"]
    new_car = Car(name=name, year=year)
    db.session.add(new_car)
    db.session.commit()
    return redirect(url_for("cars_list"))
