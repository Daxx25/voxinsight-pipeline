# core/pipeline.py
import re
import json
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
from core.guards import verify_verbatim_quote

SYSTEM_PROMPT = """
You are a Principal Product Manager. Analyze the provided customer text and return a strict JSON object.
Do not include any introductory text or markdown formatting blocks (like ```json). Return raw JSON only.

Expected JSON Structure:
{
    "product_area": "Choose exactly one: Authentication & Login, Analytics Dashboard, Billing & Invoicing, Integrations & APIs, or Core UI & Navigation",
    "sentiment_score": -1.0 to 1.0 (float),
    "summary": "1-sentence summary of the core issue",
    "pain_points": ["Point 1", "Point 2"],
    "feature_requests": ["Request 1"],
    "verbatim_quote": "The EXACT string snippet copied directly from the text provided."
}
"""

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=5))
def _execute_groq_call(client: Groq, text: str) -> dict:
    """Calls Groq using the ultra-fast llama-3.3-70b-versatile model with forced JSON mode."""
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        response_format={"type": "json_object"},
        temperature=0.0
    )
    return json.loads(completion.choices[0].message.content)

def run_voc_pipeline(raw_text: str, source_type: str, api_key: str) -> dict:
    if not api_key:
        return {"status": "error", "message": "Groq API Key missing. Provide it in the sidebar."}
        
    cleaned_text = re.sub(r'(\[Music\]|Gong Transcript:)', '', raw_text)

    try:
        client = Groq(api_key=api_key)
        parsed_json = _execute_groq_call(client, f"Source: {source_type}\nText:\n{cleaned_text}")
        
        # Guardrail execution
        guard_result = verify_verbatim_quote(cleaned_text, parsed_json.get("verbatim_quote", ""))
        
        output_payload = {
            "product_area": parsed_json.get("product_area", "Core UI & Navigation"),
            "sentiment_score": float(parsed_json.get("sentiment_score", 0.0)),
            "summary": parsed_json.get("summary", "No summary generated."),
            "pain_points": parsed_json.get("pain_points", []),
            "feature_requests": parsed_json.get("feature_requests", []),
            "verbatim_quote": guard_result["matched_quote"],
            "quote_verification_status": guard_result["type"]
        }
        
        if not guard_result["verified"]:
            return {
                "status": "warning",
                "message": "Insight captured, but verbatim quote matching failed automated validation.",
                "data": output_payload
            }
            
        return {"status": "success", "message": "Groq pipeline executed smoothly.", "data": output_payload}
        
    except Exception as e:
        return {"status": "error", "message": f"Groq Pipeline failed: {str(e)}"}