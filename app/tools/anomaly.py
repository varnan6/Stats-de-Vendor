import pandas as pd
from scipy.stats import zscore

from app.db.connection import get_connection

def get_anomalies():

    conn = get_connection()

    query = """
        SELECT vendor_id, avg_spend, avg_delay
        FROM vendor_features
    """

    df = pd.read_sql(query, conn)
    conn.close()

    df["z_spend"] = zscore(df["avg_spend"])
    df["z_delay"] = zscore(df["avg_delay"])

    df["is_anomaly"] = (
        df["z_spend"].abs() > 2 | df["z_delay"].abs() > 2
    )

    return df[df["is_anomaly"]]