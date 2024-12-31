from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shelf_no = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specification = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    storage_location = db.Column(db.String(100), nullable=False)
    expiration_date = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.String(200), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Tokyo')))

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        shelf_no = request.form['shelf_no']
        name = request.form['name']
        specification = request.form['specification']
        quantity = request.form['quantity']
        storage_location = request.form['storage_location']
        expiration_date = request.form['expiration_date']
        if expiration_date == '不明':
            expiration_date = '不明'
        else:
            expiration_date = datetime.strptime(request.form['expiration_date_input'], '%Y-%m-%d').strftime('%Y-%m-%d')
        remarks = request.form['remarks']
        new_product = Product(
            shelf_no=shelf_no, name=name, specification=specification, 
            quantity=quantity, storage_location=storage_location, 
            expiration_date=expiration_date, remarks=remarks,
            last_updated=datetime.now(pytz.timezone('Asia/Tokyo')))
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.shelf_no = request.form['shelf_no']
        product.name = request.form['name']
        product.specification = request.form['specification']
        product.quantity = request.form['quantity']
        product.storage_location = request.form['storage_location']
        expiration_date = request.form['expiration_date']
        if expiration_date == '不明':
            product.expiration_date = '不明'
        else:
            product.expiration_date = datetime.strptime(request.form['expiration_date_input'], '%Y-%m-%d').strftime('%Y-%m-%d')
        product.remarks = request.form['remarks']
        product.last_updated = datetime.now(pytz.timezone('Asia/Tokyo'))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)