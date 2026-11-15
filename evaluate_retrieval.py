"""Run the required k=1,3,5 retrieval comparison and chunking experiment.
This script measures evidence retrieval. Answer correctness is intentionally left
for human review in the CSV; it is not fabricated by an automatic keyword score.
"""
import csv
from pathlib import Path
from rag import rebuild_index, retrieve

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)

CASES = [
    ("E1", "What are the help desk opening hours?", ["01_company_overview.md"], ["Sunday"]),
    ("E2", "What is the tuition for Web Development?", ["02_programs_and_services.md"], ["PKR 22,000"]),
    ("E3", "What is the total first payment for Web Development and when is tuition due?", ["02_programs_and_services.md", "03_current_student_policy.md"], ["PKR 22,000", "PKR 2,000", "5 calendar days"]),
    ("E4", "Compare the old and current refund percentage and notice period.", ["03_current_student_policy.md", "04_archived_student_policy.md"], ["50%", "80%", "5 calendar days", "7 calendar days"]),
    ("E5", "What should a student do if a class resource is missing?", ["05_operations_faq_and_test_notes.md"], ["Student Support"]),
    ("E6", "What percentage sibling discount is offered?", ["05_operations_faq_and_test_notes.md"], ["not specified"]),
]

def run():
    rows = []
    for size, overlap, label, questions in [
        (850, 140, "baseline", CASES),
        (500, 80, "smaller_chunks", CASES[:3]),
    ]:
        rebuild_index(size, overlap)
        for case_id, question, expected_files, expected_terms in questions:
            for k in (1, 3, 5) if label == "baseline" else (5,):
                hits = retrieve(question, k=k, chunk_size=size, chunk_overlap=overlap)
                found_files = sorted(set(x["metadata"]["source_file"] for x in hits))
                joined = "\n".join(x["text"] for x in hits).lower()
                required_found = all(any(f == hit for hit in found_files) for f in expected_files)
                terms_found = all(term.lower() in joined for term in expected_terms)
                irrelevant = [f for f in found_files if f not in expected_files]
                rows.append({
                    "experiment": label, "chunk_size": size, "chunk_overlap": overlap,
                    "question_id": case_id, "question": question, "k": k,
                    "expected_sources": ";".join(expected_files),
                    "retrieved_sources": ";".join(found_files),
                    "required_source_files_retrieved": "yes" if required_found else "no",
                    "expected_terms_present": "yes" if terms_found else "no",
                    "irrelevant_source_files": ";".join(irrelevant),
                    "irrelevant_evidence_retrieved": "review required" if irrelevant else "no by filename check",
                    "final_answer_correct": "MANUAL REVIEW REQUIRED",
                    "review_notes": "Inspect retrieved chunks and run the app; record actual answer correctness. Do not treat source filename match alone as proof.",
                })
    path = OUT / "retrieval_experiment_results.csv"
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    print(f"Wrote {len(rows)} experiment rows to {path}")
    print("Note: the smaller-chunk run leaves the index using 500/80 settings. Rebuild default index with: python ingest.py")

if __name__ == "__main__":
    run()
