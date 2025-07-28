
# 📘 Persona-Based Semantic PDF Analyzer – Adobe Hackathon Round 2 Submission

> 🔍 **Submission for Adobe 'Connecting the Dots' Hackathon — Round 2**

This project is a backend system that intelligently extracts and ranks relevant sections from a collection of PDF documents based on a user persona and their job-to-be-done. It is designed to assist knowledge workers — like Students, Professors and Working Professionals — in quickly accessing the most relevant information from large, unstructured documents.


---

## 🧠 Problem Statement

In professional environments, experts often deal with lengthy documents without clear structure or navigation. This project enables machines to:
- Interpret document structure (headings and hierarchy)
- Identify and rank content relevant to the user's role and goal
- Summarize it for quick understanding

---

## 👤 Use Case

**Persona**: Investment Analyst  
**Goal**: Analyze trends in R&D spending across companies

---
# 🧠 Round 1A – PDF Outline Extractor

## 🔍 Overview

In this phase, we build a lightweight and efficient **PDF structure extractor** that processes documents to extract:

- The document **title**
- Headings structured as **H1, H2, H3**
- Associated **page numbers**

This outline serves as a foundational layer for further document understanding tasks (like ranking or summarization in later rounds).

---

## 🚀 What It Does

Given a folder of PDF files (`/input`), the system:

1. Opens each PDF using **PyMuPDF** (`fitz`)
2. Analyzes **font sizes** on each page
3. Classifies text lines into heading levels based on relative font size:
   - Largest font → `H1`
   - Next smaller font → `H2`
   - Next smaller font → `H3`
4. Outputs a JSON structure per file with:
   ```json
   {
     "title": "My PDF Title",
     "outline": [
       { "level": "H1", "text": "Introduction", "page": 1 },
       { "level": "H2", "text": "Overview", "page": 2 }
     ]
   }
   ```

---

## 🛠️ Technologies Used

| Component        | Purpose                           |
|------------------|-----------------------------------|
| **Python 3.10**  | Core programming language         |
| **PyMuPDF (fitz)** | Text and font extraction from PDFs |
| **Docker**       | Environment packaging & isolation |

---

## 🧱 Project Structure

```
Challenge_1A/
├── main.py              # Script to extract outline from PDFs
├── Dockerfile              # Docker build script
├── utils/
│   └── extractor.py        # Logic for heading detection
├── input/                  # Folder with input PDF files
├── output/                 # Output JSONs will be saved here
```

---

## 🐳 How to Use (with Docker)

### 🧰 1. Build the Docker image

```bash
docker build --platform linux/amd64 -t pdfintelligence_1a:submission .
```

### ▶️ 2. Run the container

```bash
docker run --rm -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" --network none pdfintelligence_1a:submission
```

- PDF files go in the `input/` folder
- Extracted JSON files appear in `output/` folder

---

## 📦 Sample Output

```json
{
  "title": "Investment Fundamentals",
  "outline": [
    { "level": "H1", "text": "Chapter 1: Basics", "page": 1 },
    { "level": "H2", "text": "What is Investment?", "page": 2 },
    { "level": "H3", "text": "Risk vs Return", "page": 3 }
  ]
}
```

---

## 📌 Notes

- Does **not** rely on external models or internet
- All font-size analysis is done **offline**, directly from the PDF
- This output will be used in Round 1B for ranking and summarization

---




🔎 Round 1B – Intelligent Section Extractor & Ranker
---
📘 Overview
This project enhances the outlines extracted in Round 1A by ranking the most relevant sections of a collection of PDF documents based on a specific persona and a job-to-be-done.

It acts as a foundational component of a smart document analysis engine — surfacing the most meaningful and contextually appropriate parts of the content, especially for use cases like financial analysis, education, research, and more.
---

1. 📂 Accepts multiple PDFs from the user  
2. 🔍 Extracts section-wise outlines (headings + subheadings)  
3. 🧠 Ranks the sections based on relevance to the persona’s job by scores
4. 📄 Extracts full text from top-ranked pages  
5. ✍️ Summarizes the extracted text using NLP  
6. 📦 Returns a clean JSON file of the final extracted + summarized data  

---

⚙️ How to Use

📌 Step 1: Prepare Your Inputs

- Place your PDF files inside the `input/` folder  
- Update `config.json` with your persona and job-to-be-done:
- For Example :

```json
{
  "persona": "Investment Analyst",
  "job_to_be_done": "analyze trends in R&D spending across companies"
}
```

---

🐳 Step 2: Run with Docker (Recommended)

> This allows completely **offline usage** without needing model downloads later

🔨 Build the Docker image:

```bash
docker build -t pdfintelligence_1b:submission .
```

🚀 Run the container:

```bash
docker run --rm -v "%cd%/input:/app/input" -v "%cd%/output:/app/output" --network none pdfintelligence_1b:submission
```

---

🛠️ How It Works (Architecture Overview)

```The solution follows a modular pipeline:```

📑 1. Outline Extraction (Extractor Module)
- Library: `PyMuPDF`
- Function: Extracts the title and hierarchical headings (H1, H2, H3) from each PDF.
- Output: JSON structure of the document's outline with page numbers.

🔎 2. Semantic Relevance Ranking (Ranker Module)
- Library: `sentence-transformers`
- Model: `all-MiniLM-L6-v2`
- Function:
  - Converts job description and all extracted headings into semantic embeddings
  - Uses cosine similarity to rank relevance
  - Selects the top N headings most relevant to the persona's goal

🧠 3. Paragraph Extraction
- Tool: `PyMuPDF`
- Function: Extracts full text from the relevant pages associated with ranked headings

✍️ 4. NLP Summarization (Summarizer Module)
- Library: `transformers`
- Model: `t5-small`
- Function:
  - Uses encoder-decoder architecture to generate abstractive summaries
  - Helps condense dense content into a few key lines

---

## 📦 Output

```The final output is a single JSON file that contains:```
- Persona and job
- Timestamp
- Ranked and summarized sections (title, page, relevance score, and refined text)

### Sample Output
```json
{
  "persona": "Investment Analyst",
  "job_to_be_done": "analyze trends in R&D spending across companies",
  "processing_timestamp": "2025-07-23",
  "extracted_sections": [
    {
      "document": "inv.pdf",
      "page_number": 4,
      "heading": "Research and Development Expenditure",
      "score": 0.88,
      "rank": 1,
      "refined_text": "This section discusses the recent increase in R&D investment across major firms..."
    }
  ]
}
```

---

## 📁 Folder Structure

```
Challenge1B/
│
├── main.py                  # 🔁 Main orchestration script
├── config.json              # 🧩 Contains persona + job-to-be-done
├── requirements.txt         # 📦 Python dependencies
├── Dockerfile               # 🐳 For containerized execution
│
├── input/                   # 📥 Place input PDF files here
├── output/                  # 📤 Final JSON file
│
└── utils/                   # ⚙️ Modular utilities
    ├── extractor.py         # Extracts headings from PDFs
    ├── ranker.py            # Ranks sections using embeddings
    └── summarizer.py        # Summarizes long paragraphs
```

---

## ⚙️ Technologies Used

| Component       | Technology / Library                |
|----------------|-------------------------------------|
| PDF Parsing     | PyMuPDF (`fitz`)                    |
| Embeddings      | `sentence-transformers`, MiniLM     |
| NLP Model       | `transformers`, `t5-small`          |
| Summarization   | Abstractive via encoder-decoder     |
| Ranking         | Cosine similarity in vector space   |
| Containerization| Docker (Python 3.10-slim)           |

---

## 🧪 Tested On

- ✔️ Windows 11 + Docker Desktop
- ✔️ Python 3.10 (in Docker)
- ✔️ Sample investment domain PDFs
---

Note:

``` There is no rule that there should be involvement of every PDF in output JSON file  which was provided by user , Some may involve some may not according to there ranks and score , our backend system aims to produce most relevent matter from the provided PDF's which is useful for the user according to their persona and job to be done.
```  

---

## 🙌 Author

Built with purpose and passion for Adobe Hackathon  
By: **Lokeswari Pindi** & **Finny Novel Balagam**
