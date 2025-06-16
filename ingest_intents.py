import json
import logging
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain.embeddings import HuggingFaceEmbeddings

load_dotenv()
log = logging.getLogger(__name__)

with open('ActionPilot/admin/clinic.json', 'r') as handle:
    data = json.load(handle)

intents = data.get('intents')
docs = list()

for intent in intents:
    metadata_copy = json.dumps(intent)
    for utterance in intent.get('utterances'):
        docs.append(
            Document(page_content=utterance, metadata={'dump': metadata_copy})
        )

embedding_model = HuggingFaceEmbeddings(
    model_name="thenlper/gte-base",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False},
)

persist_directory = "./ActionPilot/VectorDB/chroma_db_intents"
vs = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory=persist_directory,
)

log.info(f"Successfully ingested {len(docs)} intent utterances using gte-base embeddings")
