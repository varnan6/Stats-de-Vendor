import requests
import json

from app.tools.risk import get_top_risky_vendors
from app.tools.anomaly import get_anomalies
from app.tools.trend import vendor_trend
from app.tools.similarity import similar_vendors

OLLAMA_URL = "http://localhost:11434/api/generate"

TOOLS = {
    "risk": get_top_risky_vendors,
    "anomaly": get_anomalies,
    "trend": vendor_trend,
    "similar": similar_vendors
}

SYSTEM_PROMPT = """
    You are an AI agent for vendor analytics.

    Available tools:
    - risk → top risky vendors
    - anomaly → anomalous vendors
    - trend → vendor trend (needs vendor_id)
    - similar → similar vendors (needs vendor_id)

    Return ONLY JSON:
    {
      "tool": "risk/anomaly/trend/similar",
      "vendor_id": optional integer
    }
"""

def call_ollama(prompt):

    response = requests.post(
        OLLAMA_URL,
        json = {
            "model": "llama3",
            "prompt": prompt,
            "stream" : False
        }
    )

    return response.json()["response"]

def decide_tool(query: str):
    
    prompt = f"{SYSTEM_PROMPT}\n User Query: {query}"

    output = call_ollama(prompt)

    try:
        return json.loads(output)
    except:
        return {"tool": "risk"}
    


def route_query(query: str):

    decision = decide_tool(query)

    tool = decision.get("tool")
    vendor_id = decision.get("vendor_id")

    if tool not in TOOLS:
        return {"error": "Invalid tool selected"}
    
    if tool in ["trend", "similar"]:
        if vendor_id is None:
            return {"error" : "vendor id required"}
        return TOOLS[tool](vendor_id)
    
    return TOOLS[tool]()