# core/schemas.py
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional

class ProductArea(str, Enum):
    AUTH = "Authentication & Login"
    DASHBOARD = "Analytics Dashboard"
    BILLING = "Billing & Invoicing"
    INTEGRATIONS = "Integrations & APIs"
    CORE_UI = "Core UI & Navigation"

class SourceType(str, Enum):
    GONG = "Gong Call"
    ZENDESK = "Zendesk Ticket"
    INTERCOM = "Intercom Chat"

class CustomerInsight(BaseModel):
    """The strict schema that the LLM MUST adhere to when extracting data."""
    product_area: ProductArea = Field(
        description="The primary product area this feedback falls into."
    )
    sentiment_score: float = Field(
        description="Strict float from -1.0 (extreme frustration) to 1.0 (extreme delight)."
    )
    summary: str = Field(
        description="A concise 1-sentence summary of the user's core problem or feedback."
    )
    pain_points: List[str] = Field(
        description="Specific, clear bullet points of friction. Empty list if none."
    )
    feature_requests: List[str] = Field(
        description="Explicit requests for new capabilities. Empty list if none."
    )
    verbatim_quote: str = Field(
        description="The EXACT, unaltered quote from the transcript proving the pain point. DO NOT paraphrase."
    )