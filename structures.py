from pydantic import BaseModel, Field
from typing import Optional

class IntentPredictionOutput(BaseModel):
    intent: Optional[str] = Field(description="predicted intent", default=None)
