from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

# Start Database
with app.app_context():
    db.create_all()

# Routes
@app.route('/allCustomers', methods=['GET'])
def all_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'email': c.email, 'password': c.password} for c in customers])

@app.route('/newCustomer', methods=['POST'])
def create_customer():
    data = request.json
    new_customer = Customer(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created successfully!'})

# Update Customer Route
@app.route('/updateCustomer/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    customer = Customer.query.get(id)
    
    if customer:
        customer.name = data['name']
        customer.email = data['email']
        customer.password = data['password']
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully!'})
    
    return jsonify({'message': 'Customer not found'}), 404

@app.route('/allProducts', methods=['GET'])
def all_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'details': p.details, 'price': p.price} for p in products])

@app.route('/newProduct', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(name=data['name'], details=data['details'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully!'})

@app.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify({'name': product.name, 'details': product.details, 'price': product.price})
    return jsonify({'message': 'Product not found'}), 404

@app.route('/updateProduct/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    product = Product.query.get(id)
    
    if product:
        product.name = data['name']
        product.details = data['details']
        product.price = data['price']
        db.session.commit()
        return jsonify({'message': 'Product updated successfully!'})
    
    return jsonify({'message': 'Product not found'}), 404

@app.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)  
    if customer:
   
        return jsonify({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'password': customer.password
        })
    else:
        return jsonify({'message': 'Customer not found'}), 404

@app.route('/deleteCustomer/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully!'})
    else:
        return jsonify({'message': 'Customer not found'}), 404

@app.route('/allOrders', methods=['GET'])
def all_orders():
    try:
        orders = Order.query.all()
        return jsonify([{
            'id': order.id,
            'product_id': order.product_id,
            'customer_id': order.customer_id
        } for order in orders])
    except Exception as e:
        return jsonify({'message': f'Error fetching orders: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
