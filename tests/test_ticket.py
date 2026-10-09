"""
Tests input validation boundaries, normalization, and the business priority logic.
"""

import unittest
from campusflow.tickets import validate_ticket_input, calculate_priority, generate_next_id, create_ticket

class TestCampusFlowTickets(unittest.TestCase):

    

    def test_validation_valid_input(self):
        """Test happy path with clean, well-formatted input data."""
        result = validate_ticket_input("Wi-Fi is down", "Network", "high", 12)
        self.assertEqual(result["title"], "Wi-Fi is down")
        self.assertEqual(result["category"], "Network")
        self.assertEqual(result["urgency"], "high")
        self.assertEqual(result["affected_users"], 12)

    def test_validation_case_and_whitespace_normalization(self):
        """Verify inputs with messy text case and padding spaces normalize correctly."""
        result = validate_ticket_input("  My Laptop Broke   ", "  hardware  ", "  HIGH  ", 5)
        self.assertEqual(result["title"], "My Laptop Broke")
        self.assertEqual(result["category"], "Hardware")
        self.assertEqual(result["urgency"], "high")

    def test_validation_blank_title_raises_error(self):
        """Assert that completely blank titles or titles with only spaces fail validation."""
        with self.assertRaises(ValueError):
            validate_ticket_input("", "Software", "low", 1)
        with self.assertRaises(ValueError):
            validate_ticket_input("    ", "Software", "low", 1)

    def test_validation_invalid_category_raises_error(self):
        """Assert that categories outside the allowed list throw an exception."""
        with self.assertRaises(ValueError):
            validate_ticket_input("Server Crash", "Database", "medium", 4)

    def test_validation_invalid_urgency_raises_error(self):
        """Assert that non-supported urgency strings throw an exception."""
        with self.assertRaises(ValueError):
            validate_ticket_input("Error message", "Software", "critical-urgency", 2)

    def test_validation_invalid_affected_users_type_and_bounds(self):
        """Assert invalid user counts (decimals, zero, negative, text, booleans) fail cleanly."""
        with self.assertRaises(ValueError):
            validate_ticket_input("Issue", "Other", "low", 0)  
        with self.assertRaises(ValueError):
            validate_ticket_input("Issue", "Other", "low", -5)  
        with self.assertRaises(ValueError):
            validate_ticket_input("Issue", "Other", "low", "10")  
        with self.assertRaises(ValueError):
            validate_ticket_input("Issue", "Other", "low", True)  


    def test_priority_rule_1_critical(self):
        """Rule 1: High urgency AND 10 or more affected users -> critical"""
        self.assertEqual(calculate_priority("high", 10), "critical")
        self.assertEqual(calculate_priority("high", 15), "critical")

    def test_priority_rule_2_high(self):
        """Rule 2: High urgency OR 10 or more affected users -> high"""
        self.assertEqual(calculate_priority("high", 9), "high")       
        self.assertEqual(calculate_priority("medium", 10), "high")     
        self.assertEqual(calculate_priority("low", 12), "high")       

    def test_priority_rule_3_medium(self):
        """Rule 3: Medium urgency OR 3 or more affected users -> medium"""
        self.assertEqual(calculate_priority("medium", 2), "medium")
        self.assertEqual(calculate_priority("low", 3), "medium")
        self.assertEqual(calculate_priority("low", 9), "medium")

    def test_priority_rule_4_low(self):
        """Rule 4: All remaining valid combinations -> low"""
        self.assertEqual(calculate_priority("low", 1), "low")
        self.assertEqual(calculate_priority("low", 2), "low")

    

    def test_generate_id_empty_db(self):
        """Confirm a brand new ticket database safely defaults to T001."""
        self.assertEqual(generate_next_id({}), "T001")

    def test_generate_id_with_existing_records(self):
        """Verify sequence auto-increments based on the highest loaded ID string."""
        mock_db = {
            "T001": {"title": "A"},
            "T002": {"title": "B"},
            "T005": {"title": "C"}  
        }
        self.assertEqual(generate_next_id(mock_db), "T006")

    def test_create_ticket_integrates_properly(self):
        """Verify the coordinator assembly assigns initial statuses and fields correctly."""
        db = {}
        ticket = create_ticket(db, "System crash", "software", "HIGH", 15)
        
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])


if __name__ == "__main__":
    unittest.main()
