
import re
import unicodedata

from Rag_pipeline import generate_answer


def normalize_text(text):
    """Normalize Unicode characters and whitespace before comparison."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u202f", " ").replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


test_cases = [
    {
        "question": "What was Freshworks' Q2 2026 revenue?",
        "expected": ["237.4 million"],
        "type": "positive",
    },
    {
        "question": "What was Freshworks' Q1 2026 revenue?",
        "expected": ["228.6 million"],
        "type": "positive",
    },
    {
        "question": "What was Freshworks' full year 2025 revenue?",
        "expected": ["838.8 million"],
        "type": "positive",
    },
    {
        "question": "Who is Ryan Manning?",
        "expected": ["Chief Product and Technology Officer"],
        "type": "positive",
    },
    {
        "question": "When will Ryan Manning join Freshworks?",
        "expected": ["August 10"],
        "type": "positive",
    },
    {
        "question": "What is Freddy AI?",
        "expected": ["AI-powered platform", "intelligent assistance"],
        "type": "positive",
    },
    {
        "question": "What was Microsoft's 2026 revenue?",
        "expected": ["I don't know"],
        "type": "negative",
    },
    {
        "question": "Who is the CEO of Apple?",
        "expected": ["I don't know"],
        "type": "negative",
    },
]


passed = 0
failed = 0
errors = 0

print("\n===== RAG GENERATION EVALUATION =====")

for test in test_cases:
    question = test["question"]

    print("\n" + "=" * 65)
    print("Question:", question)

    try:
        answer, sources = generate_answer(question)

        print("Answer:", answer)
        print("Retrieved chunks:", len(sources))

        normalized_answer = normalize_text(answer)
        expected = [
            normalize_text(item)
            for item in test["expected"]
        ]

        if test["type"] == "positive":
            success = any(
                item in normalized_answer
                for item in expected
            )
        else:
            # A negative test passes only when the model explicitly
            # says it cannot answer from the supplied documents.
            success = (
                "i don't know based on the provided documents"
                in normalized_answer
            )

        if success:
            passed += 1
            print("Result: PASS")
        else:
            failed += 1
            print("Result: FAIL")
            print("Expected keyword(s):", test["expected"])

    except Exception as error:
        errors += 1
        print("Result: ERROR")
        print(f"{type(error).__name__}: {error}")


total = len(test_cases)

print("\n" + "=" * 65)
print("FINAL GENERATION RESULTS")
print("=" * 65)
print(f"Passed: {passed}/{total}")
print(f"Failed: {failed}/{total}")
print(f"Errors: {errors}/{total}")
print(f"Pass rate: {passed / total * 100:.1f}%")
