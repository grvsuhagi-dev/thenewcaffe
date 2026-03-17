from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database/data.db")
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/reservation", methods=["GET", "POST"])
def reservation():
    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        date = request.form["date"]
        time = request.form["time"]
        people = request.form["people"]

        conn = get_db()
        conn.execute(
            "INSERT INTO reservations (name, phone, date, time, people) VALUES (?,?,?,?,?)",
            (name, phone, date, time, people),
        )
        conn.commit()

        return "Reservation Confirmed!"

    return render_template("reservation.html")


@app.route("/order", methods=["POST"])
def order():

    name = request.form["name"]
    item = request.form["item"]
    quantity = request.form["quantity"]

    conn = get_db()
    conn.execute(
        "INSERT INTO orders (name,item,quantity) VALUES (?,?,?)",
        (name, item, quantity),
    )
    conn.commit()

    return "Order Placed Successfully!"


if __name__ == "__main__":
    app.run(debug=True)