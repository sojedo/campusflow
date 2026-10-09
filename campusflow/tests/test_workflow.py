cat << 'EOF' > tests/test_workflow.py
import unittest
from campusflow.workflow import assign_ticket, update_status, get_work_queue
from campusflow.reports import generate_reports


class TestWorkflowAndReports(unittest.TestCase):

    def setUp(self):
        self.tickets = [
            {"id": "T001", "priority": "low", "status": "open", "assigned_to": None},
            {"id": "T002", "priority": "critical", "status": "open", "assigned_to": None},
            {"id": "T003", "priority": "critical", "status": "open", "assigned_to": None},
        ]

    def test_unassigned_in_progress_rejection(self):
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")

    def test_valid_lifecycle(self):
        assign_ticket(self.tickets, "T001", "Alice")
        update_status(self.tickets, "T001", "in_progress")
        self.assertEqual(self.tickets[0]["status"], "in_progress")

        update_status(self.tickets, "T001", "resolved")
        self.assertEqual(self.tickets[0]["status"], "resolved")

    def test_resolved_ticket_modification_rejected(self):
        assign_ticket(self.tickets, "T001", "Alice")
        update_status(self.tickets, "T001", "in_progress")
        update_status(self.tickets, "T001", "resolved")

        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "in_progress")

    def test_work_queue_sorting_and_tie_break(self):
        queue = get_work_queue(self.tickets)
        ordered_ids = [t["id"] for t in queue]
        self.assertEqual(ordered_ids, ["T002", "T003", "T001"])

    def test_empty_reports_handling(self):
        report = generate_reports([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["status_breakdown"]["open"], 0)


if __name__ == "__main__":
    unittest.main()
EOF