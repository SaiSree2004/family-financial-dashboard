import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Streamlit app title
st.title("Family Financial Health Dashboard")

# Section for user input
st.header("Enter Financial Data")
family_id = st.text_input("Family ID", "FAM001")
income = st.number_input("Monthly Income", value=5000, step=100)
savings = st.number_input("Savings", value=1000, step=100)
expenses = st.number_input("Monthly Expenses", value=2000, step=100)
loan_payments = st.number_input("Loan Payments", value=500, step=50)
credit_card_spending = st.number_input("Credit Card Spending", value=300, step=50)
financial_goals_met = st.slider("Financial Goals Met (%)", min_value=0, max_value=100, value=50)
month = st.number_input("Month (1-12)", value=11, step=1, min_value=1, max_value=12)

# CSV Upload
st.header("Upload Financial Data (Optional)")
uploaded_file = st.file_uploader("Upload your financial data (CSV)", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:")
    st.dataframe(data)

# API URLs (update these if deployed on a different server)
score_api_url = "http://127.0.0.1:5000/score"
predict_api_url = "http://127.0.0.1:5000/predict_expenses"

# Call Flask API for scoring
if st.button("Calculate Financial Score"):
    # Prepare input data
    input_data = {
        "Income": income,
        "Savings": savings,
        "Monthly Expenses": expenses,
        "Loan Payments": loan_payments,
        "Credit Card Spending": credit_card_spending,
        "Financial Goals Met (%)": financial_goals_met
    }

    try:
        # Call the scoring API
        response = requests.post(score_api_url, json=input_data)
        result = response.json()
        financial_score = result.get("financial_score", 0)

        # Display the score
        st.subheader(f"Financial Score: {financial_score}/100")

        # Financial Recommendations
        st.header("Recommendations")
        if financial_score < 50:
            st.warning("Your financial health is below average. Consider reducing discretionary spending.")
        elif financial_score < 75:
            st.info("Your financial health is good, but there's room for improvement. Keep saving!")
        else:
            st.success("Excellent financial health! Keep up the great work!")

        # Visualizations
        st.header("Visualizations")

        # Spending distribution (Pie chart)
        st.subheader("Spending Distribution")
        spending_labels = ['Savings', 'Expenses', 'Loan Payments', 'Credit Card Spending']
        spending_values = [savings, expenses, loan_payments, credit_card_spending]

        fig, ax = plt.subplots()
        ax.pie(spending_values, labels=spending_labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        st.pyplot(fig)

        # Category-wise spending (Bar chart)
        st.subheader("Category-Wise Spending")
        categories = ['Savings', 'Expenses', 'Loan Payments', 'Credit Card Spending']
        amounts = [savings, expenses, loan_payments, credit_card_spending]
        df = pd.DataFrame({'Category': categories, 'Amount': amounts})

        chart = alt.Chart(df).mark_bar().encode(
            x='Category',
            y='Amount',
            color='Category'
        )
        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"Error connecting to the API: {e}")

# Call Flask API for expense prediction
if st.button("Predict Next Month's Expenses"):
    # Prepare input data
    input_data = {
        "Income": income,
        "Savings": savings,
        "Monthly Expenses": expenses,
        "Loan Payments": loan_payments,
        "Month": month
    }

    try:
        # Call the prediction API
        response = requests.post(predict_api_url, json=input_data)
        result = response.json()
        predicted_expenses = result.get("predicted_expenses", 0)

        # Display the predicted expenses
        st.subheader(f"Predicted Next Month's Expenses: ${predicted_expenses}")

    except Exception as e:
        st.error(f"Error connecting to the API for prediction: {e}")
