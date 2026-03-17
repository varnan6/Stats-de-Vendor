import pandas as pd

from app.db.connection import get_connection

def vendor_trend(vendor_id):

    conn = get_connection()

    query = f"""
        SELECT
            DATE_TRUNC('month', date) AS month,
            AVG(amount) AS avg_spend,
            AVG(delivery_delays_days) AS avg_delay
        FROM purchase_orders
        WHERE vendor_id = '{vendor_id}
        GROUP BY month
        ORDER BY month;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    df["spend_change"] = df["avg_spend"].pct_change()
    df["delay_change"] = df["avg_delay"].pct_change()

    return df