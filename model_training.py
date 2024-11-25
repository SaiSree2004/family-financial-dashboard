import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Load dataset
file_path = r"C:\Users\gvnss\Downloads\family_financial_and_transactions_data.xlsx"  
data = pd.read_excel(file_path)

# Prepare data
data['Transaction Date'] = pd.to_datetime(data['Transaction Date'])
data['Month'] = data['Transaction Date'].dt.month
features = ['Income', 'Savings', 'Monthly Expenses', 'Loan Payments', 'Month']
target = 'Monthly Expenses'

X = data[features]
y = data[target]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model
with open("expense_prediction_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model training complete! Saved as expense_prediction_model.pkl.")
