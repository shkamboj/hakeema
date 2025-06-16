from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PlaywrightURLLoader
from langchain.embeddings import HuggingFaceEmbeddings  # Changed from OpenAIEmbeddings

load_dotenv()

urls = [
    "https://www.genomicseducation.hee.nhs.uk/genotes/knowledge-hub/wilson-disease/", 
    "https://www.genomicseducation.hee.nhs.uk/genotes/in-the-clinic/presentation-clinical-suspicion-of-bloom-syndrome/",
    "https://en.wikipedia.org/wiki/Narendra_Modi",
]

# Load documents
loader = PlaywrightURLLoader(urls=urls)
docs = loader.load()

# Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
splits = text_splitter.split_documents(docs)

# Set up gte-base embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="thenlper/gte-base",
    model_kwargs={'device': 'cpu'},  # or 'cuda' if you have GPU
    encode_kwargs={'normalize_embeddings': True},  # Important for cosine similarity
)

# Create and persist vector store
persist_directory = "./ActionPilot/VectorDB/chroma_db"
vs = Chroma.from_documents(
    documents=splits,
    embedding=embedding_model,  # Using gte-base instead of OpenAI
    persist_directory=persist_directory,
)

print(f"Successfully ingested {len(splits)} document chunks using gte-base embeddings")
