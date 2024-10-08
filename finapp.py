import streamlit as st
import pandas as pd
import plotly.express as px

# Function to calculate key financial indicators
def calculate_indicators(data):
    # Initialize results dictionary
    results = {}
    
    # Calculate key indicators
    if 'Revenue' in data and 'Net Income' in data:
        results['ROI (%)'] = (data['Net Income'] / data['Revenue']) * 100
    
    if 'Net Income' in data and 'Total Revenue' in data:
        results['Profit Margin (%)'] = (data['Net Income'] / data['Total Revenue']) * 100
    
    if 'Current Assets' in data and 'Current Liabilities' in data:
        results['Current Ratio'] = data['Current Assets'] / data['Current Liabilities']
    
    if 'Total Assets' in data and 'Total Liabilities' in data:
        results['Debt-to-Equity Ratio'] = data['Total Liabilities'] / (data['Total Assets'] - data['Total Liabilities'])
    
    if 'Net Income' in data and 'Shareholder Equity' in data:
        results['Return on Equity (ROE) (%)'] = (data['Net Income'] / data['Shareholder Equity']) * 100
    
    if 'Net Income' in data and 'Shares Outstanding' in data:
        results['Earnings Per Share (EPS)'] = data['Net Income'] / data['Shares Outstanding']

    # Convert results into a DataFrame with a single row
    return pd.DataFrame([results])  # Wrap results in a list to create a single-row DataFrame

# Function to visualize the financial indicators
def visualize_indicators(indicators_df):
    st.write("### Financial Indicators Visualization")

    # Line chart for indicators
    line_fig = px.line(indicators_df, title='Key Financial Indicators Over Time', markers=True)
    st.plotly_chart(line_fig)

    # Bar chart for indicators
    indicators_df.reset_index(drop=True, inplace=True)
    bar_fig = px.bar(indicators_df.melt(var_name='Indicator', value_name='Value'), 
                     x='Indicator', y='Value', 
                     title='Key Financial Indicators (Bar Chart)',
                     text='Value')  # Set text to show the value of each bar
    st.plotly_chart(bar_fig)

    # Pie chart for revenue distribution if applicable
    if 'ROI (%)' in indicators_df.columns and 'Profit Margin (%)' in indicators_df.columns:
        revenue_distribution = indicators_df[['ROI (%)', 'Profit Margin (%)']]
        pie_fig = px.pie(values=revenue_distribution.values.flatten(), 
                         names=revenue_distribution.columns, 
                         title='Revenue Distribution by Key Indicators')
        st.plotly_chart(pie_fig)

# Streamlit app layout
def main():
    st.title("Professional Financial Analysis App")
    st.write("Input your financial data to analyze key financial indicators.")

    # Input fields for financial data
    st.subheader("Enter your financial data:")

    # Create a form for user input
    with st.form(key='financial_data_form'):
        revenue = st.number_input("Total Revenue ($)", min_value=0.0, format="%.2f")
        net_income = st.number_input("Net Income ($)", min_value=0.0, format="%.2f")
        total_assets = st.number_input("Total Assets ($)", min_value=0.0, format="%.2f")
        current_assets = st.number_input("Current Assets ($)", min_value=0.0, format="%.2f")
        current_liabilities = st.number_input("Current Liabilities ($)", min_value=0.0, format="%.2f")
        total_liabilities = st.number_input("Total Liabilities ($)", min_value=0.0, format="%.2f")
        shareholder_equity = st.number_input("Shareholder Equity ($)", min_value=0.0, format="%.2f")
        shares_outstanding = st.number_input("Shares Outstanding", min_value=0)

        submit_button = st.form_submit_button("Calculate Indicators")

    if submit_button:
        # Create a DataFrame for the inputs
        data = {
            'Revenue': revenue,
            'Net Income': net_income,
            'Total Assets': total_assets,
            'Current Assets': current_assets,
            'Current Liabilities': current_liabilities,
            'Total Liabilities': total_liabilities,
            'Shareholder Equity': shareholder_equity,
            'Shares Outstanding': shares_outstanding
        }
        
        # Calculate the indicators
        indicators_df = calculate_indicators(data)

        # Show the results
        st.write("### Calculated Financial Indicators")
        st.write(indicators_df)

        # Visualize the indicators
        visualize_indicators(indicators_df)

        # Export functionality
        if st.button("Download Indicators Data"):
            csv = indicators_df.to_csv().encode('utf-8')
            st.download_button("Download CSV", csv, "financial_indicators.csv", "text/csv")

if __name__ == "__main__":
    main()

