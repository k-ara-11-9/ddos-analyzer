from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

model = OllamaLLM(model="llama3.2")

template = """
You are a cybersecurity expert analyzing network flow records.

Use ONLY the provided data context to answer.
If something is not present in the data, say so clearly.

Here is the relevant dataset context:
{data}

Question:
{question}

Provide a concise, technical answer based on the dataset.
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

embeddings = OllamaEmbeddings(model="mxbai-embed-large")
db_location = "./chroma_langchain_db"

db = Chroma(
    persist_directory=db_location,
    embedding_function=embeddings
)

print("\nDDoS Analyzer — Interactive Query Mode\n")

while True:
    print("\n" + "=" * 70)
    question = input("Ask your question (q to quit): ").strip()
    print("=" * 70)
    print("\n")

    if question.lower() == 'q':
        print("\nExiting...\n")
        break

    docs = db.similarity_search(question, k=5)

    if not docs:
        print("No relevant data found in the database.")
        continue

    context = "\n".join(
        [f"{doc.metadata['label']} flow from {doc.metadata['source_ip']} -> {doc.metadata['dest_ip']}: {doc.page_content}" for doc in docs]
    )

    result = chain.invoke({"data": context, "question": question})
    print(result)