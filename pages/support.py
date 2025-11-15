import streamlit as st
import mysql.connector
from datetime import datetime
import pandas as pd
import altair as alt


## removing the sidebar from the streamlit page
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
        [data-testid="stHamburgerMenu"] { display: none; }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# ----------------------------------------------
# Creating Database Connection
# ----------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="246768@Rag",
        database="project"
    )

# ----------------------------------------------
# Fetching Queries from DB
# ----------------------------------------------
def fetch_queries(status_filter=None, category_filter=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM queries WHERE 1=1"
    params = []

    if status_filter and status_filter != "All":
        query += " AND state = %s"
        params.append(status_filter)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()
    return rows

# ----------------------------------------------
# Close a Query
# ----------------------------------------------
def close_query(query_id):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE queries
        SET state = 'Closed',
            closed_on = %s
        WHERE query_id = %s
    """

    values = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), query_id)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()

# ----------------------------------------------
#creating streamlit UI
# ----------------------------------------------
st.title(" Query Management Dashboard (Support Team)")

# ----------------------------------------------
# FILTERS
# ----------------------------------------------
st.subheader("Filter Queries")

left, right = st.columns(2)

status_filter = left.selectbox("Filter by state", ["All", "Open", "Closed"])

# ----------------------------------------------
# Fetch & Display Data
# ----------------------------------------------
queries = fetch_queries(status_filter,)

if queries:
    df = pd.DataFrame(queries)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No queries found for the selected filters.")

# ----------------------------------------------
# CLOSING the QUERY
# ----------------------------------------------
st.subheader("Close an Open Query")

# Filtering only open queries for closure
open_queries = [q for q in queries if q["state"] == "Open"]

if open_queries:
    selected_query = st.selectbox(
        "Select Query to Close",
        open_queries,
        format_func=lambda x: f"#{x['query_id']} - {x['query_title']}"
    )

    if st.button("Close Selected Query"):
        close_query(selected_query["query_id"])
        st.success(f"Query #{selected_query['query_id']} has been closed.")
        st.rerun()
else:
    st.info("No open queries available to close.")

    
st.subheader("📊 Query Analytics Dashboards")

# Fetch all data
all_queries = fetch_queries()

if all_queries:

    df = pd.DataFrame(all_queries)

    # Convert date fields
    df["created_on"] = pd.to_datetime(df["created_on"])
    df["closed_on"] = pd.to_datetime(df["closed_on"], errors="coerce")

    # ======================================================
    # 1️⃣ QUERIES CREATED PER DAY (LINE CHART)
    # ======================================================
    created_per_day = (
        df.groupby(df["created_on"].dt.date)
        .size()
        .reset_index(name="count")
        .rename(columns={"created_on": "date"})
    )

    st.markdown("### 📅 Queries Created Per Day")
    chart_created = (
        alt.Chart(created_per_day)
        .mark_line(point=True, color="#1D1992")
        .encode(
            x="date:T",
            y="count:Q",
            tooltip=["date", "count"]
        )
        .properties(height=300)
    )
    st.altair_chart(chart_created, use_container_width=True)

    # ======================================================
    # 2️⃣ QUERIES CLOSED PER DAY (AREA CHART)
    # ======================================================
    closed_df = df.dropna(subset=["closed_on"])

    if not closed_df.empty:
        closed_per_day = (
            closed_df.groupby(closed_df["closed_on"].dt.date)
            .size()
            .reset_index(name="count")
            .rename(columns={"closed_on": "date"})
        )

        st.markdown("### ✔ Queries Closed Per Day")
        chart_closed = (
            alt.Chart(closed_per_day)
            .mark_area(color="#158315", opacity=0.5)
            .encode(
                x="date:T",
                y="count:Q",
                tooltip=["date", "count"]
            )
            .properties(height=300)
        )
        st.altair_chart(chart_closed, use_container_width=True)
    else:
        st.info("No queries have been closed yet.")

        st.markdown("### 🥧 Open vs Closed Queries (Pie Chart)")

# Count open vs closed
status_counts = df["state"].value_counts().reset_index()
status_counts.columns = ["state", "count"]

# Pie Chart
pie_chart = (
    alt.Chart(status_counts)
    .mark_arc()
    .encode(
        theta="count:Q",
        color="state:N",
        tooltip=["state", "count"]
    )
)

st.altair_chart(pie_chart, use_container_width=True)