import os
import psycopg2
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

def create_tables(cursor):

    cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    
    # Vendors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendors (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            rating FLOAT CHECK (rating BETWEEN 0 AND 5),
            on_time_delivery_rate FLOAT CHECK (on_time_delivery_rate BETWEEN 0 AND 1)
        );
    """)

    # Purchase Orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            vendor_id UUID REFERENCES vendors(id) ON DELETE CASCADE,
            date DATE NOT NULL,
            amount NUMERIC NOT NULL,
            delivery_delays_days INT,
            category TEXT
        );
    """)

    # Vendor embeddings' table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vector_embeddings(
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            vendor_id UUID REFERENCES vendors(id) ON DELETE CASCADE,
            content TEXT NOT NULL,
            embedding VECTOR(768)
        );
    """)

def create_indexes(cursor):

    # Index for faster vendor-based lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_purchase_orders_vendor_id ON purchase_orders(vendor_id);
    """)

    # Index for date-based queries (trend analysis)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_purchase_orders_date ON purchase_orders(date);
    """)

    # Vector index for semantic search
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_vendor_embeddings_vector
        ON vector_embeddings
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 10);
    """)

def main():
    
    conn   = None
    cursor = None

    try:
        print("=== Connecting to db ===")
        conn = get_connection()
        cursor = conn.cursor()

        print("=== Creating tables ===")
        create_tables(cursor)

        print("=== Creating indexes ===")
        create_indexes(cursor)

        conn.commit()
        print("=== Database Initialization completed successfully ===")
    
    except Exception as e:
        
        if conn:
            conn.rollback()
        print("=== Error during DB initialization ===\n Error: ")
        print(e)
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("=== Connection closed ===")

if __name__ == "__main__":
    main()