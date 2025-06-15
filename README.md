# adk-hack
Repo for ADK hackathon

### (Generic Agent for predicting actions, collection their data, and executing them).

## Steps to run
1. Run `pip install -r ActionPilot/requirements.txt` to install ActionPilot agent's requirements.
2. Run `python ActionPilot/ingest_intents.py` to ingest actions data. (currently one example is used.)
3. Run `python ActionPilot/ingest_kb.py` to ingest KB. (currently few urls only used.)
4. Run `adk web` to initiate the web UI on port 8000.
