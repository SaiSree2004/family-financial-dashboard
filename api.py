from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the saved regression model for expense prediction
with open("expense_prediction_model.pkl", "rb") as file:
    prediction_model = pickle.load(file)

# Scoring function
def calculate_score(data):
    income = data["Income"]
    savings = data["Savings"]
    expenses = data["Monthly Expenses"]
    loan_payments = data["Loan Payments"]
    credit_card_spending = data["Credit Card Spending"]
    goals_met = data["Financial Goals Met (%)"]

    # Example scoring calculation with weights
    score = (savings / income) * 40 + (1 - (expenses / income)) * 20 + \
            (1 - (loan_payments / income)) * 10 + \
            (1 - (credit_card_spending / income)) * 10 + \
            (goals_met / 100) * 20
    return round(score, 2)

@app.route('/score', methods=['POST'])
def score_family():
    """
    Calculate the financial score for a family.
    """
    family_data = request.get_json()
    score = calculate_score(family_data)
    return jsonify({"financial_score": score})

@app.route('/predict_expenses', methods=['POST'])
def predict_expenses():
    """
    Predict next month's expenses based on historical financial data.
    """
    input_data = request.get_json()
    
    # Prepare input for prediction
    df = pd.DataFrame([input_data])
    features = ['Income', 'Savings', 'Monthly Expenses', 'Loan Payments', 'Month']
    prediction = prediction_model.predict(df[features])[0]

    return jsonify({"predicted_expenses": round(prediction, 2)})

if __name__ == '__main__':
    app.run(debug=True)
