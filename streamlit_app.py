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

# DEBUG: show available columns
# st.write("Columns:", df.columns.tolist())

# Safely detect relevant columns
year_col = [col for col in df.columns if "year" in col.lower()][0]
miif_col = [col for col in df.columns if "miif" in col.lower()][0]
province_col = [col for col in df.columns if "province" in col.lower()][0]

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Select Year", sorted(df[year_col].dropna().unique(), reverse=True))
miif_class = st.sidebar.selectbox("Select MIIF Class", sorted(df[miif_col].dropna().unique()))
province = st.sidebar.selectbox("Select Province", ["All"] + sorted(df[province_col].dropna().unique()))

# Filtered data
filtered_df = df[df[year_col] == year]
if miif_class:
    filtered_df = filtered_df[df[miif_col] == miif_class]
if province != "All":
    filtered_df = filtered_df[df[province_col] == province]

# Display table
st.subheader("Filtered Municipalities")
display_cols = [col for col in df.columns if any(k in col for k in ["municipality", "province", "miif", "gpi_score", "gpi_rank"])]
st.dataframe(filtered_df[display_cols].sort_values(display_cols[-1]))

# Download
st.download_button("Download CSV", filtered_df.to_csv(index=False), "gpi_filtered.csv", "text/csv")

# Close DB connection
conn.close()
