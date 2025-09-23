import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("SHOES.csv")

# Clean Sales column
df["Sales"] = df["Sales"].replace('[$,]', '', regex=True).astype("int64")

# Streamlit title
st.title("Shoes Sales Dashboard")

# Region selection dropdown
region = st.selectbox("Select a Region:", df["Region"].unique())

# Filter data based on region
filtered = df[df["Region"] == region]

# Plotly interactive bar chart
fig = px.bar(
    filtered,
    x="Subsidiary",
    y="Sales",
    color="Subsidiary",
    title=f"Sales by Subsidiary in {region}",
    text="Sales"
)

fig.update_traces(texttemplate='%{text:,}', textposition="outside")
fig.update_layout(xaxis_tickangle=-45, showlegend=False)

# Show chart
st.plotly_chart(fig, use_container_width=True)
