import streamlit as st
import requests
import pandas as pd

st.title("SpaceX Data Logistics System")

# AI used throughout this file to figure out StreamLit and properly display information
# AI used to debug and help match the frontend to the backend and make it work after Error 500s

APIUrl = "http://127.0.0.1:8000"

def fetch_data(endpoint):
    try:
        response = requests.get(f"{APIUrl}{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error: {e}")
        return None

st.header("Overview Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    data = fetch_data("/launches/count")
    if data and "totalCount" in data:
        st.metric("Total Launches", data["totalCount"])

with col2:
    data = fetch_data("/launches/countSuccess")
    if data and "totalCSuccessCount" in data:
        st.metric("Total Successes", data["totalSuccessCount"])

with col3:
    data = fetch_data("/launches/countFailed")
    if data and "totalFailCount" in data:
        st.metric("Total Failed", data["totalFailCount"])

st.header("Past Launch Analysis")

queryOption = st.selectbox(
    "Select Analysis:",
    [
        "Failed Launches",
        "Successful Launches",
        "Complete Launch Details",
        "Highest Stage Rockets",
        "Top Reused Cores"
    ]
)

if queryOption == "Failed Launches":
    data = fetch_data("/launches/failed")
    if data:
        st.write(f"Total Failed Launches: {data.get('count', 0)}")
        df = pd.DataFrame(data.get("launches", []))
        st.dataframe(df, use_container_width=True)

elif queryOption == "Successful Launches":
    data = fetch_data("/launches/succeeded")
    if data:
        st.write(f"Total Successful Launches: {data.get('count', 0)}")
        df = pd.DataFrame(data.get("launches", []))
        st.dataframe(df, use_container_width=True)

elif queryOption == "Complete Launch Details":
    data = fetch_data("/launches/details")
    if data:
        st.write(f"Total Records: {data.get('count', 0)}")
        df = pd.DataFrame(data.get("launches", []))
        st.dataframe(df, use_container_width=True)

elif queryOption == "Highest Stage Rockets":
    data = fetch_data("/rockets/highStage")
    if data:
        st.write(f"Maximum Stages: {data.get('highStage', 'N/A')}")
        df = pd.DataFrame(data.get("rockets", []))
        st.dataframe(df, use_container_width=True)

elif queryOption == "Top Reused Cores":
    limit = st.slider("Number of cores:", 1, 10, 5)
    data = fetch_data(f"/cores/reuseCount?limit={limit}")
    if data:
        df = pd.DataFrame(data.get("cores", []))
        st.dataframe(df, use_container_width=True)
