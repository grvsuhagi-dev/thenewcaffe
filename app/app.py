from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ---------------- DATABASE MODELS ----------------

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PreOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    items = db.Column(db.Text, nullable=False)
    total = db.Column(db.Float, nullable=False)
    pickup_time = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- CREATE DATABASE ----------------

with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']
        guests = int(request.form['guests'])
        special_requests = request.form['special_requests']

        reservation = Reservation(
            name=name,
            email=email,
            phone=phone,
            date=date,
            time=time,
            guests=guests,
            special_requests=special_requests
        )

        db.session.add(reservation)
        db.session.commit()

        flash('Reservation created successfully!', 'success')

        return redirect(url_for('reservation'))

    return render_template('reservation.html')


@app.route('/preorder', methods=['POST'])
def preorder():

    data = request.get_json()

    name = data['name']
    email = data['email']
    phone = data['phone']
    items = str(data['items'])
    total = float(data['total'])
    pickup_time = data['pickup_time']

    order = PreOrder(
        name=name,
        email=email,
        phone=phone,
        items=items,
        total=total,
        pickup_time=pickup_time
    )

    db.session.add(order)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Pre-order placed successfully!'
    })


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/api/reservations')
def get_reservations():

    reservations = Reservation.query.order_by(
        Reservation.created_at.desc()
    ).limit(10).all()

    return jsonify([
        {
            'id': r.id,
            'name': r.name,
            'date': r.date,
            'time': r.time,
            'guests': r.guests
        }
        for r in reservations
    ])


# ---------------- RUN SERVER ----------------

if __name__ == '__main__':
    app.run(debug=True)