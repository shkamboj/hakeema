import os
import logging
from google.genai import types
from google.adk.tools.agent_tool import AgentTool
from google.adk.agents import LlmAgent, SequentialAgent, Agent, LoopAgent

from ._log_formatter import CustomFormatter
from .structures import IntentPredictionOutput
from .callbacks import validate_intent_prediction
from .tools import register_patient, submit_feedback
from .tools import fetch_in_what_structure_entities_needs_to_be_stored
from .prompts import (
    ROOT_AGENT_PROMPT, KB_AGENT_PROMPT, INTENT_ENTITY_AGENT_PROMPT, INTENT_PREDICTION_AGENT_PROMPT,
)
from .tools import (
    validate_and_dump_collected_data_json, search_web, get_current_datetime, date_is_in_future,
    fetch_what_entities_needs_to_be_collected, retrieve_relevant_context, retrieve_top_5_intents,
)


custom_handler = logging.StreamHandler()
custom_handler.setFormatter(CustomFormatter())
logging.basicConfig(
    level=logging.INFO,
    handlers=[custom_handler],
)

greeting_agent = LlmAgent(
    name="General_Chat_Agent",
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
    model="gemini-2.0-flash-exp",
    description="Handles general chat which is not about specific actions/questions.",
)

intent_prediction_agent = LlmAgent(
    name="Intent_Prediction_Agent",
    model="gemini-2.0-flash-exp",
    output_key='intent',
    tools=[retrieve_top_5_intents],
    description="Agent for robustly predicting the user's intent from a predefined list.",
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
    instruction=INTENT_PREDICTION_AGENT_PROMPT,
    after_agent_callback=validate_intent_prediction
)

# validate_data_agent = LlmAgent(
#     name="Validate_Data_Agent",
#     model="gemini-2.0-flash",
#     description="Validates the data collected at any given point of entity collection",
#     instruction="""
#     You need to call the tool validate_entity_data to validate the values captured till now.
#     You also has access to the current datetime function to get today's date
#     and current time if you need it for some resolution.
#     """,
#     tools=[validate_entity_data, get_current_datetime]
# )
# 5. Whenever you collect new data you need to validate it using validate data agent every time.

# action_data_restructure_agent = LlmAgent(
#     name="Restructure_Data_Agent",
#     model="gemini-2.5-flash-preview-05-20",
#     generate_content_config=types.GenerateContentConfig(temperature=0.0),
#     description='Can restructure the collected entities data, once whole of the entities is collected',
#     instruction="""Restructure the recently captured data strictly into format provided by the structure tool.
#     Return the output in JSON format only.""",
#     tools=[fetch_in_what_structure_entities_needs_to_be_stored],
# )

action_executor_agent = Agent(
    name="Action_Executor_Agent",
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
    model="gemini-2.0-flash-exp",
    description=(
        "Agent used to executed the actions based on predicted intent and collected entities",
    ),
    instruction="""
    You have access to multiple tools, you can execute actions as per requirements.
    Just ask a confirmation from the user before proceeding.
    """,
    tools=[register_patient, submit_feedback]
)

intent_entity_agent = LlmAgent(
    name="Intent_Entity_Agent",
    description = "Agent to handle intent prediction to entity collection",
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
    model="gemini-2.0-flash-exp",
    instruction=INTENT_ENTITY_AGENT_PROMPT,
    tools=[AgentTool(agent=intent_prediction_agent),
    fetch_what_entities_needs_to_be_collected,
    validate_and_dump_collected_data_json,
    get_current_datetime],
    sub_agents=[action_executor_agent],
)

kb_agent = LlmAgent(
    name="Knowledge_Base_Agent",
    model="gemini-2.0-flash-exp",
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
    instruction=KB_AGENT_PROMPT,
    description="Fetches context from knowledge base and generates an answer for the query.",
    tools=[retrieve_relevant_context, search_web],
)

notification_agent = LlmAgent(
    name="Notification_Agent",
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
    description="Transforms final responses into formats for channels such as email/whatsapp and sends it to user.",
)

root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash-exp",
    generate_content_config=types.GenerateContentConfig(temperature=0.0),
    description=(
        "Root agent"
    ),
    instruction=ROOT_AGENT_PROMPT,
    sub_agents=[greeting_agent, intent_entity_agent, kb_agent, notification_agent],
)

