## Project Goal
***CampusFlow 
CampusFlow is a lightweight, command-line ticket management system designed for university IT departments. It streamlines ticket submission, prioritizes issues based on urgency and user impact, enforces valid status workflows, tracks task assignments, and persists all operational data to JSON storage.

Team & Contribution Summary
## Engineer A (Ticket Management & Validation Lead)
Role: Designed the core ticket model, validation rules, ticket creation logic, and ID generation (generate_next_id).

Key Contributions: Implemented ticket input sanitation, priority calculation based on impact/urgency, list/dictionary data mapping, and ticket listing/viewing CLI views.

## Engineer B (Workflow, Storage & Reporting Lead)
Role: Architected workflow status transitions, queue sorting, storage persistence, and analytical reporting.

Key Contributions: Implemented valid status guards (e.g., open $\rightarrow$ in_progress $\rightarrow$ resolved), staff assignment logic, work queue sorting algorithm, JSON file storage handlers (storage.py), and the automated unit test suite.

## Environment & Setup Instructions
Prerequisites
**Python Version: Python 3.12+Dependencies: Standard library only (no external pip dependencies required).

## Installation & Setup
1. Clone the Repository:
git clone https://github.com/your-org/campusflow.git
cd campusflow

2. Verify Python Installation:
python3 --version
3. Verify Environment Pathing:
Ensure PYTHONPATH points to the project root directory when running modules or tests.

## Running the CLI Application
Launch the main CLI application from the root directory:python3 main.py
Main Menu Options
When prompted, select options 1 through 7:
1. Create Ticket (F1): Interactive prompt to create a new ticket with title, category, urgency, and affected user count.
2. List All / View Ticket (F2): Displays a summary table of all tickets or detailed view of a single ticket by ID.
3. Assign Ticket: Assigns an unassigned ticket to an IT support staff member.
4. Update Status Workflow: Transitions a ticket's status adhering to strict system guards.
5. View Work Queue: Displays tickets prioritized by urgency, affected user count, and submission date.
6. View Reports: Displays operational summary metrics (e.g., total open tickets, breakdown by category, average resolution state).
7. Exit & Save: Persists current state to disk and exits the program safely.
## Running Tests
CampusFlow uses Python's built-in unittest framework.
Run All Unit Tests
Run the entire test suite from the project root using test discovery:
PYTHONPATH=. python3 -m unittest discover -s tests -v

## Test Suite Coverage
**tests/test_workflow.py: Validates status state transitions, invalid status transition prevention, ticket assignment, and work queue priority ordering.
**tests/test_storage.py: Validates JSON file loading, saving, handling missing files, handling malformed data, and ensuring schema consistency on read/write cycles.
## Priority & Workflow Rules
1. Priority Calculation Matrix
Ticket priority is derived from Urgency and Affected Users:
**Urgency Levels: low, medium, high
**Priority scoring ensures high-impact and high-urgency tickets bubble up to the top of the Work Queue.
2. Status Workflow GuardsTickets must progress through lifecycle states in a strict sequence:Open, in progress, resolved and closed
### Rules:
**A ticket cannot skip directly from Open to Closed or Resolved.
**A ticket must be assigned to a staff member before transitioning to In Progress.
**Reopening a Resolved ticket sends it back to In Progress.
## Data Persistence & Resetting Data
File Location
All ticket records are automatically saved to:
data/tickets.json

### How to Start Fresh
To clear all data and start with a clean state:
1. Remove the JSON file:rm data/tickets.json
2. Relaunch the CLI application (python3 main.py). The system will automatically detect the missing file and initialize a new empty database.

## Known Limitations & Future ImprovementsLimitations

**Single-user CLI: Does not currently support simultaneous concurrent multi-user sessions or network-based authentication.*Storage Scalability: JSON-file storage is suitable for small-scale deployment but lacks indexing for thousands of records.
### Future Improvements
Database Migration: Replace tickets.json with SQLite / PostgreSQL for transactional persistence.

REST API: Wrap the workflow engines in a FastAPI backend with a React web interface.

Automated Email Notifications: Notify users when their ticket status changes or when staff members are assigned.
## Name
Samuel Ojedo
Nnenna Uzoezie
