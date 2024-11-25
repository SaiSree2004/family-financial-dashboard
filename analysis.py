import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r"C:\Users\gvnss\Downloads\family_financial_and_transactions_data.xlsx"  # Replace with your file path
data = pd.read_excel(file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(data.head())

# Dataset Info
print("\nDataset Info:")
print(data.info())

# Check for missing values
print("\nMissing values in the dataset:")
print(data.isnull().sum())

# Basic statistics of numeric columns
print("\nBasic statistics of numeric columns:")
print(data.describe())

# Step 1: Calculate Family-level spending and financial score

# Family-wise total spending
data['Spending'] = data['Amount']  # Assuming 'Amount' is the spending column
family_spending = data.groupby('Family ID')['Spending'].sum()

# Calculate the financial score for each family
def calculate_score(row):
    if row['Income'] == 0:
        return 0
    savings_ratio = row['Savings'] / row['Income']
    expense_ratio = row['Monthly Expenses'] / row['Income']
    loan_ratio = row['Loan Payments'] / row['Income']
    financial_goals_met = row['Financial Goals Met (%)'] / 100
    
    # Scoring logic
    score = (savings_ratio * 50) - (expense_ratio * 30) - (loan_ratio * 10) + (financial_goals_met * 30)
    return max(0, min(100, score))  # Ensure score is between 0 and 100

# Apply the scoring function to the dataset
data['Financial Score'] = data.apply(calculate_score, axis=1)

# Family-wise financial scores
family_scores = data.groupby('Family ID')['Financial Score'].mean()

# Visualization 1: Spending distribution across categories
plt.figure(figsize=(10, 6))
category_spending = data.groupby('Category')['Amount'].sum().sort_values(ascending=False)
category_spending.plot(kind='bar', color='lightcoral')
plt.title('Spending Distribution by Category')
plt.xlabel('Category')
plt.ylabel('Total Spending')
plt.xticks(rotation=45, ha='right')
plt.show()

# Visualization 2: Family-wise financial scores
plt.figure(figsize=(12, 6))
family_scores = family_scores.sort_values(ascending=False)
family_scores.plot(kind='bar', color='skyblue')
plt.title('Family-Wise Financial Scores')
plt.xlabel('Family ID')
plt.ylabel('Average Financial Score')
plt.xticks(rotation=45, ha='right')
plt.show()

# Visualization 3: Member-wise spending trends
plt.figure(figsize=(12, 6))
member_spending_trends = data.groupby(['Family ID', 'Member ID'])['Amount'].sum().unstack()
member_spending_trends.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Member-Wise Spending Trends')
plt.xlabel('Family ID')
plt.ylabel('Total Spending')
plt.xticks(rotation=45, ha='right')
plt.show()

# Display family-wise financial scores
print("\nFamily-Wise Financial Scores:")
print(family_scores)

# Save the results to a CSV file if needed
family_scores.to_csv("family_scores.csv")
