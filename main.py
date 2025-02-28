import streamlit as st
import pandas as pd
from data_handler import ExpenseTracker
from visualizations import (
    create_category_pie_chart,
    create_budget_gauge,
    create_daily_expenses_line
)

# Initialize the expense tracker
@st.cache_resource
def get_tracker():
    return ExpenseTracker()

tracker = get_tracker()

# Page configuration
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Title and description
st.title("💰 Personal Expense Tracker")
st.markdown("""
    Keep track of your expenses and monitor your budget with this simple tool.
    Add new expenses, set your monthly budget, and view your spending patterns.
""")

# Sidebar for adding new expenses and setting budget
with st.sidebar:
    st.header("Add New Expense")
    with st.form("expense_form", clear_on_submit=True):
        amount = st.number_input("Amount ($)", min_value=0.01, format="%f")
        category = st.selectbox("Category", tracker.categories)
        description = st.text_input("Description")
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            tracker.add_expense(amount, category, description)
            st.success("Expense added successfully!")

    st.header("Set Monthly Budget")
    with st.form("budget_form"):
        current_budget = tracker.get_budget()
        new_budget = st.number_input(
            "Monthly Budget ($)",
            min_value=0.0,
            value=float(current_budget),
            format="%f"
        )
        budget_submitted = st.form_submit_button("Update Budget")
        
        if budget_submitted:
            tracker.set_budget(new_budget)
            st.success("Budget updated successfully!")

# Main content area
col1, col2 = st.columns(2)

# Budget Status
with col1:
    st.subheader("Budget Status")
    status = tracker.get_budget_status()
    
    # Create metrics
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    with col_metric1:
        st.metric("Total Spent", f"${status['total']:.2f}")
    with col_metric2:
        st.metric("Budget", f"${status['budget']:.2f}")
    with col_metric3:
        st.metric("Remaining", f"${status['remaining']:.2f}")
    
    # Budget gauge
    st.plotly_chart(
        create_budget_gauge(status['percentage_used']),
        use_container_width=True
    )

    # Budget notifications
    if status['percentage_used'] >= 90:
        st.error("⚠️ Warning: You've used 90% or more of your monthly budget!")
    elif status['percentage_used'] >= 75:
        st.warning("⚠️ Notice: You've used 75% of your monthly budget.")
    else:
        st.success("✅ You're within your budget limits!")

# Expense Analysis
with col2:
    st.subheader("Expense Analysis")
    category_totals = tracker.get_category_totals()
    st.plotly_chart(
        create_category_pie_chart(category_totals),
        use_container_width=True
    )

# Recent Expenses
st.subheader("Recent Expenses")
monthly_expenses = tracker.get_monthly_expenses()
if not monthly_expenses.empty:
    st.plotly_chart(
        create_daily_expenses_line(monthly_expenses),
        use_container_width=True
    )
    
    # Display expense table
    st.dataframe(
        monthly_expenses.sort_values('date', ascending=False)
        .style.format({
            'amount': '${:.2f}',
            'date': lambda x: x.strftime('%Y-%m-%d %H:%M')
        }),
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("No expenses recorded for this month yet.")
