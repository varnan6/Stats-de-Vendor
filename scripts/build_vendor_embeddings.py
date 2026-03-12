import os
import psycopg2
import uuid
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname"   : os.getenv("DB_NAME"),
    "user"     : os.getenv("DB_USER"),
    "password" : os.getenv("DB_PASSWORD"),
    "host"     : os.getenv("DB_HOST"),
    "port"     : os.getenv("DB_PORT")
}

def main():

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("=== Building vendor embeddings ===")

    cur.execute("""
        SELECT
            vendor_id,
            avg_spend,
            spend_std,
            avg_delay,
            delay_std,
            total_orders
        FROM vendor_features;
    """)

    rows = cur.fetchall()

    for r in rows:

        vendor_id, avg_spend, spend_std, avg_delay, delay_std, total_orders = r

        vector = [
            float(avg_spend or 0),
            float(spend_std or 0),
            float(avg_delay or 0),
            float(delay_std or 0),
            float(total_orders or 0)
        ]

        cur.execute("""
        INSERT INTO vector_embeddings (id, vendor_id, content, embedding)
        VALUES (%s, %s, %s, %s)
        """,
        (
            str(uuid.uuid4()),
            vendor_id,
            "vendor_behavior_embedding",
            vector
        ))

    
    conn.commit()
    cur.close()
    conn.close()

    print("=== Vector embeddings generated successfully ===")


if __name__ == "__main__":
    main()