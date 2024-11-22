import streamlit as st 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.figure_factory as ff 
import plotly.express as px 

@st.cache_data
def load_data():
    df = pd.read_csv("./Unicorn_Companies.csv")
    df.loc[:,"Valuation ($)"] = df.loc[:,"Valuation"].str.replace("$","").str.replace("B","000000000").astype("int64")
    df.loc[:,"Funding ($)"] = df.loc[:,"Funding"].str.replace("Unknown","-1").str.replace("$","").str.replace("M","000000").str.replace("B","000000000").astype("int64")
    df.drop(columns=["Valuation","Funding"], axis=1, inplace=True)
    df['Date Joined'] = pd.to_datetime(df['Date Joined'], format="mixed")
    df.loc[:,"Year Joined"] = df["Date Joined"].dt.year
    df.loc[:, "Years to unicorn status"] = df["Year Joined"] - df["Year Founded"]
    df.loc[:,"Count"] = 1

    return df

df = load_data()

st.title("Unicorn Companies App")

# create filters
# dynamic filter for multiple fields 
filters = {
    "Industry": df["Industry"].unique(),
    "Country/Region": df["Country/Region"].unique(),
    "Year Founded": df["Year Founded"].unique(),
    "City": df["City"].unique(),
    "Year Joined": df["Year Joined"].unique()
}
# Store user selections
selected_filters = {}
# Generate multiselect widgets dynamically
for key, options in filters.items():
    selected_filters[key] = st.sidebar.multiselect(key, options)
# Filter the data dynamically
filtered_data = df  # Start with the full dataset
for key, selected_values in selected_filters.items():
    if selected_values:  # Apply filter only if a selection is made
        filtered_data = filtered_data[filtered_data[key].isin(selected_values)]
# Display the filtered data
st.dataframe(filtered_data)

# display the table
# st.dataframe(combined_table)
# calculate some metrics
no_of_companies = len(filtered_data)
total_valuation = f"$ {round(filtered_data["Valuation ($)"].sum() / 1000000000, 2)} B"
total_funding = f"$ {round(filtered_data["Funding ($)"].sum() / 1000000000, 2)} B"


# display these metrics 
# using streamlit container / column components

col1, col2, col3 = st.columns(3)
with col1:
    # st.write("Summary of Dataset Columns")
    st.metric("No of Companies",no_of_companies)

with col2:
    st.metric("Total Valuation", total_valuation)

with col3:
    st.metric("Total Funding", total_funding)


# create diferent charts 
con = st.container()

with con:
    # matplotlib / seaborn
    st.subheader("Charts section")
    bar_plot_1 = sns.countplot(data=filtered_data, x=filtered_data['Industry'])
    plt.xticks(rotation=45)
    plt.ylabel("No of companies")
    st.pyplot(bar_plot_1.get_figure())

    # plotly charts (pip install plotly: in the cmd)
    # line chart 
    line_1 = px.bar(filtered_data, x="Industry", y="Count")
    st.plotly_chart(line_1)


# investors table 
investors_list = filtered_data["Select Investors"].str.split(",").explode().str.strip()
investors_df = investors_list.value_counts().reset_index()
investors_df.columns = ['Investor', 'Company Counts']

st.title("Investors Data")
st.dataframe(investors_df)