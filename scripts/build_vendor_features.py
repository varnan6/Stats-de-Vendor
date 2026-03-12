import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname"  : os.getenv("DB_NAME"),
    "user"    : os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host"    : os.getenv("DB_HOST"),
    "port"    : os.getenv("DB_PORT")
}

def main():
    
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("=== Computing vendor features ===")

    cur.execute("""
        SELECT
            vendor_id,
            AVG(amount),
            STDDEV(amount),
            AVG(delivery_delays_days),
            COUNT(*),
            SUM(amount),
            MIN(date),
            MAX(date)
        FROM purchase_orders
        GROUP BY vendor_id;
    """)

    rows = cur.fetchall()

    print(f"Found {len(rows)} vendors")

    for r in rows:

        cur.execute("""
            INSERT INTO vendor_features(
                vendor_id,
                avg_spend,
                spend_std,
                avg_delay,
                total_orders,
                total_spend,
                first_order,
                last_order)
                
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    
            ON CONFLICT (vendor_id)
            DO UPDATE SET
                avg_spend = EXCLUDED.avg_spend,
                spend_std = EXCLUDED.spend_std,
                avg_delay = EXCLUDED.avg_delay,
                delay_std = EXCLUDED.delay_std,
                total_orders = EXCLUDED.total_orders,
                total_spend = EXCLUDED.total_spend,
                first_order = EXCLUDED.first_order,
                last_order = EXCLUDED.last_order,
                last_updated = NOW();
        """, r)

    conn.commit()

    cur.close()
    conn.close()

    print("Vendor features built successfully.")

if __name__ == "__main__":
    main()