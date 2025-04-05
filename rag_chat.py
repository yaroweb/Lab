from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.core.chat_engine import SimpleChatEngine

# 1. LLM initialisieren
llm = Ollama(model="llama3")

# 2. Datenquellen laden (z. B. PDFs als Text konvertiert)
documents = SimpleDirectoryReader("insolvenz_daten").load_data()

# 3. Index erstellen
index = VectorStoreIndex.from_documents(documents)

# 4. Chat-Engine aus Index bauen
chat_engine = index.as_chat_engine(llm=llm, chat_mode="condense_question", verbose=True)

# 5. Chat starten (z. B. aus API aufrufbar machen)
response = chat_engine.chat("Welche Fristen gelten für Gläubigerversammlungen?")
print(response.response)
