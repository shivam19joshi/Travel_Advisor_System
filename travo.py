import streamlit as st
import pandas as pd

# Sample destination dataset
destinations = [
    {"Country": "Thailand", "AvgCost": 50000, "BestMonths": ["November", "December", "January"]},
    {"Country": "Singapore", "AvgCost": 80000, "BestMonths": ["February", "March", "July"]},
    {"Country": "Indonesia (Bali)", "AvgCost": 60000, "BestMonths": ["April", "May", "September"]},
    {"Country": "Turkey", "AvgCost": 100000, "BestMonths": ["April", "May", "October"]},
    {"Country": "UAE (Dubai)", "AvgCost": 70000, "BestMonths": ["November", "December", "January"]},
    {"Country": "Georgia", "AvgCost": 65000, "BestMonths": ["April", "May", "September"]},
    {"Country": "Japan", "AvgCost": 120000, "BestMonths": ["March", "April", "November"]},
    {"Country": "Switzerland", "AvgCost": 200000, "BestMonths": ["June", "July", "December"]},
    {"Country": "Vietnam", "AvgCost": 55000, "BestMonths": ["January", "February", "March"]},
    {"Country": "Maldives", "AvgCost": 95000, "BestMonths": ["November", "December", "January"]}
]

# Convert to DataFrame
df = pd.DataFrame(destinations)

# Streamlit UI
st.title("🌍 Travel Recommendation App")

st.subheader("Plan Your Next Trip")

name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=100, value=25)
budget = st.number_input("Enter your travel budget (INR)", min_value=10000, value=60000, step=5000)
month = st.selectbox("Select your preferred travel month", 
                     ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December'])

if st.button("Suggest Destinations"):
    st.write(f"Hello **{name}** 👋, based on your budget of ₹{budget} and your travel month ({month}), here are some options:")

    filtered = df[(df["AvgCost"] <= budget) & (df["BestMonths"].apply(lambda x: month in x))]

    if not filtered.empty:
        st.table(filtered[["Country", "AvgCost"]].rename(columns={"Country": "Destination", "AvgCost": "Estimated Cost (INR)"}))
    else:
        st.warning("No destinations match your budget and preferred month. Try increasing your budget or changing the month.")

st.markdown("---")
