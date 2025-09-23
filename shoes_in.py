import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

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

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
sb.barplot(x="Subsidiary", y="Sales", data=filtered, ax=ax)
plt.xticks(rotation=45)
ax.set_title(f"Sales by Subsidiary in {region}")
st.pyplot(fig)
