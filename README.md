# Stats-de-Vendor

Stats-de-Vendor is a FastAPI-based analytics service that helps monitor vendors' performance, detect anomalies in spend and delay, and track monthly trends. It integrates a PostgreSQL database, pandas analytics, and optionally an LLM layer to query insights in natural language.

## Features

- **Anomaly Detection:** Identify vendors with unusually high spend or delays using z-scores.
- **Vendor Trend Analysis:** Track spend and delay trends over time for each vendor.
- **LLM Integration:** Query insights in natural language (`/ask` endpoint).
- **FastAPI Backend:** Lightweight and fast API server with automatic docs.
- **PostgreSQL Support:** Works with your vendor transactions stored in PostgreSQL.

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **Data Analysis:** pandas, numpy, scipy
- **ORM/DB Connection:** psycopg2 (direct)
- **Deployment:** Uvicorn

## Project Structure
```
Stats-de-Vendor/
├── app/
│   ├── agent/
│   │   ├── llm_agent.py       # Handles LLM routing
│   │   └── router.py          # FastAPI /ask endpoint
│   ├── db/
│   │   └── connection.py      # PostgreSQL connection
│   └── tools/
│       ├── anomaly.py         # Detects anomalous vendors
│       └── trend.py           # Fetches monthly trends
├── main.py                    # FastAPI app entrypoint
├── README.md
└── requirements.txt
```

## ⚡ Installation

1. Clone the repo:
```bash
git clone https://github.com/yourusername/Stats-de-Vendor.git
cd Stats-de-Vendor
```

2. Create a virtual environment:
```bash
python3 -m venv stats-venv
source stats-venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure PostgreSQL connection in `app/db/connection.py`.

## Running the Server
```bash
uvicorn main:app --reload
```

- Open Swagger UI: http://127.0.0.1:8000/docs
- Open OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## API Endpoints

### `/ask?query=...`

**Description:** Main endpoint to query vendor analytics.

**Example queries:**
- `show anomalous vendors` → Returns vendors with high spend or delays
- `trend of vendor <vendor_id>` → Returns monthly spend/delay trends

**Response Format (JSON):**
```json
[
  {
    "month": "2025-01",
    "spend": 5200,
    "delay": null
  }
]
```

## Testing

Test anomaly detection:
```bash
curl "http://127.0.0.1:8000/ask?query=show%20anomalous%20vendors"
```

Test vendor trend:
```bash
curl "http://127.0.0.1:8000/ask?query=trend%20of%20vendor%208b2a95e5-3a4a-4250-ba28-e37d6257175c"
```

**Expected Output:** JSON with monthly spend and delay; NaN values replaced with `null`.

## Notes

- Make sure your database contains the required tables (`vendor_features`, `transactions`).
- `NaN` values in trends are replaced with `null` to comply with JSON.
- SQL queries use parameterized statements to prevent syntax errors and SQL injection.

## Future Improvements

- Add an LLM explanation layer for human-readable insights.
- Add authentication for secure API access.
- Add real-time analytics dashboards using Plotly or Dash.
- Add unit tests for each tool.

## License
MIT License © 2026 Varnan Rathod
