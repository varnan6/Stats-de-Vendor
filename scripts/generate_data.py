import psycopg2
import random
import math
from datetime import datetime, timedelta
import uuid

# Configuration
DB_CONFIG = {
    "dbname"   : "vendor_db",
    "user"     : "postgres",
    "password" : "vendor_db",
    "host"     : "localhost",
    "port"     : "5432"
}

START_YEAR = 2023
END_YEAR = 2024

# Vendor behavior profiles
def generate_vendor_profiles(vendor_ids):
    profiles = {}

    for vid in vendor_ids:
        profiles[vid] = {
            "base"              : random.randint(80000, 250000),
            "seasonal_amplitude": random.randint(10000,40000),
            "volatility"        : random.uniform(0.05, 0.15),
            "delay_mean"        : random.randint(2, 10),
            "delay_std"         : random.uniform(1,4),
            "anomaly_month"     : random.randint(0,23)
        }
    
    return profiles

# Generate monthly spend
def compute_monthly_spend(profile, month_index):
    base = profile["base"]
    seasonal = profile["seasonal_amplitude"] * math.sin(2*math.pi*month_index/12)
    noise = random.gauss(0, profile["volatility"]*base)

    spend = base + seasonal + noise

    # Inject anomaly
    if month_index == profile["anomaly_month"]:
        spend *= random.uniform(2,3)
    
    return max(spend, 10000)

def main():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Fetch vendor IDs
    cur.execute("SELECT id FROM vendors;")
    vendor_ids = [row[0] for row in cur.fetchall()]

    profiles = generate_vendor_profiles(vendor_ids)

    month_index = 0

    for year in range(START_YEAR, END_YEAR + 1):
        for month in range(1,13):
            first_day = datetime(year, month, 1)

            for vid in vendor_ids:
                profile = profiles[vid]
                monthly_spend = compute_monthly_spend(profile, month_index)

                # Split into 2-4 orders
                order_count = random.randint(2,4)
                splits = [random.random() for _ in range(order_count)]
                total = sum(splits)
                splits = [s / total for s in splits]

                for split in splits:
                    amount = monthly_spend * split
                    order_date = first_day + timedelta(days = random.randomint(0,27))
                    delay = random.gauss(profile["delay_mean"], profile["delay_std"])
                    delay = max(int(delay), 0)
                    delivery_date = order_date + timedelta(days = delay)

                    cur.execute(
                        """
                        INSERT INTO purchase_orders
                        (id, vendor_id, order_amount, order_date, delivery_date)
                        VALUES (%s, %s, %s, %s, %s);
                        """,
                        (
                            str(uuid.uuid4()),
                            vid,
                            round(amount, 2),
                            order_date.date(),
                            delivery_date.date()
                        )
                    )
            
            month_index += 1
        
        conn.commit()
        cur.close()
        conn.close()

        print("Synthetic purchase orders generated successfully.")


if __name__ == "__main__":
    main()
        