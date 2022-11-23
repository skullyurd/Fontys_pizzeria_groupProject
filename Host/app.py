import json
from operator import truth
from flask import Flask, jsonify, redirect, request, render_template, template_rendered, session, url_for
from datetime import timedelta
import os
import ovenPieceOfCode
from threading import Thread

app = Flask(__name__)

app.secret_key = "key"
app.permanent_session_lifetime = timedelta(hours=1)

images_folder = os.path.join('static', 'Images')

app.config['UPLOAD_FOLDER'] = images_folder

quantityPerPizza = []
orders = []
price = 0
TotalOrders = 0

@app.route("/", methods=["POST", "GET"])
def homepage():
    global user

    if request.method == "POST":
        session.permanent = truth
        user = request.form["nm"]
        session["user"] = user
        return redirect (url_for("store"))
    else:
        if "user" in session:
            return redirect (url_for("store"))
        return render_template('index.html')


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("homepage"))

@app.route("/store", methods=["POST", "GET"])
def store():

    if "user" in session:
        user = session["user"]
        MagheritaPizzaPic = os.path.join(app.config['UPLOAD_FOLDER'], 'MargheritaPizza.jpg')
        BurgerPizzaPic = os.path.join(app.config['UPLOAD_FOLDER'], 'BurgerPizza.jpg')
        ExoticPizzaPic = os.path.join(app.config['UPLOAD_FOLDER'], 'ExoticPizza.jpg')
        MarinaraPizzaPic = os.path.join(app.config['UPLOAD_FOLDER'], 'MarinaraPizza.jpg')
        NinoBelPizzaPic = os.path.join(app.config['UPLOAD_FOLDER'], 'NinoBelPizza.jpg')
        PepperoniPizzaPic = os.path.join(app.config['UPLOAD_FOLDER'], 'PepperoniPizza.jpg')
        ProsciuttoPizzaPic = os.path.join(app.config['UPLOAD_FOLDER'], 'ProsciuttoPizza.jpg')
        QuattrosPizzaPic = os.path.join(app.config['UPLOAD_FOLDER'], 'QuattrosPizza.jpg')
        StarCarlosPizzaPic = os.path.join(app.config['UPLOAD_FOLDER'], 'StarCarlosPizza.jpg')

        return render_template("store.html",
        pizzaMagherita = MagheritaPizzaPic,
        pizzaBurger = BurgerPizzaPic,
        pizzaExotic = ExoticPizzaPic,
        pizzaMarinara = MarinaraPizzaPic,
        PizzaNinoBel = NinoBelPizzaPic,
        pizzaPepperoni = PepperoniPizzaPic,
        pizzaProsciutto = ProsciuttoPizzaPic,
        pizzaQuattros = QuattrosPizzaPic,
        pizzaStarCarlos = StarCarlosPizzaPic)

    else:
        return redirect(url_for("homepage"))

@app.route("/about")
def about():

    aboutPic = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.jpg')

    return render_template("about.html", logo = aboutPic)

@app.route("/receiveInfo", methods=['POST', 'GET'])
def receiveInfo():
    global price, TotalOrders

    output = request.get_json()
    result = json.loads(output)
    #this is a dict type
    #print(result['price'])
    #print(result['pizzas'])
    #print(result['quantityPizzas'])

    price = result['price']
    orders.append(result['pizzas'])
    quantityPerPizza.append(result['quantityPizzas'])

    length = len(orders[0])

    #for i in range(length):
     #   print(quantityPerPizza[0][i])
      #  print(orders[0][i])

    TotalOrders = TotalOrders + 1

    return redirect (url_for("payment"))

@app.route("/customize")
def customize():

    logoPic = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.jpg')
    
    return render_template("custom_page.html",
    logo = logoPic)

@app.route("/payment", methods=['POST', 'GET'])
def payment():
    global price

    if "user" in session:
        user = session["user"]
        return render_template("pay_page.html",
        customerPay = price)
    else:
        return redirect(url_for("homepage"))


    

@app.route("/tracker", methods=['POST', 'GET'])
def tracker():
    
    if "user" in session:
        user = session["user"]
        thr = Thread(target=ovenPieceOfCode.siteStuff, args=[orders])
        thr.start()
    
        return render_template("tracker_page.html")
    else:
        return redirect(url_for("homepage"))


@app.route("/pizzaOrders")
def pizzaOrders():
    global TotalOrders

    lengthEveryone = len(orders)
    #print(len(orders))
    
    if len(orders) > 0:
        length = 9
    else:
        length = 0

    return render_template("orderScreen.html", pizzaList = orders,
    orderLength = length,
    quant = quantityPerPizza,
    allOrders = lengthEveryone)

def removeOrders():
    orders.pop(0)
    #print(orders)
    #print("everything removed?")

def receiveTime(incomingTime):
    print(incomingTime)