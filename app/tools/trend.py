import pandas as pd
import numpy as np
from app.db.connection import get_connection

def vendor_trend(vendor_id):

    conn = get_connection()

    query = """
        SELECT
            DATE_TRUNC('month', date) AS month,
            AVG(amount) AS avg_spend,
            AVG(delivery_delays_days) AS avg_delay
        FROM purchase_orders
        WHERE vendor_id = %s
        GROUP BY month
        ORDER BY month;
    """

    df = pd.read_sql(query, conn, params=(vendor_id,))
    conn.close()

    df["spend_change"] = df["avg_spend"].pct_change()
    df["delay_change"] = df["avg_delay"].pct_change()

    return df.replace({np.nan: None}).to_dict(orient="records")