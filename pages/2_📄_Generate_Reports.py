import streamlit as st

st.set_page_config(
    page_title="Generate Reports",
    page_icon="📄",
    layout="wide"
)

import asyncio
import io
import os
import pathlib
from os.path import isfile, join
import pandas as pd
import helpers.sidebar
import helpers.util
import services.prompts
import services.llm
import helpers.util

helpers.sidebar.show()

st.header("Generate Reports")
st.write("Create tailored financial documents, based on sample datasets.  Choose your sample dataset and generate "
         "reports.")

# Add a sidebar option to select a sample dataset (csv file)
parent_path = pathlib.Path(__file__).parent.parent.resolve()
data_path = os.path.join(parent_path, "data")
tx_files = [f for f in os.listdir(data_path) if isfile(join(data_path, f))]
tx_dataset_name = st.sidebar.selectbox('Pick a transaction sample dataset', tx_files)

# Add a sidebar option to select a document type
document_type = st.sidebar.selectbox("Select a document type:",
                                     ["Spending by Category", "Spending by Tag"])

generate_button_sb = st.sidebar.button("Generate Report&nbsp;&nbsp;➠", type="primary", key="generate_button_sb")

# Load and display the selected dataset
file_location = os.path.join(data_path, tx_dataset_name)
data_frame = pd.read_csv(file_location)

st.markdown("### Incoming Transactions Data")
st.dataframe(data_frame, use_container_width=True, height=200)

report_data, report_advice = st.columns([12, 10], gap="medium")


def filter_transactions(df: pd.DataFrame) -> pd.DataFrame:
    # Exclude positive amount transactions (income) and transfers/Paypal transactions
    filtered_data = data_frame[(df['Amount'] < 0) &
                               (~df['Account'].str.contains('Paypal', case=False)) &
                               (~df['Category'].str.contains('Transfer', case=False))].copy()
    # Make all transaction amounts positive (now they are expenses) for easier analysis
    filtered_data['Amount'] = filtered_data['Amount'].abs()
    return filtered_data


if generate_button_sb:
    filtered_data = filter_transactions(data_frame)

    # Calculate the most used account by number of transactions
    most_used_account_by_transactions: str = filtered_data['Account'].value_counts().idxmax()

    # Calculate the top 3 most spendy accounts by amount of money
    top_spendy_accounts: pd.DataFrame = filtered_data.groupby('Account')['Amount'].sum().sort_values(
        ascending=False).head(3)

    with report_data:
        st.markdown(f"### {document_type} Report Data")

    with report_advice:
        st.markdown(f"### {document_type} Advice")
        advice = st.empty()

    if document_type == "Spending by Category":
        # Calculate spending by category
        category_summary: pd.DataFrame = filtered_data.groupby('Category').agg({
            'Amount': ['sum', 'mean', 'count']
        }).reset_index()
        category_summary.columns = ['Category', 'Total $ spent', 'Average/Tx', '# Tx']
        category_summary['Average/Tx'] = category_summary['Average/Tx'].round(2)

        # Calculate most 3 spendy categories by transaction count
        most_spendy_categories_by_count: pd.DataFrame = category_summary.sort_values('# Tx', ascending=False).head(
            3)
        most_spendy_categories_by_count['Average/Tx'] = most_spendy_categories_by_count['Average/Tx'].round(2)

        # Calculate most 3 spendy categories by total amount
        most_spendy_categories_by_amount: pd.DataFrame = category_summary.sort_values('Total $ spent',
                                                                                      ascending=False).head(3)
        most_spendy_categories_by_amount['Average/Tx'] = most_spendy_categories_by_amount['Average/Tx'].round(2)

        category_summary_advice_prompt = services.prompts.category_summary_prompt(
            category_summary.to_markdown(),
            most_spendy_categories_by_amount.to_markdown(),
            most_spendy_categories_by_count.to_markdown(),
            most_used_account_by_transactions,
            top_spendy_accounts.to_markdown())


        with report_data:
            left_details, right_details = st.columns([1, 1])
            with left_details:
                st.write("Summary of spending by category:")
                st.write(category_summary)
                st.write("\nMost used account by number of transactions:", most_used_account_by_transactions)

            with right_details:
                st.write("\nTop 3 most spendy accounts by amount of money:")
                st.write(top_spendy_accounts)

                st.write("\nMost 3 spendy categories by total amount:")
                st.write(most_spendy_categories_by_amount)

                st.write("\nMost 3 spendy categories by transaction count:")
                st.write(most_spendy_categories_by_count)

            asyncio.run(helpers.util.run_prompt(category_summary_advice_prompt, advice))

    elif document_type == "Spending by Tag":
        # Calculate spending by tag
        tag_summary = filtered_data.groupby('Tag').agg({
            'Amount': ['sum', lambda x: (x.sum() / filtered_data['Amount'].sum()) * 100, 'count']
        }).reset_index()
        tag_summary.columns = ['Tag', 'Total $ spent', '% of total spend', '# Tx']
        tag_summary = tag_summary.sort_values('% of total spend', ascending=False)

        tag_summary_advice_prompt = services.prompts.tag_summary_prompt(
            tag_summary.to_markdown(),
            most_used_account_by_transactions,
            top_spendy_accounts.to_markdown())

        with report_data:
            st.write(tag_summary)

            # Streamlit app
            st.write("\nTop 3 most spendy accounts by amount of money:")
            st.write(top_spendy_accounts)
        asyncio.run(helpers.util.run_prompt(tag_summary_advice_prompt, advice))
