# Meridian University RAG — Short Report (maximum 3 pages)

## 1. Business use case
Meridian University is a fictional skills-training institution. The assistant supports prospective students, enrolled learners, instructors and administrators with documented programme, fee, admissions, policy and support questions. It is a classroom prototype and must not make official decisions or expose personal records.

## 2. Knowledge base and pipeline
Five Markdown documents contain the institution overview, eight-programme catalogue, current policy v2.0, archived policy v1.0, and operations/FAQs. Policy documents include version, effective date and status metadata. The pipeline loads Markdown, splits it with `RecursiveCharacterTextSplitter`, embeds chunks with `sentence-transformers/all-MiniLM-L6-v2`, stores vectors and metadata in Chroma, retrieves relevant chunks, and sends evidence plus the question to Gemini through the Google GenAI SDK. Streamlit displays the answer, source filenames, excerpts and expandable retrieved chunks.

Policy selection is coded in `rag.py`: current questions filter to CURRENT chunks, historical questions filter to ARCHIVED chunks, and explicit comparisons retrieve both. Retrieved text is treated as untrusted evidence, not instructions. Insufficient evidence must produce the exact abstention sentence.

## 3. Retrieval experiment
Run `python evaluate_retrieval.py`. It compares k=1, k=3 and k=5 on six unchanged questions, then repeats three questions using chunk size 500 / overlap 80 instead of 850 / 140. Complete `retrieval_experiment_results.csv` after execution and inspect the actual retrieved text. Do not claim a setting is best until the run has been performed. More chunks may help two-document questions but can add irrelevant or archived-policy evidence. Record the best setting and examples from your own output here.

## 4. Failures and limitations
Record one real failure from your experiment, the question, retrieved chunks, why the evidence was insufficient or noisy, and the change you tested. Known limitations include semantic retrieval misses, model paraphrasing, API/network failure, and the fact that human review is needed to score answer correctness. The project does not contain verified real-world policies or student records.

## 5. Improvements and production gap
Possible next improvements include hybrid keyword + semantic retrieval, reranking, automated regression tests, role-based access, policy approval workflow, monitoring, audit logs, privacy/security review and a verified source-of-truth process. Editing Markdown alone does not update vectors already stored in Chroma; rebuild the index after every knowledge-base update.
