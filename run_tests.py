"""Run all 20 assignment test questions through the live RAG app.
Requires GEMINI_API_KEY in .env. Results are written with actual answers and
retrieved filenames. Human pass/fail review is intentionally required.
"""
import csv
from pathlib import Path
from rag import answer_question

ROOT = Path(__file__).resolve().parent
src = ROOT / "tests" / "test_set_20_questions.csv"
dst = ROOT / "reports" / "actual_test_results.csv"

def main():
    with src.open(encoding="utf-8-sig", newline="") as f:
        tests = list(csv.DictReader(f))
    output = []
    for row in tests:
        print(f"Running {row['test_id']}: {row['question']}")
        try:
            result = answer_question(row["question"], k=5)
            actual = result["answer"]
            sources = ";".join(sorted(set(x["metadata"]["source_file"] for x in result["sources"])))
            error = ""
        except Exception as exc:
            actual, sources, error = "", "", str(exc)
        output.append({**row, "actual_answer": actual, "actual_sources": sources,
                       "runtime_error": error, "pass_fail": "MANUAL REVIEW REQUIRED",
                       "review_reason": "Check factual correctness, source support, abstention and policy version."})
    with dst.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=output[0].keys())
        writer.writeheader(); writer.writerows(output)
    print(f"Saved actual run results to {dst}")

if __name__ == "__main__":
    main()
