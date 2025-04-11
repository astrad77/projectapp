import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Electricity and Renewables", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("electricity.csv", parse_dates=["date"])
    return df

df = load_data()

# Sidebar
st.sidebar.header("Controls")
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df["date"].min(), df["date"].max()],
    min_value=df["date"].min(),
    max_value=df["date"].max()
)

price_sector = st.sidebar.selectbox(
    "Select Price Sector",
    ["price_all", "price_residential", "price_commercial", "price_industrial"]
)

rolling_window = st.sidebar.slider(
    "Smoothing (Rolling Average Window, in Months)",
    min_value=1,
    max_value=12,
    value=3
)

show_raw = st.sidebar.checkbox("Show Raw Data", False)

# Filter data
df_filtered = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

# Tabs
tab1, tab2 = st.tabs(["📈 Price Trends", "🔍 Correlation Analysis"])

with tab1:
    st.subheader(f"{price_sector.replace('price_', '').capitalize()} Price vs Production Over Time")
    df_plot = df_filtered.copy()
    df_plot[price_sector] = df_plot[price_sector].rolling(rolling_window).mean()
    df_plot["production"] = df_plot["production"].rolling(rolling_window).mean()

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()
    ax1.plot(df_plot["date"], df_plot[price_sector], color="blue", label="Price")
    ax2.plot(df_plot["date"], df_plot["production"], color="green", label="Production", alpha=0.6)

    ax1.set_ylabel("Price (¢/kWh)", color="blue")
    ax2.set_ylabel("Production (MWh)", color="green")
    ax1.set_xlabel("Date")
    st.pyplot(fig)

with tab2:
    st.subheader("Correlation Between Production and Prices")
    fig2, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=df_filtered,
        x="production",
        y=price_sector,
        ax=ax,
        color="purple"
    )
    ax.set_xlabel("Production (MWh)")
    ax.set_ylabel(f"{price_sector.replace('price_', '').capitalize()} Price (¢/kWh)")
    st.pyplot(fig2)

if show_raw:
    st.subheader("Raw Data")
    st.dataframe(df_filtered)


