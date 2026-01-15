from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load processed dataset
df = pd.read_csv("data/processed/ddos_balanced_sample.csv")

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
db_location = "./chroma_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    for i, row in df.iterrows():
        text = (
            f"Flow observed at {row['Timestamp']}: {row['Source IP']}:{row['Source Port']} -> "
            f"{row['Destination IP']}:{row['Destination Port']} using protocol {row['Protocol']}.\n"
            f"Flow duration: {row['Flow Duration']} units.\n"
            f"Packets: Forward {row['Total Fwd Packets']}, Backward {row['Total Backward Packets']}.\n"
            f"Packet lengths (Fwd/ Bwd): Max {row['Fwd Packet Length Max']}/{row['Bwd Packet Length Max']}, "
            f"Min {row['Fwd Packet Length Min']}/{row['Bwd Packet Length Min']}, "
            f"Mean {row['Fwd Packet Length Mean']}/{row['Bwd Packet Length Mean']}, "
            f"Std {row['Fwd Packet Length Std']}/{row['Bwd Packet Length Std']}.\n"
            f"Flow rates: Bytes/s {row['Flow Bytes/s']}, Packets/s {row['Flow Packets/s']}.\n"
            f"Flags counts: FIN {row['FIN Flag Count']}, SYN {row['SYN Flag Count']}, RST {row['RST Flag Count']}, "
            f"PSH {row['PSH Flag Count']}, ACK {row['ACK Flag Count']}, URG {row['URG Flag Count']}.\n"
            f"Label: {row['Label']}."
        )

        meta = {
            "source_ip": row["Source IP"],
            "dest_ip": row["Destination IP"],
            "protocol": row["Protocol"],
            "label": row["Label"]
        }

        documents.append(Document(page_content=text, metadata=meta))

    # Create vector DB
    db = Chroma.from_documents(
        documents,
        embeddings,
        persist_directory=db_location
    )
    print(f"Vector DB created at {db_location} with {len(documents)} documents.")
else:
    print(f"Vector DB already exists at {db_location}.")
