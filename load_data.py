import os
import sqlite3
import pandas as pd


def initialize_database():
  """Initializes the SQLite database and creates normalized tables."""
  conn = sqlite3.connect("tennis_analytics.db")
  cursor = conn.cursor()

  # 1. Categories Table
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id VARCHAR(50) PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL
    );
    """)

  # 2. Competitions Table
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS competitions (
        competition_id VARCHAR(50) PRIMARY KEY,
        competition_name VARCHAR(100) NOT NULL,
        parent_id VARCHAR(50),
        type VARCHAR(20) NOT NULL,
        gender VARCHAR(10) NOT NULL,
        category_id VARCHAR(50),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    """)

  # 3. Complexes Table
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS complexes (
        complex_id VARCHAR(50) PRIMARY KEY,
        complex_name VARCHAR(100) NOT NULL
    );
    """)

  # 4. Venues Table
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS venues (
        venue_id VARCHAR(50) PRIMARY KEY,
        venue_name VARCHAR(100) NOT NULL,
        city_name VARCHAR(100) NOT NULL,
        country_name VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        timezone VARCHAR(100) NOT NULL,
        complex_id VARCHAR(50),
        FOREIGN KEY (complex_id) REFERENCES complexes(complex_id)
    );
    """)

  # 5. Competitors Table
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS competitors (
        competitor_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        country VARCHAR(100) NOT NULL,
        country_code CHAR(3) NOT NULL,
        abbreviation VARCHAR(10) NOT NULL
    );
    """)

  # 6. Competitor Rankings Table
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS competitor_rankings (
        rank_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rank INT NOT NULL,
        movement INT NOT NULL,
        points INT NOT NULL,
        competitions_played INT NOT NULL,
        competitor_id VARCHAR(50),
        FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
    );
    """)

  conn.commit()
  conn.close()
  print("Database schema created successfully.")


def load_csv_to_db():
  """Reads the 6 CSV files and loads them into the database."""
  conn = sqlite3.connect("tennis_analytics.db")

  csv_mapping = {
      "categories.csv": "categories",
      "competitions.csv": "competitions",
      "complexes.csv": "complexes",
      "venues.csv": "venues",
      "competitors.csv": "competitors",
      "competitor_rankings.csv": "competitor_rankings",
  }

  for file_name, table_name in csv_mapping.items():
    if os.path.exists(file_name):
      try:
        df = pd.read_csv(file_name)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(
            f"Successfully loaded '{file_name}' into table '{table_name}'"
            f" ({len(df)} rows)."
        )
      except Exception as e:
        print(f"Error loading {file_name}: {e}")
    else:
      print(f"Warning: '{file_name}' not found in the working directory.")

  conn.close()


if __name__ == "__main__":
  initialize_database()
  load_csv_to_db()