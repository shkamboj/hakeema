from langchain.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import json
import uuid
from typing import Dict, List
from serpapi import GoogleSearch
import os
from google.adk.tools import ToolContext


embedding_model = HuggingFaceEmbeddings(
        model_name="thenlper/gte-base",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )


def retrieve_relevant_context(query: str, n_results: int = 15, score_threshold: float = 0.2) -> Dict[str, List]:
    """
    Retrieve relevant document chunks from Chroma DB based on a query using gte-base embeddings.
    
    Args:
        query (str): The search query
        n_results (int): Number of results to return (default: 5)
        score_threshold (float): Minimum similarity score (0-1) to include (default: 0.7)
    Returns:
        dict: Dictionary containing:
            - 'documents': List of document texts
            - 'scores': List of similarity scores
            - 'metadata': List of metadata dictionaries
            - 'ids': List of document IDs
    """
    
    vs = Chroma(
        persist_directory="./ActionPilot/VectorDB/chroma_db",
        embedding_function=embedding_model
    )
    
    results = vs.similarity_search_with_score(
        query=query,
        k=n_results
    )
    
    documents = []
    scores = []
    metadata = []
    ids = []
    
    for doc, score in results:
        if score >= score_threshold:
            documents.append(doc.page_content)
            scores.append(score)
            metadata.append(doc.metadata)
            ids.append(doc.metadata.get('id', str(hash(doc.page_content))))
    
    return {
        'documents': documents,
        'scores': scores,
        'metadata': metadata,
        'ids': ids
    }

def retrieve_top_5_intents(query: str, n_results: int = 5, score_threshold: float = 0.2) -> Dict[str, List]:
    vs = Chroma(
        persist_directory="./ActionPilot/VectorDB/chroma_db_intents",
        embedding_function=embedding_model
    )
    
    results = vs.similarity_search_with_score(
        query=query,
        k=n_results
    )
    
    intents = []
    covered = set()
    for doc, score in results:
        if score >= score_threshold:
            doc_metadata = doc.metadata.get('dump')
            if doc_metadata:
                metadata_json = json.loads(doc_metadata)
            else:
                metadata_json = {}
            if metadata_json.get('name') not in covered:
                intents.append({
                    'name': metadata_json.get('name'),
                    # 'score': score,
                    # 'metadata': metadata_json
                })
                covered.add(metadata_json.get('name'))

    print(intents, "possible intents")
    return {
        'possible_intents': intents
    }


def fetch_what_entities_needs_to_be_collected(intent: str):
    intent = intent.strip()
    with open('ActionPilot/admin/clinic.json', 'r') as handle:
        data = json.load(handle)
    
    intents = data.get('intents')
    
    for entry in intents:
        if intent == entry.get('name'):
            return entry.get('entities')
    
    return None

def fetch_in_what_structure_entities_needs_to_be_stored(intent: str):
    with open('ActionPilot/admin/clinic.json', 'r') as handle:
        data = json.load(handle)
    
    intents = data.get('intents')
    
    for entry in intents:
        if intent == entry.get('name'):
            return entry.get('entities')
    
    return None


def validate_and_dump_collected_data_json(tool_context: ToolContext, intent: str, json_str: str):
    session_id = tool_context._invocation_context.session.id
    entities_details = fetch_in_what_structure_entities_needs_to_be_stored(intent)
    collection_progress = dict()
    try:
        obj = json.loads(json_str)
        for entity in entities_details:
            if entity.get('key') in obj:
                validation_tool = entity.get('validation_tool')
                value = obj.get(entity.get('key'))
                
                if validation_tool:
                    response = globals()[validation_tool](value)
                    print("debug response, ", response)
                    if type(response) == str:
                        return response
                
                collection_progress[entity.get('key')] = value
            else:
                collection_progress[entity.get('key')] = None
        with open(f"ActionPilot/dumps/{session_id}.json", 'w') as handle:
            json.dump(obj, handle)
        
        return f"Data collected till now: {collection_progress}"
    except Exception as e:
        print(f"exception : {e}")
        return 'Validation failed'



def search_web(query: str):
    """
    Perform a web search.

    Args:
        query (str): The search query.
    Returns:
        list: List of search results (dicts).
    """
    api_key = os.getenv('SERPAPI_API_KEY')
    num_results=10
    location="New Delhi, India"
    hl="en"
    gl="in"
    params = {
        "engine": "google",
        "q": query,
        "location": location,
        "hl": hl,
        "gl": gl,
        "num": num_results,
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    return results.get("organic_results", [])

from datetime import datetime

def get_current_datetime():
    return datetime.now().strftime("%d %B, %Y %H:%M:%S")

def date_is_in_future(iso_date: str):
    if datetime.now().isoformat() < iso_date:
        return True
    else:
        return "The provided date and time is in past, can't be used"

def date_is_in_past(iso_date: str):
    if datetime.now().isoformat() > iso_date:
        return True
    else:
        return "The provided date and time is in future, can't be used"

def today_or_future_date(iso_date: str):
    if datetime.now().isoformat() <= iso_date:
        return True
    else:
        return "The provided date is in the past, can't be used"


def today_or_past_date(iso_date: str):
    if datetime.now().isoformat() >= iso_date:
        return True
    else:
        return "The provided date is in the future, can't be used"



def ten_digit_number(number: str):
    for char in number:
        if char not in '0123456789':
            return 'Not a valid contact number because it contains non numerics'
    
    if len(number) != 10:
        return 'Not a valid contact number because length is not equal to 10'

    
    return True


################# ============================ ################################## (Specific tools to achieve actions) # Memory only
import random, string

patients = dict()

def _generate_unique_id(object):
    while True:
        
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=6))
        new_id = letters + numbers
        if new_id not in patients:
            patients[new_id] = object
            return new_id

def register_patient(object: dict):
    """Registers a new patient in the system.

    This function takes a dictionary containing patient information and validates 
    each field before registering the patient. The expected keys in the input dictionary are:

    - `patient_name`: String.
    - `date_of_birth`: ISO_DateTime. 
    - `contact_number`: 10-digit number.
    - `insurance_provider`: String.
    - `emergency_contact_name`: String. 
    - `emergency_contact_number`: 10-digit number.
    - `address`: String.

    Args:
        object (dict): A dictionary containing the patient's registration details.

    Returns:
        dict: Patient ID registered for the new patient
    """

    new_id = _generate_unique_id(object)
    return new_id

def submit_feedback(object: dict):
    pass
