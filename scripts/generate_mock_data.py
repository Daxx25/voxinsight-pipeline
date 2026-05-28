# scripts/generate_mock_data.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_historical_data(num_records=500, days=90):
    """Generates realistic mock VoC data with built-in trends/anomalies for the dashboard."""
    
    # Define our constants based on our schemas
    product_areas = [
        "Authentication & Login", "Analytics Dashboard", 
        "Billing & Invoicing", "Integrations & APIs", "Core UI & Navigation"
    ]
    source_types = ["Gong Call", "Zendesk Ticket", "Intercom Chat"]
    
    # Base setup
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = [start_date + timedelta(days=random.uniform(0, days)) for _ in range(num_records)]
    dates.sort() # Sort chronologically
    
    data = []
    
    for dt in dates:
        # 1. Base Probabilities
        area = random.choices(
            product_areas, 
            weights=[10, 30, 20, 25, 15], # Dashboard and Integrations usually get the most feedback
            k=1
        )[0]
        source = random.choice(source_types)
        
        # 2. Engineer an Anomaly (A sudden bug in Authentication 30 days ago)
        days_ago = (end_date - dt).days
        is_anomaly_period = 25 <= days_ago <= 35
        
        if is_anomaly_period and random.random() < 0.6: 
            # Force 60% of tickets during this 10-day window to be severe Auth bugs
            area = "Authentication & Login"
            sentiment = round(random.uniform(-1.0, -0.6), 2) # Highly negative
            summary = "Cannot log in via SSO / SAML integration failing."
            pain_point = "SSO loop redirects back to login screen."
            quote = "I've been trying to log in for 3 hours and the Okta SSO just keeps refreshing."
            
        else:
            # Normal distribution of sentiment based on the area
            if area == "Billing & Invoicing":
                sentiment = round(random.uniform(-0.8, 0.2), 2) # Usually negative
                summary = "Confusion around prorated billing."
                pain_point = "Cannot find the invoice for the added seats."
                quote = "Where do I download the PDF for last month's true-up?"
            elif area == "Analytics Dashboard":
                sentiment = round(random.uniform(-0.3, 0.8), 2) # Mixed to positive
                summary = "Wants more export options for charts."
                pain_point = "CSV export is missing the new cohort columns."
                quote = "The charts look great, but I really need to export this to a CSV for my leadership team."
            else:
                sentiment = round(random.uniform(-0.5, 0.7), 2)
                summary = f"General feedback regarding {area}."
                pain_point = "UX is slightly confusing."
                quote = f"It took me a while to figure out how the {area} works."

        data.append({
            "date": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "source_type": source,
            "product_area": area,
            "sentiment_score": sentiment,
            "summary": summary,
            "pain_point": pain_point,
            "verbatim_quote": quote
        })

    df = pd.DataFrame(data)
    
    # Save safely using pathlib/os for cross-platform compatibility
    os.makedirs('data', exist_ok=True)
    file_path = os.path.join('data', 'mock_historical.csv')
    df.to_csv(file_path, index=False)
    
    print(f"✅ Successfully generated {num_records} records!")
    print(f"✅ Engineered a negative sentiment anomaly in 'Authentication & Login'.")
    print(f"✅ Saved to: {file_path}")

if __name__ == "__main__":
    generate_historical_data()