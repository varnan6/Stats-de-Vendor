from app.tools.risk import get_top_risky_vendors
from app.tools.anomaly import get_anomalies
from app.tools.trend import vendor_trend
from app.tools.similarity import similar_vendors

def route_query(query):

    query = query.upper()

    match query:
        
        case "RISK":
            return get_top_risky_vendors()
        
        case "ANOMALY":
            return get_anomalies()
        
        case "TREND":
            vendor_id = extract_vendor_id(query)
            return vendor_trend(vendor_id)
        
        case "SIMILAR":
            vendor_id = extract_vendor_id(query)
            return similar_vendors(vendor_id)

        case _:
            return "Couldn't understand the query. Please recheck."
        

def extract_vendor_id(query):
    return query.split()[-1]