import streamlit as st
import pandas as pd

# 1. Page Configuration Setup
st.set_page_config(
    page_title="Supermarket Retail Sales Dashboard",
    page_icon="🛍️",
    layout="wide"
)

st.title("📊 Interactive Supermarket Retail Sales Dashboard")
st.markdown("Analyze baseline transaction metrics, performance tracking metrics, and branch profiles live.")

# 2. Ingest Dataset with Caching to Improve Performance
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/juarezefren/datasets/main/supermarket_sales.csv'
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    data['Date'] = pd.to_datetime(data['Date'])
    return data

df = load_data()

# 3. Sidebar Filtering Options
st.sidebar.header("🎯 Filter Options")
city_filter = st.sidebar.multiselect(
    "Select Target Cities:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_filter = st.sidebar.multiselect(
    "Select Customer Segment:",
    options=df["Customer type"].unique(),
    default=df["Customer type"].unique()
)

# Apply Active Filters dynamically to Data View Layers
filtered_df = df[
    (df["City"].isin(city_filter)) & 
    (df["Customer type"].isin(customer_filter))
]

# 4. Top-level Summary KPI Blocks
total_revenue = filtered_df["Total"].sum()
total_transactions = filtered_df.shape[0]
avg_rating = filtered_df["Rating"].mean()

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="💰 Total Sales Revenue", value=f"${total_revenue:,.2f}")
with kpi2:
    st.metric(label="📦 Transactions Tracked", value=f"{total_transactions:,}")
with kpi3:
    st.metric(label="⭐ Avg Customer Rating", value=f"{avg_rating:.2f} / 10")

st.divider()

# 5. Visual Layer Realization
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Daily Sales Performance Trend")
    daily_sales = filtered_df.groupby('Date')['Total'].sum()
    # Streamlit native interactive line charting
    st.line_chart(daily_sales)

with chart_col2:
    st.subheader("🏢 Operational Revenue by Branch")
    branch_sales = filtered_df.groupby('Branch')['Total'].sum()
    # Streamlit native interactive bar charting
    st.bar_chart(branch_sales)

# 6. Granular Data Preview Matrix
st.subheader("📋 Ingested Transaction Log")
st.dataframe(filtered_df, use_container_width=True)
