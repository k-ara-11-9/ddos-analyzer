# DDoS Analyzer (RAG-based Network Flow Analysis)

## Overview
This project implements a Retrieval-Augmented Generation (RAG) pipeline to analyze network flow records and distinguish Distributed Denial-of-Service (DDoS) traffic from benign traffic. The system is built on the CIC-DDoS2019 dataset and allows natural language queries that are grounded in real network telemetry rather than relying on generic model knowledge.

The pipeline consists of:
1. Preprocessing and balancing a large CSV dataset of network flows
2. Converting each record into a structured textual representation
3. Generating embeddings using Ollama and storing them in a Chroma vector database
4. Retrieving relevant flows at query time and passing them as context to a large language model

This enables exploratory, data-driven analysis of cybersecurity traffic patterns.

---

## Project Structure
```
ddos-analyzer/
│
├── data/
│   ├── raw/                 # Original CIC-DDoS2019 dataset
│   └── processed/          # Balanced and sampled CSV used for embeddings
│
├── src/
│   ├── prepare_data.py     # Dataset sampling and preprocessing
│   ├── vector.py           # Embedding and vector database creation
│   └── main.py             # Query interface using RAG
│
├── chroma_langchain_db/    # Persisted Chroma vector database
└── README.md
```

---

## Dataset
The project uses a subset of the **CIC-DDoS2019** dataset, which contains labeled network flow records for benign and DDoS traffic. A balanced sample is created to ensure equal representation of both classes.

### Dataset Citation
If you use this project or the dataset in reports or presentations, please cite:

Canadian Institute for Cybersecurity (CIC), University of New Brunswick. *CIC-DDoS2019 Dataset*. Available via Kaggle: https://www.kaggle.com/datasets/aymenabb/ddos-evaluation-dataset-cic-ddos2019

Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). Toward generating a new intrusion detection dataset and intrusion traffic characterization. *Proceedings of ICISSP*.

---

## Setup

### Models and Performance
This project uses two Ollama models by default:
- **LLM**: `llama3.2` (used for answering questions)
- **Embeddings**: `mxbai-embed-large` (used for vectorization)

**Runtime note:** `mxbai-embed-large` provides high-quality embeddings but can be slow on CPU, especially for several thousand rows. For faster development iterations, you may temporarily switch to a lighter model such as `nomic-embed-text`, then revert to `mxbai-embed-large` for final runs.

To change the embedding model, update it in both `src/vector.py` and `src/main.py`:
- Development (faster): `nomic-embed-text`
- Final (higher quality): `mxbai-embed-large`



### 1. Create Virtual Environment

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

**All platforms:**
```bash
pip install pandas langchain langchain-ollama langchain-chroma chromadb
```

Ensure **Ollama** is installed and running locally with the required models:
- `llama3.2`
- `mxbai-embed-large`

To pull models explicitly:
```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

```bash
pip install pandas langchain langchain-ollama langchain-chroma chromadb
```

Ensure **Ollama** is installed and running locally with the required models:
- `llama3.2`
- `mxbai-embed-large`

---

## Usage

### Step 1: Preprocess Dataset
Creates a balanced sample of benign and attack flows.

**Windows:**
```bash
python src/prepare_data.py
```

**Linux / macOS:**
```bash
python3 src/prepare_data.py
```

### Step 2: Build Vector Database
Embeds the processed dataset and stores vectors in Chroma.

**Windows:**
```bash
python src/vector.py
```

**Linux / macOS:**
```bash
python3 src/vector.py
```

This step is computationally expensive but is performed only once. Subsequent runs will reuse the stored vectors.

### Step 3: Query the System
Start the interactive query interface:

**Windows:**
```bash
python src/main.py
```

**Linux / macOS:**
```bash
python3 src/main.py
```

---


## Example High-Level Questions
These questions are designed to demonstrate retrieval-grounded reasoning rather than generic explanations:

1. **"What are the key characteristics that differentiate DDoS traffic from benign traffic in this dataset?"**
2. **"Which network flow features most clearly separate attack traffic from normal traffic based on the retrieved records?"**
3. **"How do packet rates and flow durations differ between DDoS and benign flows in the dataset?"**
4. **"What measurable indicators from this dataset could be used in a real-time DDoS detection system?"**
5. **"Summarize common behavioral patterns observed in malicious traffic compared to benign traffic."**

The responses are generated using only the retrieved dataset context, ensuring that the answers are grounded in real network flow records.

---

## Technical Approach

- **Preprocessing**: Filters and samples the raw dataset to create a balanced subset.
- **Text Representation**: Each network flow record is converted into a descriptive textual format capturing protocol, packet statistics, flow duration, flags, and labels.
- **Embedding**: Text representations are embedded using `mxbai-embed-large` via Ollama.
- **Vector Storage**: Embeddings are stored in a persistent Chroma vector database.
- **Retrieval + Generation**: At query time, the most relevant records are retrieved and passed to a language model, enabling context-aware analysis.

---

## Applications
- Exploratory analysis of network traffic
- Demonstration of Retrieval-Augmented Generation in cybersecurity
- Feature-level understanding of DDoS attack behavior
- Educational and research prototyping

---

## Future Improvements
- Add statistical aggregation for numeric features (e.g., averages per label)
- Visualize traffic patterns using graphs
- Expand to multi-class attack classification
- Integrate streaming or near real-time flow ingestion

---

## License
This project is intended for educational and research purposes.

