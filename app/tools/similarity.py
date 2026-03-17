from app.db.connection import get_connection

def similar_vendors(vendor_id, limit = 5):
    
    conn = get_connection()
    cur = conn.cursor()

    query = f"""
        SELECT v2.name
        FROM vector_embeddings e1
        JOIN vector_embeddings e2
            ON e1.vendor_id != e2.vendor_id
        JOIN vendors v2
            ON v2.id = e2.vendor_id
        WHERE e1.vendor_id = '{vendor_id}'
        ORDER BY e1.embedding <-> e2.embedding
        LIMIT {limit};
    """

    cur.execute(query)
    results = cur.fetchall()

    conn.close()

    return [r[0] for r in results]