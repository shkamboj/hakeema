import json
import logging
import argparse
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings


from agents._utils import validate_file_path
from agents._log_formatter import CustomFormatter

load_dotenv()
log = logging.getLogger(__name__)


if __name__ == '__main__':
    custom_handler = logging.StreamHandler()
    custom_handler.setFormatter(CustomFormatter())
    logging.basicConfig(
        level=logging.INFO,
        handlers=[custom_handler],
    )

    parser = argparse.ArgumentParser(description="Script to ingest intent utterances into a vector database.")
    parser.add_argument("-c", "--config", dest="config_file", required=True, type=validate_file_path,
                        help="configuration json file path", metavar="FILE")
    args = parser.parse_args()

    log.info(f"Using config file: {args.config_file}")
    with open(args.config_file, 'r') as handle:
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

    persist_directory = "./VectorDB/chroma_db_intents"
    log.info(f"Persisting vector store to {persist_directory}")
    vs = Chroma.from_documents(
        documents=docs,
        embedding=embedding_model,
        persist_directory=persist_directory,
    )

    log.info(f"Successfully ingested {len(docs)} intent utterances using gte-base embeddings")
