import sqlite3
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Tennis Data & Game Analytics Explorer",
    page_icon="🎾",
    layout="wide",
)

# Database Connection


@st.cache_resource
def get_connection():
  return sqlite3.connect("tennis_analytics.db", check_same_thread=False)


conn = get_connection()

# Sidebar Navigation
st.sidebar.title("🎾 Navigation & Filters")
app_mode = st.sidebar.selectbox(
    "Choose View",
    [
        "Home Dashboard",
        "Competitions Explorer",
        "Venues & Complexes",
        "Rankings Leaderboard",
        "Advanced SQL Playground",
    ],
)

# 1. Home Dashboard
if app_mode == "Home Dashboard":
  st.title("🎾 Game Analytics: Sportradar Tennis Dashboard")
  st.markdown(
      "Welcome to the interactive tennis data analytics portal. Use the sidebar"
      " to navigate through structured competitions, venue mappings, ranking"
      " leaderboards, and the custom SQL analytics playground."
  )

  try:
    total_competitors = pd.read_sql(
        "SELECT COUNT(*) FROM competitors", conn
    ).iloc[0, 0]
    total_countries = pd.read_sql(
        "SELECT COUNT(DISTINCT country) FROM competitors", conn
    ).iloc[0, 0]
    max_points = pd.read_sql(
        "SELECT MAX(points) FROM competitor_rankings", conn
    ).iloc[0, 0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", total_competitors)
    col2.metric("Countries Represented", total_countries)
    col3.metric("Highest Points Scored", max_points if max_points else 0)
  except Exception as e:
    st.info(f"Summary metrics status: {e}")

# 2. Competitions Explorer
elif app_mode == "Competitions Explorer":
  st.header("🏆 Competitions & Categories Hierarchy")
  try:
    df_comp = pd.read_sql(
        """
            SELECT c.competition_name, c.type, c.gender, cat.category_name 
            FROM competitions c 
            LEFT JOIN categories cat ON c.category_id = cat.category_id
        """,
        conn,
    )
    gender_filter = st.selectbox(
        "Filter by Gender", ["All"] + list(df_comp["gender"].dropna().unique())
    )
    if gender_filter != "All":
      df_comp = df_comp[df_comp["gender"] == gender_filter]
    st.dataframe(df_comp, use_container_width=True)
  except Exception as e:
    st.warning(f"Database query error: {e}")

# 3. Venues & Complexes
elif app_mode == "Venues & Complexes":
  st.header("🏟️ Complexes and Venues Analysis")
  try:
    df_venues = pd.read_sql(
        """
            SELECT v.venue_name, v.city_name, v.country_name, v.timezone, c.complex_name 
            FROM venues v 
            LEFT JOIN complexes c ON v.complex_id = c.complex_id
        """,
        conn,
    )
    country_filter = st.selectbox(
        "Filter by Country",
        ["All"] + list(df_venues["country_name"].dropna().unique()),
    )
    if country_filter != "All":
      df_venues = df_venues[df_venues["country_name"] == country_filter]
    st.dataframe(df_venues, use_container_width=True)
  except Exception as e:
    st.warning(f"Database query error: {e}")

# 4. Rankings Leaderboard
elif app_mode == "Rankings Leaderboard":
  st.header("📊 Competitor Rankings & Points")
  try:
    df_ranks = pd.read_sql(
        """
            SELECT comp.name, comp.country, r.rank, r.movement, r.points, r.competitions_played 
            FROM competitor_rankings r 
            JOIN competitors comp ON r.competitor_id = comp.competitor_id 
            ORDER BY r.rank ASC
        """,
        conn,
    )
    top_n = st.slider("Show Top N Competitors", 5, 50, 10)
    st.dataframe(df_ranks.head(top_n), use_container_width=True)
  except Exception as e:
    st.warning(f"Database query error: {e}")

# 5. Advanced SQL Playground
elif app_mode == "Advanced SQL Playground":
  st.header("⚡ Advanced SQL Analytics Playground")
  st.markdown(
      "Write and execute custom SQL queries directly against your tennis"
      " relational database."
  )

  default_query = (
      "SELECT comp.name, comp.country, r.rank, r.points \nFROM competitors comp"
      " \nJOIN competitor_rankings r ON comp.competitor_id = r.competitor_id"
      " \nORDER BY r.points DESC LIMIT 10;"
  )

  user_query = st.text_area(
      "Enter SQL Query:", value=default_query, height=150
  )

  if st.button("Execute Query"):
    try:
      result_df = pd.read_sql(user_query, conn)
      st.success(
          f"Query executed successfully! Returned {len(result_df)} rows."
      )
      st.dataframe(result_df, use_container_width=True)
    except Exception as e:
      st.error(f"SQL Execution Error: {e}")