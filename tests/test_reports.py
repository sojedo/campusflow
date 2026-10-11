import unittest


def generate_reports(tickets: list) -> dict:
    report = {
        "total": len(tickets),
        "status_breakdown": {"open": 0, "in_progress": 0, "resolved": 0},
        "priority_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
    }

    for ticket in tickets:
        st = ticket.get("status")
        pr = ticket.get("priority")
        if st in report["status_breakdown"]:
            report["status_breakdown"][st] += 1
        if pr in report["priority_breakdown"]:
            report["priority_breakdown"][pr] += 1

    return report


class TestGenerateReports(unittest.TestCase):

    def test_empty_tickets_list(self):
        """Should return zeroed-out counts when given an empty list."""
        result = generate_reports([])
        expected = {
            "total": 0,
            "status_breakdown": {"open": 0, "in_progress": 0, "resolved": 0},
            "priority_breakdown": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        }
        self.assertEqual(result, expected)

    def test_valid_tickets(self):
        """Should accurately count valid statuses and priorities."""
        sample_tickets = [
            {"status": "open", "priority": "critical"},
            {"status": "in_progress", "priority": "high"},
            {"status": "resolved", "priority": "low"},
            {"status": "open", "priority": "medium"},
        ]
        
        result = generate_reports(sample_tickets)
        
        self.assertEqual(result["total"], 4)
        self.assertEqual(result["status_breakdown"]["open"], 2)
        self.assertEqual(result["status_breakdown"]["in_progress"], 1)
        self.assertEqual(result["priority_breakdown"]["critical"], 1)
        self.assertEqual(result["priority_breakdown"]["low"], 1)

    def test_missing_keys_in_tickets(self):
        """Should safely ignore tickets missing 'status' or 'priority' keys without crashing."""
        malformed_tickets = [
            {"status": "open"},  
            {"priority": "high"},
            {"id": 101}
        ]
        
        result = generate_reports(malformed_tickets)
        
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["status_breakdown"]["open"], 1)
        self.assertEqual(result["priority_breakdown"]["high"], 1)
        self.assertEqual(result["status_breakdown"]["in_progress"], 0)

    def test_unexpected_or_invalid_values(self):
        """Should ignore values that don't match predefined breakdowns."""
        invalid_tickets = [
            {"status": "unknown_status", "priority": "critical"},
            {"status": "resolved", "priority": "ultra-high"}
        ]
        
        result = generate_reports(invalid_tickets)
        
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["status_breakdown"]["open"], 0)
        self.assertEqual(result["status_breakdown"]["resolved"], 1)
        self.assertEqual(result["priority_breakdown"]["critical"], 1)
        self.assertEqual(result["priority_breakdown"]["high"], 0)


if __name__ == "__main__":
    unittest.main()
