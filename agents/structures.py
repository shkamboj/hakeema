from typing import Optional
from pydantic import BaseModel, Field


class IntentPredictionOutput(BaseModel):
    intent: Optional[str] = Field(description="predicted intent", default=None)
