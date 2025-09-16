import streamlit as st
import sqlite3
import pandas as pd

# Simple password protection
st.set_page_config(page_title="GPI Governance Risk Portal", layout="wide")
password = st.text_input("Enter password to access the GPI Portal:", type="password")
if password != "Hollard2024":
    st.stop()

st.title("Governance Performance Index (GPI) Dashboard")

# Connect to the SQLite database
conn = sqlite3.connect("GPI_Databank_2016_2024.sqlite")
df = pd.read_sql_query("SELECT * FROM gpi_databank", conn)

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", sorted(df["year"].dropna().unique(), reverse=True))
miif_class = st.sidebar.selectbox("Select MIIF Class", sorted(df["miif_class"].dropna().unique()))
province = st.sidebar.selectbox("Select Province", ["All"] + sorted(df["province"].dropna().unique()))

# Filtered data
filtered_df = df[df["year"] == year]
if miif_class:
    filtered_df = filtered_df[filtered_df["miif_class"] == miif_class]
if province != "All":
    filtered_df = filtered_df[filtered_df["province"] == province]

# Display table
st.subheader("Filtered Municipalities")
st.dataframe(filtered_df[["municipality", "province", "miif_class", "gpi_score", "gpi_rank"]].sort_values("gpi_rank"))

# Download
st.download_button("Download CSV", filtered_df.to_csv(index=False), "gpi_filtered.csv", "text/csv")

# Close DB connection
conn.close()
