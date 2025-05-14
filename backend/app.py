import os
import openai
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# 🔐 Set your OpenAI API key (preferably from environment variables)
openai.api_key = os.getenv('OPENAI_API_KEY', 'your-api-key-here')  # Replace or set in env

print("Starting server...")

app = Flask(__name__)
CORS(app)

# ✅ Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ✅ Expense categorization using OpenAI GPT
def categorize_expense(feature):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial assistant who classifies expenses into categories like Food, Transport, Shopping, Bills, Finance, Entertainment, Health, or Other."},
                {"role": "user", "content": f"What category does this expense belong to: '{feature}'?"}
            ],
            temperature=0.2,
            max_tokens=10
        )
        category = response['choices'][0]['message']['content'].strip()
        return category if category else "Other"
    except Exception as e:
        print("OpenAI error:", e)
        return "Other"

# ✅ User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# ✅ Expense model with category
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False, default='Other')

# ✅ Create tables
with app.app_context():
    db.create_all()

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

# ✅ Expense management endpoint
@app.route('/api/expenses', methods=['GET', 'POST'])
def manage_expenses():
    if request.method == 'POST':
        data = request.get_json()
        feature = data.get('feature')
        amount = data.get('amount')

        if not feature or amount is None:
            return jsonify({'error': 'Feature and amount are required'}), 400

        category = categorize_expense(feature)
        new_expense = Expense(feature=feature, amount=amount, category=category)
        db.session.add(new_expense)
        db.session.commit()

        return jsonify({'message': f'Expense added to category: {category}'}), 201

    else:  # GET
        expenses = Expense.query.all()
        return jsonify([
            {'feature': e.feature, 'amount': e.amount, 'category': e.category}
            for e in expenses
        ])

# ✅ Run the app
if __name__ == '__main__':
    print("Running Flask app...")
    app.run(debug=True)
