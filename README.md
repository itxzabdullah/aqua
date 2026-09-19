# WQI Agentic Layer

An agentic layer for a Water Quality Index (WQI) machine learning pipeline, built around LangGraph, Google Gemini, Retrieval-Augmented Generation (RAG), and trained machine learning models.

The system is designed to make existing WQI predictions, water-quality classifications, risk forecasts, and regulatory knowledge accessible through conversational interaction and automated report generation.

---

## Overview

The project provides two specialized AI agents:

1. **Conversational Chatbot Agent**
   - Allows users, field officers, and environmental researchers to ask questions about water samples and water-quality regulations.
   - Retrieves information from WHO and Pakistan NSDWQ regulatory sources.
   - Invokes trained machine learning models when quantitative predictions are required.
   - Produces grounded responses with source citations.
   - Uses a self-checking mechanism to identify unsupported claims.

2. **Report Generation Agent**
   - Converts validated machine-learning predictions into structured reports.
   - Generates compliance summaries, water-quality classifications, and projected risk information.
   - Performs programmatic validation before document generation.
   - Exports reports in DOCX and PDF formats.

Both agents share a common foundation consisting of a regulatory knowledge base, trained machine-learning models, and report templates.

---

## System Architecture

```text
                         ┌─────────────────────┐
                         │        USER         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │      CHATBOT AGENT        │
                    │        LangGraph          │
                    └─────────────┬─────────────┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                         ▼                 ▼
                  ┌─────────────┐   ┌─────────────┐
                  │ Retrieval   │   │ ML Tool     │
                  │ Node        │   │ Node        │
                  └──────┬──────┘   └──────┬──────┘
                         │                 │
                         ▼                 ▼
                  ┌─────────────┐   ┌─────────────┐
                  │   Chroma    │   │ CatBoost    │
                  │ WHO/NSDWQ   │   │ Gradient    │
                  │ Knowledge   │   │ Boosting    │
                  │ Base        │   │ ARIMA       │
                  └──────┬──────┘   └──────┬──────┘
                         │                 │
                         └────────┬────────┘
                                  ▼
                         ┌────────────────┐
                         │   Generation   │
                         │      Node      │
                         └───────┬────────┘
                                 ▼
                         ┌────────────────┐
                         │   Self-Check   │
                         │     (CRAG)     │
                         └───────┬────────┘
                                 │
                                 ▼
                                USER


                    SHARED FOUNDATION
              ┌──────────────────────────────┐
              │ WHO / NSDWQ Knowledge Base   │
              │ Chroma Vector Store          │
              │ CatBoost Regression          │
              │ Gradient Boosting Classifier │
              │ ARIMA Forecasting             │
              │ Report Templates             │
              └──────────────┬───────────────┘
                             │
                             ▼
                 ┌────────────────────────┐
                 │   REPORT AGENT         │
                 │      LangGraph         │
                 └───────────┬────────────┘
                             │
                             ▼
                Data Fetch → Template Select
                             │
                             ▼
                       Narrative Draft
                             │
                             ▼
                       QA Validation
                             │
                             ▼
                       Format & Export
                             │
                         ┌───┴───┐
                         ▼       ▼
                       DOCX     PDF
````

---

## Agents

### Agent 1 — Conversational Chatbot

The chatbot uses the following LangGraph workflow:

```text
Router
   │
   ├── Retrieval Node
   │
   ├── Tool-Call Node
   │
   └── Hybrid Query
          │
          ▼
     Generation
          │
          ▼
      Self-Check
```

The router identifies the type of incoming request:

* **Statutory / policy lookup**
* **Real-time sample inference**
* **Compound queries requiring both retrieval and model inference**

The retrieval node searches the regulatory knowledge base.

The tool-call node invokes the appropriate machine-learning model.

The generation node combines retrieved evidence and model outputs into a natural-language response.

The self-check node verifies that the generated response is supported by the available evidence.

---

### Agent 2 — Report Generation

The report-generation agent follows a deterministic linear pipeline:

```text
Data Fetch
    ↓
Template Selection
    ↓
Narrative Draft
    ↓
QA Validation
    ↓
Format & Export
```

The agent is intended to generate structured reports for:

* Individual water-sample compliance
* Regional or municipal summaries
* Longitudinal water-quality risk trends

The QA stage verifies that quantitative values in the generated narrative correspond to the underlying model outputs before the document is exported.

---

## Machine Learning Models

The agentic layer exposes the existing trained models through programmatic tools.

### CatBoost

Used for:

```text
WQI continuous regression
```

Planned tool:

```python
predict_wqi()
```

### Gradient Boosting

Used for:

```text
Water-quality classification
```

Planned tool:

```python
classify_water_quality()
```

### ARIMA

Used for:

```text
Temporal risk-score forecasting
```

Planned tool:

```python
forecast_risk()
```

The models are treated as deterministic computational tools. The LLM does not replace the trained models or independently calculate their predictions.

---

## Knowledge Base

The RAG knowledge base is built from water-quality regulatory and technical information.

### Primary Sources

* WHO Guidelines for Drinking-water Quality
* Pakistan National Standards for Drinking Water Quality (NSDWQ)
* WQI mathematical formulas
* Relevant parameter toxicity and health-risk references

### Knowledge Base Pipeline

```text
Source Documents
      ↓
Document Parsing
      ↓
Chunking
      ↓
Metadata Tagging
      ↓
Embeddings
      ↓
Chroma Vector Store
      ↓
Hybrid Retrieval
```

### Metadata

Documents are tagged with metadata such as:

```text
jurisdiction
parameter
category
unit
source
threshold type
health-risk information
```

Jurisdiction metadata allows retrieval to distinguish between sources such as:

```text
WHO
NSDWQ
```

---

## Retrieval

The planned retrieval architecture combines:

* Dense semantic retrieval
* BM25 keyword retrieval
* Metadata filtering

The goal is to support queries where exact regulatory terminology and semantic meaning are both important.

Example:

```text
"What is the permissible turbidity limit according to Pakistan NSDWQ?"
```

The retrieval system should identify relevant Pakistan NSDWQ material rather than relying only on general semantic similarity.

---

## Technology Stack

| Component            | Technology                         |
| -------------------- | ---------------------------------- |
| Agent orchestration  | LangGraph                          |
| LLM                  | Google Gemini                      |
| LLM integration      | LangChain / LangChain Google GenAI |
| Vector database      | Chroma                             |
| Sparse retrieval     | BM25                               |
| Data processing      | pandas                             |
| Regression model     | CatBoost                           |
| Classification model | Gradient Boosting                  |
| Forecasting model    | ARIMA                              |
| DOCX generation      | python-docx                        |
| PDF generation       | ReportLab                          |
| Evaluation           | RAGAS + Numeric QA                 |
| Testing              | pytest                             |

---

## Project Structure

```text
WQI-Agent/
│
├── agents/
│   ├── chatbot/
│   └── reporting/
│
├── rag/
│   ├── ingestion.py
│   ├── documents.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── vector_store.py
│
├── models/
│   ├── catboost_tool.py
│   ├── gradient_boosting_tool.py
│   └── arima_tool.py
│
├── reports/
│   ├── templates/
│   ├── generator.py
│   └── validator.py
│
├── schemas/
│   └── state.py
│
├── data/
│   ├── WHO_Drinking_Water_Quality_Standards.csv
│   └── Pakistan_NSDWQ_Standards_Sample_Parameters.csv
│
├── tests/
│
├── main.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

> The structure will evolve as implementation progresses.

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd WQI-Agent
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Do not commit `.env` to version control.

---

## Development Roadmap

### Phase 1 — Architecture & Knowledge Base

* [ ] Project environment setup
* [ ] WHO dataset ingestion
* [ ] Pakistan NSDWQ dataset ingestion
* [ ] Document construction
* [ ] Metadata tagging
* [ ] Chroma vector-store setup
* [ ] Dense retrieval
* [ ] BM25 retrieval
* [ ] Hybrid retrieval
* [ ] Retrieval evaluation

### Phase 2 — Chatbot Agent

* [ ] LangGraph state definition
* [ ] Router node
* [ ] Retrieval node
* [ ] ML tool node
* [ ] CatBoost tool integration
* [ ] Gradient Boosting tool integration
* [ ] ARIMA tool integration
* [ ] Generation node
* [ ] Citation handling
* [ ] Self-check / CRAG node
* [ ] Query reformulation
* [ ] End-to-end chatbot testing

### Phase 3 — Report Generation Agent

* [ ] Data-fetch node
* [ ] Report template selection
* [ ] Narrative drafting
* [ ] Numeric QA validation
* [ ] Compliance validation
* [ ] DOCX generation
* [ ] PDF generation
* [ ] End-to-end report testing

### Phase 4 — Evaluation & Deployment

* [ ] RAGAS evaluation
* [ ] Context retrieval evaluation
* [ ] Answer faithfulness evaluation
* [ ] Citation verification
* [ ] Numeric consistency evaluation
* [ ] End-to-end user acceptance testing
* [ ] Deployment preparation

---

## Safety & Grounding

Water-quality guidance can have direct health and safety implications.

The system therefore follows a grounding-first architecture:

```text
Regulatory Claim
      ↓
Retrieved Evidence
      ↓
Generated Response
      ↓
Evidence Verification
      ↓
User
```

Safety and potability statements should be grounded in the relevant WHO or Pakistan NSDWQ source material.

Similarly, quantitative predictions should originate from the trained machine-learning models rather than being generated or calculated by the LLM.

---

## Evaluation

The system will be evaluated using two complementary approaches.

### RAG Evaluation

RAGAS will be used to evaluate aspects such as:

* Context relevance
* Context retrieval
* Answer faithfulness

### Numeric Validation

Programmatic validation will check that:

```text
Model Output
      ==
Reported Numerical Value
```

This is particularly important for automated report generation.

---

## Current Development Status

**Status: Initial Development**

Current focus:

```text
Project Setup
      ↓
Data Ingestion
      ↓
RAG Document Construction
      ↓
Chroma Retrieval
      ↓
LangGraph Agents
      ↓
Evaluation
```

The implementation is being developed incrementally, with each foundation component tested independently before being connected to the agentic layer.

---

## Project Design Reference

The architecture and implementation plan are based on the project design document:

**Agentic Layer for the Water Quality Index (WQI) Machine Learning Pipeline**

The approved design specifies LangGraph-based conversational and report-generation agents, a WHO/NSDWQ RAG knowledge base, callable CatBoost/Gradient Boosting/ARIMA models, deterministic report generation, and RAGAS/numeric evaluation.