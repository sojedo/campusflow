# Design Decisions & Contracts

## Ticket Data Schema
All modules communicate using standard Python dictionary objects:
- `id` (str): Sequential identifier (`T001`, `T002`, ...).
- `title` (str): Non-empty string.
- `category` (str): `Network`, `Hardware`, `Software`, or `Other`.
- `urgency` (str): `low`, `medium`, or `high`.
- `affected_users` (int): Positive integer $> 0$.
- `priority` (str): Calculated as `critical`, `high`, `medium`, or `low`.
- `status` (str): `open`, `in_progress`, or `resolved`.
- `assigned_to` (str or None): Support staff name or `None`.

## Exception Contracts
Validation failures throw standard `ValueError` or `KeyError` exceptions. The CLI (`main.py`) catches these to display clear user messages without crashing.