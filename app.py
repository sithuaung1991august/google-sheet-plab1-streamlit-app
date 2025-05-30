import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import io # for text output of df.info()

st.set_page_config(layout="wide")
st.title("Google Sheet Data Viewer - Web Version")
st.markdown("Displaying data directly from a public Google Sheet, deployed entirely on the web.")

# --- Configuration for Public Sheet ---
# IMPORTANT: Ensure your Google Sheet is set to "Anyone with the link" as "Viewer"
# Paste your Google Sheet's shareable link here:
PUBLIC_SHEET_URL = "https://docs.google.com/spreadsheets/d/1rB2_E5wex8tpmZJvjBe-f4anGO-cg92SOvbdnV77RYg/edit?usp=sharing"

# Create a connection object to your Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Use st.cache_data to cache the data for faster loading.
# ttl (Time-To-Live) defines how long the data is cached before being re-fetched.
@st.cache_data(ttl=600) # Cache for 10 minutes (600 seconds)
def load_data(sheet_url):
    try:
        # Read the entire spreadsheet. You can also specify a worksheet name/index.
        # Change "Sheet1" below if your sheet has a different name
        df = conn.read(spreadsheet=sheet_url, worksheet="Sheet1", usecols=list(range(10))) # Added usecols as a safeguard
        return df
    except Exception as e:
        st.error(f"Error loading data from Google Sheet: {e}")
        st.warning("Please ensure the Google Sheet URL is correct and sharing is set to 'Anyone with the link' as 'Viewer'.")
        st.warning("Also, check your internet connection or Google API status.")
        return None

df = load_data(PUBLIC_SHEET_URL)

if df is not None:
    if not df.empty:
        st.write("### Data Preview")
        st.dataframe(df)

        st.write(f"### Data Shape: {df.shape[0]} rows, {df.shape[1]} columns")

        if st.checkbox("Show descriptive statistics"):
            st.write(df.describe())

        if st.checkbox("Show column information"):
            buffer = io.StringIO()
            df.info(buf=buffer)
            s = buffer.getvalue()
            st.text(s)
    else:
        st.info("The Google Sheet was loaded, but it appears to be empty.")
else:
    st.info("Failed to load data. Please review the URL and sharing settings of your Google Sheet.")

st.markdown("---")
st.markdown("Data powered by Google Sheets and deployed via Streamlit Community Cloud.")
