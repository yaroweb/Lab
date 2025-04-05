from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import StorageContext, load_index_from_storage
import os

# Lokales LLM & Embeddings
llm = Ollama(model="llama3.2:latest")
embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# Daten einlesen
data_dir = "insolvenz_daten"
documents = SimpleDirectoryReader(input_dir=data_dir).load_data()

# Index aufbauen oder laden
if not os.path.exists("storage"):
    index = VectorStoreIndex.from_documents(
        documents,
        llm=llm,
        embed_model=embed_model
    )
    index.storage_context.persist(persist_dir="storage")
else:
    storage_context = StorageContext.from_defaults(persist_dir="storage")
    index = load_index_from_storage(
        storage_context,
        llm=llm,
        embed_model=embed_model
    )

# Chat-Engine starten – LLM explizit übergeben!
chat_engine = index.as_chat_engine(
    llm=llm,
    chat_mode="condense_question",
    verbose=True
)

# Beispiel-Chat
frage = "Welche Fristen gelten für Gläubigerversammlungen?"
antwort = chat_engine.chat(frage)

print("Antwort:", antwort.response)