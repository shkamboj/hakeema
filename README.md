# Hakeema: AI-Powered Patient Experience Platform
Hakeema is an intelligent, conversational AI platform built with Google's Gemini and Agent Development Kit (ADK) to automate and streamline patient-clinic interactions, creating a seamless and modern healthcare experience.

## 🚀 The Problem
The administrative side of healthcare is often a source of friction for patients. Long wait times on the phone, confusing processes for registration, and difficulty getting timely information create a frustrating experience. For clinics, these manual processes are inefficient, costly, and divert staff from focusing on high-value patient care.

## ✨ Our Solution
Hakeema provides clinics with a 24/7 virtual assistant that intelligently handles a wide range of patient needs. By integrating a natural language interface into a clinic's website or app, Hakeema makes healthcare administration effortless for patients and efficient for providers.

This project was developed for a Google Hackathon, with a focus on leveraging Google's powerful AI stack to solve a real-world problem.

## 🎬 Demo
Watch the Video Demo: [Link to your 2-minute video walkthrough]

Try it Live: [Link to your live deployment, if available]

## 🌟 Key Features
Multi-Turn Intent Handling: Manages complex, conversational workflows for a variety of tasks.

Intelligent Appointment Booking: Schedule appointments through a natural conversation.

New Patient Registration: Onboard new patients with a guided, conversational form.

On-Demand Information: Instantly answer queries about visiting hours, services, and more.

Secure Bill Payment & Test Result Inquiries: Handle sensitive tasks with a clear flow for authenticated users.

Feedback Collection: Easily gather and structure patient compliments or complaints.

Highly Extensible: New intents and capabilities can be added by simply updating a JSON configuration, requiring minimal code changes.

## 🏗️ How It Works: A Multi-Agent Architecture
Hakeema is built on a sophisticated multi-agent architecture using the Google Agent Development Kit (ADK). This design ensures that tasks are handled by specialized agents, leading to more robust and accurate outcomes.

Triage with the root_agent: All user input first hits the root_agent. Its job is to determine the user's general purpose: is it chit-chat, a request for information, or an action-oriented task?

Intent Prediction: For actions, the root_agent routes the query to the intent_entity_agent. This agent uses a sub-agent for precise intent recognition in a two-step process:

Retrieval: It uses a Chroma vector database and a Hugging Face embedding model (thenlper/gte-base) to retrieve the Top 5 most semantically similar intents from our predefined list.

Reasoning: The powerful Gemini 2.0 Flash model then analyzes these 5 options in the context of the user's query to make a final, highly accurate prediction.

Conversational Entity Collection: Once the intent is known (e.g., register_new_patient), the intent_entity_agent begins a multi-turn conversation to collect the necessary information (entities like patient_name, date_of_birth, etc.).

Real-Time Validation: As each piece of information is collected, it is passed to a validation tool. This tool checks the data against predefined rules (e.g., today_or_past_date, ten_digit_number). This ensures data integrity before the final action is executed.

Action Execution: After all required entities are collected and validated, the action_executor_agent takes over. It confirms the details with the user one last time and then calls the final tool (e.g., register_patient) to complete the process.

## 🛠️ Technology Stack
Core AI/LLM: Google Gemini 2.0 Flash

Agent Framework: Google Agent Development Kit (ADK)

Backend: Python

Vector Database: Chroma DB

Embeddings: Hugging Face thenlper/gte-base

Supporting Libraries: LangChain, SerpAPI


## 🔮 What's Next: The Roadmap for Hakeema
We are excited about the future of Hakeema and plan to expand its capabilities:

Google Wallet Integration: Allow seamless payment of medical bills.

Google Maps Integration: Provide directions to the clinic after booking an appointment.

Voice and Multimodality: Enable interaction via voice with Google Assistant and allow users to upload images of insurance cards or prescriptions.

Proactive Notifications: Use RCS Business Messaging to send appointment reminders, test result alerts, and post-visit surveys.

Deployment on Google Cloud: Migrate the infrastructure to Google Cloud for enhanced scalability, security, and integration with services like Cloud Functions and Cloud SQL.



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
