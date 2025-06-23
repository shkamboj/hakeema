# ADK Hack

Repo for ADK hackathon.

Generic Agent for predicting actions, collection their data, and executing them.

TODO: when running `adk web` make sure only one directory is assuemd to be of agents, skip others like `scripts/`, or have a list of directories that contain agent stored somewhere as config.

## Setup

1. Run  to install ActionPilot agent's requirements.
    ```bash
    pip install -r requirements.txt
    ```
2. Run to ingest actions data. (currently one example is used.)
    ```bash
    python scripts/ingest_intents.py -c <path_to_json_file>
    ```
3. Run to ingest KB. (currently few urls only used.)
    ```bash
    python scripts/ingest_kb.py
    ```
4. Run  to initiate the web UI on port 8000.
    ```bash
    adk web
    ```
