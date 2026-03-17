import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from sklearn.ensemble import IsolationForest
from scipy.stats import zscore

from app.db.connection import get_connection


load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def fetch_vendor_features():

    conn = psycopg2.connect(**DB_CONFIG)

    query = """
        SELECT
            vendor_id,
            avg_spend,
            spend_std,
            avg_delay,
            delay_std,
            total_orders
        FROM vendor_features;
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df

def detect_anomalies(df):

    features = df[[
        "avg_spend",
        "spend_std",
        "avg_delay",
        "delay_std",
        "total_orders"
    ]]

    # Z-score
    df["zscore_spend"] = zscore(df["avg_spend"])
    df["zscore_delay"] = zscore(df["avg_delay"])

    # Isolation Forest
    model = IsolationForest(
        contamination=0.15,
        random_state=42
    )
    
    model.fit(features)

    df["anomaly_score"] = model.decision_function(features)
    df["is_anomaly"] = df["anomaly_score"] == -1

    return df

def store_anomalies(df):

    conn = get_connection()
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
        INSERT INTO vendor_anomalies (vendor_id, is_anomaly, anomaly_score)
        VALUES (%s, %s, %s)
        ON CONFLICT (vendor_id)
        DO UPDATE SET
            is_anomaly = EXCLUDED.is_anomaly,
            anomaly_score = EXCLUDED.anomaly_score,
            last_updated = CURRENT_TIMESTAMP;
        """, (
            row["vendor_id"],
            row["is_anomaly"],
            row["anomaly_score"]
        ))

    conn.commit()
    conn.close()

def main():

    print("=== Runnign vendor anomaly detection ===")
    
    df = fetch_vendor_features()
    df = detect_anomalies(df)

    anomalies = df[df["is_anomaly"] == True]

    store_anomalies(df)

    print("\nDetected anomalous vendors: ")
    print(anomalies[[
        "vendor_id",
        "avg_spend",
        "avg_delay",
        "zscore_spend",
        "zscore_delay"
    ]])

    print(f"\nTotal anomalies detected: {len(anomalies)}")

if __name__ == "__main__":
    main()