# scripts/generate_mock_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_live_dataset(target_path=None):
    """Generates a dynamic 90-day historical customer log dataset ending today."""
    if target_path is None:
        target_path = os.path.join("data", "mock_historical.csv")
        
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    np.random.seed(42)  # Controlled variance
    # Generate dates counting backward from today
    end_date = datetime.now()
    dates = [end_date - timedelta(days=int(i)) for i in np.linspace(0, 90, 450)]

    product_areas = [
        "Authentication & Login", 
        "Analytics Dashboard", 
        "Billing & Invoicing", 
        "Integrations & APIs", 
        "Core UI & Navigation"
    ]
    sources = ["Zendesk Ticket", "Intercom Chat", "Gong Call"]

    data = []
    for date in dates:
        area = np.random.choice(product_areas)
        source = np.random.choice(sources)
        
        # Default baseline sentiment
        sentiment = np.random.uniform(-0.2, 0.6)
        summary = f"Standard follow-up investigation regarding {area.lower()} stability."
        quote = "The performance matrix operations seem stable under normal parameters."
        
        # --- ENGINEERED ANOMALY WINDOW ---
        # If the log falls within the last 30 days and belongs to 'Integrations & APIs',
        # simulate a severe drop in sentiment to trigger our dashboard's alert system.
        if (end_date - date).days <= 30 and area == "Integrations & APIs":
            sentiment = np.random.uniform(-0.9, -0.3)
            summary = "Critical payload drops detected inside webhook synchronization layer."
            quote = "The webhooks syncing to HubSpot keep throwing silent 500 errors."

        data.append({
            "date": date.strftime("%Y-%m-%d %H:%M:%S"),
            "source_type": source,
            "product_area": area,
            "sentiment_score": round(sentiment, 2),
            "summary": summary,
            "verbatim_quote": quote
        })

    df = pd.DataFrame(data)
    df.to_csv(target_path, index=False)
    return len(df)

if __name__ == "__main__":
    # Allows backward compatibility for terminal executions
    count = generate_live_dataset()
    print(f"Generated {count} rows successfully.")