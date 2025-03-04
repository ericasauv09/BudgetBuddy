import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_category_pie_chart(category_totals):
    if not isinstance(category_totals, pd.Series):
        raise ValueError("category_totals must be a Pandas Series")
    fig = px.pie(
        values=category_totals.values,
        names=category_totals.index,
        title='Expenses by Category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_budget_gauge(percentage_used):
    if not isinstance(percentage_used, (int, float)):
        raise ValueError("percentage_used must be a numeric value")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage_used,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Budget Usage"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgreen"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))
    return fig

def create_daily_expenses_line(expenses_df):
    if not isinstance(expenses_df, pd.DataFrame):
        raise ValueError("expenses_df must be a Pandas DataFrame")
    daily_expenses = expenses_df.groupby('date')['amount'].sum().reset_index()
    fig = px.line(
        daily_expenses,
        x='date',
        y='amount',
        title='Daily Expenses Trend',
        labels={'amount': 'Amount ($)', 'date': 'Date'}
    )
    return fig
