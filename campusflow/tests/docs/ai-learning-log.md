# AI Learning Log

## Fellow 1: [Nnenna Uzoezie]
### Interaction #1 — Custom Exceptions vs standard ValueError
- **Problem:** Unsure how to cleanly communicate validation failures without breaking execution.
- **AI Prompt:** "What are the trade-offs in Python between defining custom exception classes vs using built-in ValueError for input validation?"
- **Experiment & Verification:** Tested raising ValueError and catching it specifically inside `main.py`. Confirmed clean user message display.

## Fellow 2: [Samuel Ojedo]
### Interaction #1 — Sorting via Tuples in Python
- **Problem:** Needed to sort by priority rank string and numeric ID simultaneously.
- **AI Prompt:** "How does key function tuple return work in sorted() for multi-criteria ordering?"
- **Experiment & Verification:** Executed a tiny experiment comparing `(priority_rank, numeric_id)` tuple pairs. Verified tie-breaker functionality in `test_workflow.py`.