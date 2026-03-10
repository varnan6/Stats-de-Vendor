import os
import psycopg2
import uuid
import random
from dotenv import load_dotenv

def get_connection():
    load_dotenv()

    return psycopg2.connect(
        dbname   = os.getenv("DB_NAME"),
        user     = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        host     = os.getenv("DB_HOST"),
        port     = os.getenv("DB_PORT")
    )

def generate_vendor_name():
    
    prefixes = [
        "Global", "Prime", "United", "Dynamic", "Advanced",
        "NextGen", "Pioneer", "Summit", "Atlas", "Vertex"
    ]

    sectors = [
        "Industrial", "Logistics", "Technologies",
        "Materials", "Components", "Supplies",
        "Solutions", "Systems", "Manufacturing"
    ]

    suffixes = ["Corp", "Ltd", "Group", "Co", "Enterprises"]

    return f"{random.choice(prefixes)} {random.choice(sectors)} {random.choice(suffixes)}"

def seed_vendors(cursor, n_vendors = 20):

    categories = [
        "manufacturing",
        "logistics",
        "electronics",
        "technology",
        "chemicals",
        "industrial",
        "energy",
        "office_supplies"
    ]

    vendors_inserted = 0

    for _ in range(n_vendors):

        vid = str(uuid.uuid4())
        name = generate_vendor_name()
        category = random.choice(categories)
        rating = round(random.uniform(3.0,5.0),2)
        on_time_delivery_rate = round(random.uniform(0.7, 0.99), 2)

        cursor.execute((
            """INSERT INTO vendors (id, name, category, rating, on_time_delivery_rate)
            VALUES(%s, %s, %s, %s, %s) ON CONFLICT(name) DO NOTHING;"""
        ), (vid, name, category, rating, on_time_delivery_rate))

        vendors_inserted += 1

    print(f"Inserted {vendors_inserted} synthetic vendors")


def main():

    conn = None
    cursor = None

    try:
        print("=== Connecting to DB ===")
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM vendors")
        vendor_count = cursor.fetchone()[0]

        print("Existing vendors: ", vendor_count)

        if vendor_count > 0:
            print("Vendors already exist. Skipping seeding.")
            return
    
        print("Generating synthetic vendors...")
        seed_vendors(cursor)

        conn.commit()

        print("Vendor seeding completed.")

    except Exception as e:

        if conn:
            conn.rollback()

        print(f"!!! Error during vendor seeding: {e} !!!")

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

        print("=== Connection closed. ===")

if __name__ == "__main__":
    main()