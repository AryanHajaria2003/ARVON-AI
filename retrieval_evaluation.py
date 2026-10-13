from retrieval import hybrid_search
import math


test_cases = [

    # -------------------------
    # Financial
    # -------------------------

    {
        "question": "What was Freshworks' Q2 2026 revenue?",
        "expected": "$237.4 million",
        "source_keyword": "Earnings-Release-Q2-2026",
        "type": "positive"
    },

    {
        "question": "What was Freshworks' Q1 2026 revenue?",
        "expected": "$228.6 million",
        "source_keyword": "Earnings-Release-Q1-2026",
        "type": "positive"
    },

    {
        "question": "What was Freshworks' Q4 2025 revenue?",
        "expected": "$222.7 million",
        "source_keyword": "Earnings",
        "type": "positive"
    },

    {
        "question": "What was Freshworks' full year 2025 revenue?",
        "expected": "$838.8 million",
        "source_keyword": "Earnings",
        "type": "positive"
    },


    # -------------------------
    # People / Company
    # -------------------------

    {
        "question": "Who is Ryan Manning?",
        "expected": "Chief Product and Technology Officer",
        "source_keyword": "Ryan",
        "type": "positive"
    },

    {
        "question": "When will Ryan Manning join Freshworks?",
        "expected": "August 10",
        "source_keyword": "Ryan",
        "type": "positive"
    },


    # -------------------------
    # Freddy AI
    # -------------------------

    {
        "question": "What is Freddy AI?",
        "expected": "conversational AI",
        "source_keyword": "Freddy",
        "type": "positive"
    },

    {
        "question": "Which channels does Freddy AI support?",
        "expected": "Microsoft Teams",
        "source_keyword": "Freddy",
        "type": "positive"
    },


    # -------------------------
    # Product / Freshservice
    # -------------------------

    {
        "question": "What is AI Agent Studio?",
        "expected": "no-code",
        "source_keyword": "AI Agent Studio",
        "type": "positive"
    },

    {
        "question": "What does Freshservice help organizations manage?",
        "expected": "IT",
        "source_keyword": "Freshservice",
        "type": "positive"
    },


    # -------------------------
    # Negative / Out-of-scope
    # -------------------------

    {
        "question": "What was Microsoft's 2026 revenue?",
        "expected": "I don't know",
        "source_keyword": "",
        "type": "negative"
    },

    {
        "question": "Who is the CEO of Apple?",
        "expected": "I don't know",
        "source_keyword": "",
        "type": "negative"
    }
]


def dcg(relevance):

    score = 0

    for rank, rel in enumerate(relevance, 1):

        score += rel / math.log2(rank + 1)

    return score


def ndcg(relevance):

    actual = dcg(relevance)

    ideal = sorted(relevance, reverse=True)

    ideal_score = dcg(ideal)

    if ideal_score == 0:
        return 0

    return actual / ideal_score


def evaluate_positive(test, results):

    expected = test["expected"].lower()
    source_keyword = test["source_keyword"].lower()

    relevant = []

    for doc in results:

        content = doc.page_content.lower()

        source = doc.metadata.get(
            "source",
            ""
        ).lower()

        answer_match = expected in content

        source_match = (
            source_keyword != ""
            and source_keyword in source
        )

        if answer_match or source_match:
            relevant.append(1)

        else:
            relevant.append(0)

    # -------------------------
    # Hit
    # -------------------------

    h5 = 1 if any(relevant[:5]) else 0
    h10 = 1 if any(relevant[:10]) else 0

    # -------------------------
    # Precision
    # -------------------------

    p5 = sum(relevant[:5]) / 5
    p10 = sum(relevant[:10]) / 10

    # -------------------------
    # Recall
    # -------------------------

    total_relevant = sum(relevant)

    if total_relevant > 0:

        r5 = sum(relevant[:5]) / total_relevant
        r10 = sum(relevant[:10]) / total_relevant

    else:

        r5 = 0
        r10 = 0

    # -------------------------
    # MRR
    # -------------------------

    rank_found = None

    for rank, value in enumerate(relevant, 1):

        if value == 1:

            rank_found = rank
            break

    if rank_found:

        reciprocal_rank = 1 / rank_found

    else:

        reciprocal_rank = 0

    # -------------------------
    # nDCG
    # -------------------------

    n5 = ndcg(relevant[:5])
    n10 = ndcg(relevant[:10])

    return {
        "hit5": h5,
        "hit10": h10,
        "precision5": p5,
        "precision10": p10,
        "recall5": r5,
        "recall10": r10,
        "mrr": reciprocal_rank,
        "ndcg5": n5,
        "ndcg10": n10,
        "rank": rank_found
    }


def evaluate_negative(test, results):

    expected = test["expected"].lower()

    # Check whether retrieved chunks actually
    # contain the expected "I don't know" answer.
    #
    # Normally they should NOT.
    answer_found = False

    for doc in results:

        content = doc.page_content.lower()

        if expected in content:

            answer_found = True
            break

    return {
        "answer_found": answer_found
    }


def evaluate_retrieval():

    hit_5 = []
    hit_10 = []

    precision_5 = []
    precision_10 = []

    recall_5 = []
    recall_10 = []

    reciprocal_ranks = []

    ndcg_5 = []
    ndcg_10 = []

    negative_pass = []

    for test in test_cases:

        question = test["question"]
        test_type = test["type"]

        results = hybrid_search(question, k=10)

        print("\n" + "-" * 60)
        print("Question:", question)

        # =====================================================
        # POSITIVE QUERY
        # =====================================================

        if test_type == "positive":

            metrics = evaluate_positive(
                test,
                results
            )

            hit_5.append(metrics["hit5"])
            hit_10.append(metrics["hit10"])

            precision_5.append(
                metrics["precision5"]
            )

            precision_10.append(
                metrics["precision10"]
            )

            recall_5.append(
                metrics["recall5"]
            )

            recall_10.append(
                metrics["recall10"]
            )

            reciprocal_ranks.append(
                metrics["mrr"]
            )

            ndcg_5.append(
                metrics["ndcg5"]
            )

            ndcg_10.append(
                metrics["ndcg10"]
            )

            if metrics["rank"]:

                print(
                    "Relevant chunk rank:",
                    metrics["rank"]
                )

            else:

                print(
                    "Relevant chunk: NOT FOUND"
                )

            print("Hit@5:", metrics["hit5"])
            print("Hit@10:", metrics["hit10"])

            print(
                "Precision@5:",
                round(metrics["precision5"], 3)
            )

            print(
                "Precision@10:",
                round(metrics["precision10"], 3)
            )

            print(
                "Recall@5:",
                round(metrics["recall5"], 3)
            )

            print(
                "Recall@10:",
                round(metrics["recall10"], 3)
            )

            print(
                "MRR:",
                round(metrics["mrr"], 3)
            )

            print(
                "nDCG@5:",
                round(metrics["ndcg5"], 3)
            )

            print(
                "nDCG@10:",
                round(metrics["ndcg10"], 3)
            )

        # =====================================================
        # NEGATIVE QUERY
        # =====================================================

        else:

            negative = evaluate_negative(
                test,
                results
            )

            passed = not negative["answer_found"]

            negative_pass.append(
                1 if passed else 0
            )

            if passed:

                print(
                    "Negative test: PASS"
                )

            else:

                print(
                    "Negative test: FAIL"
                )

            print(
                "Expected behavior:",
                "No answer found in documents"
            )

    # =========================================================
    # FINAL RESULTS
    # =========================================================

    print("\n")
    print("=" * 60)
    print("              RETRIEVAL EVALUATION")
    print("=" * 60)

    print("\nPositive Queries")

    print(
        "Hit@5:",
        round(
            sum(hit_5) / len(hit_5),
            3
        )
    )

    print(
        "Hit@10:",
        round(
            sum(hit_10) / len(hit_10),
            3
        )
    )

    print(
        "Precision@5:",
        round(
            sum(precision_5) /
            len(precision_5),
            3
        )
    )

    print(
        "Precision@10:",
        round(
            sum(precision_10) /
            len(precision_10),
            3
        )
    )

    print(
        "Recall@5:",
        round(
            sum(recall_5) /
            len(recall_5),
            3
        )
    )

    print(
        "Recall@10:",
        round(
            sum(recall_10) /
            len(recall_10),
            3
        )
    )

    print(
        "MRR:",
        round(
            sum(reciprocal_ranks) /
            len(reciprocal_ranks),
            3
        )
    )

    print(
        "nDCG@5:",
        round(
            sum(ndcg_5) /
            len(ndcg_5),
            3
        )
    )

    print(
        "nDCG@10:",
        round(
            sum(ndcg_10) /
            len(ndcg_10),
            3
        )
    )

    print("\nNegative Queries")

    print(
        "Negative test accuracy:",
        round(
            sum(negative_pass) /
            len(negative_pass),
            3
        )
    )


if __name__ == "__main__":

    evaluate_retrieval()