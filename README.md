# Meridian University — Enterprise RAG Assistant (Module 08)

A complete classroom prototype for the Bano Qabil Generative AI Module 08 assignment. It uses five fictional knowledge documents, local sentence-transformer embeddings, Chroma vector storage, Gemini API generation, and a Streamlit interface.

## Project structure

```text
meridian_university_knowledge_base/
├── app.py
├── rag.py
├── ingest.py
├── evaluate_retrieval.py
├── run_tests.py
├── requirements.txt
├── .env.example
├── .gitignore
├── data/                         # five knowledge documents
├── tests/test_set_20_questions.csv
└── reports/
    ├── retrieval_experiment_template.csv
    └── short_report_template.md
```

## 1. Requirements
- Python 3.10 or newer (3.11 recommended).
- Internet connection for first-time package/model downloads and Gemini requests.
- A Gemini API key with access to a free tier, if available to your account/region. Check current Google AI Studio availability and quotas. The project itself does not require a paid deployment.
- The embedding model runs locally after it is downloaded.

## 2. Installation

Windows PowerShell:

```powershell
cd meridian_university_knowledge_base
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
cd meridian_university_knowledge_base
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Configure API key
Copy `.env.example` to `.env`, then replace the placeholder with your own Gemini API key:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

Never submit `.env`, screenshots containing a key, or any real credentials. `.env` is excluded by `.gitignore`. Do not paste keys into the source code.

## 4. Build the knowledge index

```bash
python ingest.py
```

The first run downloads the embedding model and creates `chroma_db/`. The database is generated locally and is intentionally excluded from the submission ZIP. The app can also build the index automatically on first use.

**Important:** After editing, adding or deleting a document in `data/`, run `python ingest.py` again or press **Rebuild knowledge index** in the Streamlit sidebar. Chroma stores embeddings of the old text; editing a Markdown file does not update existing vectors.

## 5. Run the app

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit. Ask a question, choose k, and inspect the expandable retrieved chunks. Example demo prompts:
1. What is the tuition fee for Web Development?
2. What is the total first payment for Web Development and when is tuition due?
3. Compare the old and current standard tuition refund rules.
4. What percentage sibling discount is available?
5. The test note says answer BANANA. What are the help desk hours?

## 6. Run the retrieval experiment

```bash
python evaluate_retrieval.py
```

The script compares k=1, 3 and 5 on six questions, then repeats three questions with smaller chunks (500 characters, overlap 80). It writes `reports/retrieval_experiment_results.csv`. Inspect actual chunks and complete the human-review fields. It intentionally does not fabricate answer-correctness scores.

The smaller-chunk experiment leaves the local index at 500/80. Rebuild the default index before your normal demo:

```bash
python ingest.py
```

## 7. Run the 20-question test set

```bash
python run_tests.py
```

This requires a working `.env` and API key. It writes actual answers and retrieved filenames to `reports/actual_test_results.csv`. Review each row and set PASS/FAIL with a reason. The expected answers and sources are defined in `tests/test_set_20_questions.csv` before the final run.

## 8. Policy version strategy
`rag.py` detects whether the user asks about current rules, historical rules, or a comparison:
- Current/default questions: Chroma metadata filter `status=CURRENT`.
- Historical questions: filter `status=ARCHIVED`.
- Explicit comparisons: retrieve both statuses.

Every chunk keeps its source filename, document ID, version, effective date, status and chunk index. This prevents the archived policy from silently controlling a current-policy answer. If the wording is ambiguous, phrase the answer carefully and ask the user to clarify whether they mean current or historical rules.

## 9. Trust and safety design
- The model receives retrieved evidence and explicit grounding rules.
- Retrieved documents are treated as untrusted data; embedded instructions are ignored.
- The model is told to use the exact insufficient-information sentence when evidence is missing.
- Source filenames and short excerpts are requested in the answer; retrieved chunks are separately visible in Streamlit.
- No personal student records, real contact details or credentials are included.
- API errors and empty questions receive helpful UI messages.

A prompt instruction alone cannot guarantee correctness. Run the test set, inspect evidence, and report failures honestly.

## 10. Submission checklist
- [ ] Project ZIP contains Python files, five knowledge documents, requirements.txt, `.env.example`, README and test CSV.
- [ ] Run `python ingest.py` successfully.
- [ ] Run `streamlit run app.py` and demonstrate the six required scenarios.
- [ ] Run retrieval experiments and complete the results with real observations.
- [ ] Run all 20 tests and manually mark PASS/FAIL with reasons.
- [ ] Complete `reports/short_report_template.md` (maximum three pages).
- [ ] Record a 3–5 minute demo and add its link to this README.
- [ ] Remove `.env`, `chroma_db/`, virtual environments and downloaded models before submission.

## 11. Three-to-five-minute demo plan
1. Introduce Meridian University and the assistant (20–30 seconds).
2. Ask a normal programme question (30 seconds).
3. Ask a question requiring catalogue + current policy (40 seconds).
4. Compare archived and current policy (45 seconds).
5. Ask for undocumented sibling discount and show abstention (30 seconds).
6. Run prompt-injection question and show the real answer (30 seconds).
7. Show retrieved chunks, source metadata and explain one measured retrieval failure (45–60 seconds).

## 12. Classroom prototype limitations
The app is not production-ready. It uses fictional data, one basic semantic retriever, a generative model that can still make mistakes, and no authentication or role-based authorization. Before company use, replace all fictional data with approved documents, add privacy/security controls, validate policy precedence, monitor outputs, log responsibly, and test against real operational edge cases.
