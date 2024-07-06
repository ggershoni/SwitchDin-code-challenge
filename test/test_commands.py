import sys
import os
import unittest
import json

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from commands import (
    create_vpp,
    create_site,
    create_battery,
    import_events,
    create_report
)


class TestVPPFunctions(unittest.TestCase):

    def setUp(self):
        # Setup any necessary test data
        self.vpp_name = "TestVPP"
        self.revenue_percentage = "10"
        self.daily_fee = "2.5"
        self.nmi = "1234567890"
        self.address = "123 Test St, Test City"
        self.manufacturer = "TestMfg"
        self.serial_num = "SN123456"
        self.capacity = "10"
        self.filename = "test_events.csv"
        self.year_month = "2024-03"

    def test_create_vpp(self):
        result = create_vpp(self.vpp_name, self.revenue_percentage, self.daily_fee)
        self.assertIsNone(result)  # Assuming the function doesn't return anything

    def test_create_site(self):
        result = create_site(self.vpp_name, self.nmi, self.address)
        self.assertIsNone(result)  # Assuming the function doesn't return anything

    def test_create_battery(self):
        create_site(self.vpp_name, self.nmi, self.address)
        result = create_battery(self.nmi, self.manufacturer, self.serial_num, self.capacity)
        self.assertIsNone(result)  # Assuming the function doesn't return anything

    def test_import_events(self):
        result = import_events(self.filename)
        self.assertIsNone(result)  # Assuming the function doesn't return anything

    def test_create_report(self):
        # Setup required for this test to pass
        create_vpp(self.vpp_name, self.revenue_percentage, self.daily_fee)

        report = create_report(self.vpp_name, self.year_month)
        self.assertIsInstance(report, str)

        # Try to parse the JSON
        try:
            json_report = json.loads(report)
        except json.JSONDecodeError:
            self.fail("create_report did not return valid JSON")

        # Check for expected keys in the JSON report
        expected_keys = ["vpp_name", "year_month", "total_revenue", "vpp_revenue", "site_revenues"]
        for key in expected_keys:
            self.assertIn(key, json_report)

    def test_integration(self):
        # Test the entire flow
        create_vpp(self.vpp_name, self.revenue_percentage, self.daily_fee)
        create_site(self.vpp_name, self.nmi, self.address)
        create_battery(self.nmi, self.manufacturer, self.serial_num, self.capacity)
        import_events(self.filename)
        report = create_report(self.vpp_name, self.year_month)

        self.assertIsInstance(report, str)
        json_report = json.loads(report)
        self.assertEqual(json_report["vpp_name"], self.vpp_name)
        self.assertEqual(json_report["year_month"], self.year_month)


if __name__ == '__main__':
    unittest.main()