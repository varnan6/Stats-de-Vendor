import pandas as pd
from app.db.connection import get_connection

def get_top_risky_vendors(limit = 5):

    conn = get_connection()

    query = f"""
    SELECT *
    FROM vendor_risk
    ORDER BY risk_score DESC
    LIMIT {limit};
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df