import pandas as pd
import os
from datetime import datetime
import json

class ExpenseTracker:
    def __init__(self):
        self.data_file = "expenses.csv"
        self.budget_file = "budget.json"
        self.categories = [
            "Food", "Transportation", "Housing", "Utilities",
            "Entertainment", "Shopping", "Healthcare", "Other"
        ]
        
        # Initialize or load existing data
        if not os.path.exists(self.data_file):
            self.expenses_df = pd.DataFrame(columns=[
                'date', 'amount', 'category', 'description'
            ])
            self.expenses_df.to_csv(self.data_file, index=False)
        else:
            self.expenses_df = pd.read_csv(self.data_file)
            self.expenses_df['date'] = pd.to_datetime(self.expenses_df['date'])

        # Initialize or load budget
        if not os.path.exists(self.budget_file):
            self.budget = {"monthly_budget": 1000}
            self.save_budget()
        else:
            with open(self.budget_file, 'r') as f:
                self.budget = json.load(f)

    def add_expense(self, amount, category, description):
        new_expense = pd.DataFrame([{
            'date': datetime.now(),
            'amount': amount,
            'category': category,
            'description': description
        }])
        self.expenses_df = pd.concat([self.expenses_df, new_expense], ignore_index=True)
        self.expenses_df.to_csv(self.data_file, index=False)

    def get_monthly_expenses(self):
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_data = self.expenses_df[
            (self.expenses_df['date'].dt.month == current_month) &
            (self.expenses_df['date'].dt.year == current_year)
        ]
        return monthly_data

    def get_monthly_total(self):
        monthly_data = self.get_monthly_expenses()
        return monthly_data['amount'].sum()

    def get_category_totals(self):
        monthly_data = self.get_monthly_expenses()
        return monthly_data.groupby('category')['amount'].sum()

    def set_budget(self, amount):
        self.budget["monthly_budget"] = amount
        self.save_budget()

    def get_budget(self):
        return self.budget["monthly_budget"]

    def save_budget(self):
        with open(self.budget_file, 'w') as f:
            json.dump(self.budget, f)

    def get_budget_status(self):
        monthly_total = self.get_monthly_total()
        budget = self.get_budget()
        remaining = budget - monthly_total
        percentage_used = (monthly_total / budget) * 100 if budget > 0 else 0
        return {
            'total': monthly_total,
            'budget': budget,
            'remaining': remaining,
            'percentage_used': percentage_used
        }
