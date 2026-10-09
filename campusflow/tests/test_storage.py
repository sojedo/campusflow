cat << 'EOF' > tests/test_storage.py
import os
import unittest
import tempfile
from campusflow.storage import load_tickets, save_tickets


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.file_path = os.path.join(self.test_dir.name, "tickets.json")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_missing_file_returns_empty(self):
        res = load_tickets(self.file_path)
        self.assertEqual(res, [])

    def test_roundtrip_save_load(self):
        data = [{"id": "T001", "title": "Test Ticket"}]
        save_tickets(self.file_path, data)
        loaded = load_tickets(self.file_path)
        self.assertEqual(data, loaded)

    def test_corrupted_json_raises_value_error(self):
        with open(self.file_path, "w") as f:
            f.write("{invalid json content")

        with self.assertRaises(ValueError):
            load_tickets(self.file_path)


if __name__ == "__main__":
    unittest.main()
EOF