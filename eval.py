from ask import answer_question
import time
# Golden dataset: question + keywords that MUST appear in a correct answer.
# Keep these easy to verify by eye — the goal is a quick sanity check, not perfection.
GOLDEN_SET = [
    {
        "question": "What is her name?",
        "expected_keywords": ["Sri Navya Kundula"],
    },
    {
        "question": "What did she study?",
        "expected_keywords": ["Technology", "Shri Vishnu"],
    },
    {
        "question": "What AI project did she build?",
        "expected_keywords": ["Netflix GPT"],
    },
    {
        "question": "What company did she work at as a Software Developer?",
        "expected_keywords": ["AT&T"],
    },
    {
        "question": "What model did she build at Quadrant Resources?",
        "expected_keywords": ["Named Entity Recognition", "NER"],
    },
    {
        "question": "What is her work authorization status?",
        "expected_keywords": ["H4 EAD"],
    },
    {
        # Deliberately unanswerable — should trigger the guardrail, NOT hallucinate
        "question": "What is the capital of France?",
        "expected_keywords": ["don't have enough information"],
    },
]


def run_eval():
    passed = 0
    results = []

    for case in GOLDEN_SET:
        answer, sources = answer_question(case["question"])
        answer_lower = answer.lower()

        hit = any(kw.lower() in answer_lower for kw in case["expected_keywords"])
        status = "PASS" if hit else "FAIL"
        if hit:
            passed += 1

        results.append((status, case["question"], answer))
        print(f"[{status}] {case['question']}")
        print(f"       -> {answer[:150]}")
        print()
        time.sleep(2)
    print(f"\nScore: {passed}/{len(GOLDEN_SET)} passed")
    return results


if __name__ == "__main__":
    run_eval()