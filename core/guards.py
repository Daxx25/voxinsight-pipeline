# core/guards.py
import re

def verify_verbatim_quote(raw_text: str, extracted_quote: str) -> dict:
    """
    Deterministically validates whether the LLM's extracted quote actually 
    exists inside the raw customer transcript.
    
    Returns a dict with verification status and metadata.
    """
    # Clean whitespace and newlines for a robust match
    normalized_raw = " ".join(raw_text.split())
    normalized_quote = " ".join(extracted_quote.split())
    
    # Check 1: Exact Match (Case-Sensitive)
    if normalized_quote in normalized_raw:
        return {"verified": True, "type": "exact", "matched_quote": extracted_quote}
        
    # Check 2: Case-Insensitive Fallback
    if normalized_quote.lower() in normalized_raw.lower():
        # Find the original case matching string inside raw text to maintain integrity
        start_idx = normalized_raw.lower().find(normalized_quote.lower())
        original_chunk = normalized_raw[start_idx : start_idx + len(normalized_quote)]
        return {"verified": True, "type": "case_insensitive", "matched_quote": original_chunk}
        
    # Check 3: Fuzzy Check for minor punctuation omissions (e.g., stripping quotes/periods)
    clean_raw = re.sub(r'[^\w\s]', '', normalized_raw.lower())
    clean_quote = re.sub(r'[^\w\s]', '', normalized_quote.lower())
    
    if clean_quote in clean_raw and len(clean_quote) > 10:
        return {"verified": True, "type": "fuzzy_punctuation", "matched_quote": extracted_quote}

    # If all fail, the LLM paraphrased or hallucinated the quote
    return {"verified": False, "type": "hallucination_detected", "matched_quote": extracted_quote}