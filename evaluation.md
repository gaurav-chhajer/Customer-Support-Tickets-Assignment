# Part B1 - Evaluation of LLM Summaries

I used a 1-5 rubric to compare each LLM summary with its reference summary. The focus is on meaning: does it describe the right product and problem, keep the important context, and avoid unsupported claims? Different wording is fine if the meaning stays the same.

| Score | Meaning |
|-------|---------|
| 5 | Keeps all key facts without adding unsupported claims. |
| 4 | Keeps the main facts, with a small loss of precision or a minor unsupported addition. |
| 3 | Describes the problem correctly but leaves out one important detail. |
| 2 | Is broadly relevant but too vague, leaving out multiple important details. |
| 1 | Misrepresents the main problem or is unrelated to the reference. |

## Scores and reasoning

| Ticket | Score | Justification |
|--------|-------|---------------|
| T1 | 3/5 | The summary correctly names CloudSync and describes the login problem. However, it leaves out that the customer was locked out after resetting their password, which is important context. |
| T2 | 2/5 | "Sync is stuck" captures the general problem but leaves out both the product, CloudSync, and the fact that the sync hangs near completion. This makes it too vague to distinguish this ticket from other sync issues. |
| T3 | 4/5 | The summary names InvoicePro and correctly describes missing items in PDF exports. However, "items" is less specific than "invoice line items," and calling it a "bug" adds a diagnosis that the reference does not explicitly establish. These are minor issues because the main problem is still clear. |
