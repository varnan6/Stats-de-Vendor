import re

from app.tools.risk import get_top_risky_vendors
from app.tools.anomaly import get_anomalies
from app.tools.trend import vendor_trend
from app.tools.similarity import similar_vendors

def route_query(query):

    query = query.lower()

    match query:
        
        case "risk":
            return get_top_risky_vendors()
        
        case "anomaly":
            return get_anomalies()
        
        case "trend":
            vendor_id = extract_vendor_id(query)
            return vendor_trend(vendor_id)
        
        case "similar":
            vendor_id = extract_vendor_id(query)
            return similar_vendors(vendor_id)

        case _:
            return "Couldn't understand the query. Please recheck."

def extract_vendor_id(query):
    match = re.search(r"\d+", query)
    return int(match.group()) if match else None