import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

from app.db.connection import get_connection

load_dotenv()

DB_CONFIG = {
    "dbname"   : os.getenv("DB_NAME"),
    "user"     : os.getenv("DB_USER"),
    "password" : os.getenv("DB_PASSWORD"),
    "host"     : os.getenv("DB_HOST"),
    "port"     : os.getenv("DB_PORT")
}

def normalize(series):
    """
        Using min-max scaling
    """
    return (series - series.min())/(series.max() - series.min())


def fetch_features():

    conn = psycopg2.connect(**DB_CONFIG)

    query = """
    SELECT
        vendor_id,
        avg_spend,
        spend_std,
        avg_delay,
        delay_std,
        total_orders
    FROM vendor_features
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def compute_risk(df):

    df["norm_volatility"] = normalize(df["spend_std"])
    df["norm_delay"] = normalize(df["avg_delay"])

    df["risk_score"] = (
        0.4*df["norm_volatility"] + 0.4*df["norm_delay"]
    )

    df["risk_score"] = (df["risk_score"]*100).round(2)

    return df

def store_risk(df):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
        INSERT INTO vendor_risk (vendor_id, risk_score)
        VALUES (%s, %s)
        ON CONFLICT (vendor_id)
        DO UPDATE SET
            risk_score = EXCLUDED.risk_score,
            last_updated = CURRENT_TIMESTAMP;
    """, (row["vendor_id"], row["risk_score"]))
    
    conn.commit()
    conn.close()

def main():

    print("=== Computing vendor risk scores ===")

    df = fetch_features()
    df = compute_risk(df)

    df = df.sort_values("risk_score", ascending=False)

    store_risk(df)

    print("\nTop risky vendors: \n")

    print(df[[
        "vendor_id",
        "avg_spend",
        "avg_delay",
        "risk_score"
    ]].head(10))


if __name__ == "__main__":
    main()