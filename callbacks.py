from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional
import json


def validate_intent_prediction(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Logs exit from an agent and validates 'intent' in session state.
    If valid intent, returns None.
    If not valid, modify the state `intent` and sends the new content to update.
    """
    current_state = callback_context.state.to_dict()
    
    with open("ActionPilot/admin/clinic.json", "r") as handle:
        data = json.load(handle)
    
    intents = data["intents"]
    valid_intents = [intent["name"] for intent in intents]
    if current_state.get("intent") and current_state.get("intent").strip() in valid_intents:
        # current_state['intent'] = current_state.get("intent").strip()
        return None
    else:
        # current_state['intent'] = None
        return types.Content(
            parts=[types.Part(text=f"Validation is failed for intent predicted, I would ask you more followups first.")],
            role="model"
        )
