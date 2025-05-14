import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

print("Starting server...")

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
CORS(app)

# ✅ Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# ✅ Expense model without category classification logic
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False, default='Other')

# ✅ Create tables
with app.app_context():
    db.create_all()

# ✅ Serve index.html at root
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

# ✅ Serve register.html (or any other HTML file)
@app.route('/register')
def serve_register():
    return send_from_directory('../frontend', 'register.html')

@app.route('/personal')
def serve_personal():
    return send_from_directory('../frontend', 'personal.html')

# ✅ Serve static files (JS, CSS, etc.)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

# ✅ User registration endpoint
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    account = data.get('account')
    email = data.get('email')

    if not account or not email:
        return jsonify({'error': 'Account number and email are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    new_user = User(account=account, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# ✅ Expense management endpoint (category set to 'Other' by default)
@app.route('/api/expenses', methods=['GET', 'POST'])
def manage_expenses():
    if request.method == 'POST':
        data = request.get_json()
        feature = data.get('feature')
        amount = data.get('amount')

        if not feature or amount is None:
            return jsonify({'error': 'Feature and amount are required'}), 400

        new_expense = Expense(feature=feature, amount=amount, category="Other")
        db.session.add(new_expense)
        db.session.commit()

        return jsonify({'message': 'Expense added successfully'}), 201

    else:  # GET
        expenses = Expense.query.all()
        return jsonify([
            {'feature': e.feature, 'amount': e.amount, 'category': e.category}
            for e in expenses
        ])

# ✅ Run the app
if __name__ == '__main__':
    print("Running Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
