# ADK Hack

Repo for ADK hackathon.

Generic Agent for predicting actions, collection their data, and executing them.

## Setup

1. Run  to install ActionPilot agent's requirements.
    ```bash
    pip install -r requirements.txt
    ```
2. Run to ingest actions data. (currently one example is used.)
    ```bash
    python ingest_intents.py -c <path_to_json_file>
    ```
3. Run to ingest KB. (currently few urls only used.)
    ```bash
    python ingest_kb.py
    ```
4. Run  to initiate the web UI on port 8000.
    ```bash
    adk web
    ```
