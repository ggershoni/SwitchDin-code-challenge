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
    create_report,
    clear_events
)


class TestCreateReport(unittest.TestCase):

    def setUp(self):
        # Setup test data
        self.vpp_name = "TestVPP"
        self.revenue_percentage = "10"
        self.daily_fee = "2.5"
        self.nmi1 = "1234567890"
        self.nmi2 = "2345678901"
        self.address1 = "123 Test St, Test City"
        self.address2 = "456 Sample Rd, Sample Town"
        self.manufacturer = "TestMfg"
        self.serial_num1 = "SN123456"
        self.serial_num2 = "SN789012"
        self.capacity1 = "10"
        self.capacity2 = "15"
        self.filename = "test_events.csv"
        self.year_month = "2024-03"

        # Create test VPP, sites, and batteries
        create_vpp(self.vpp_name, self.revenue_percentage, self.daily_fee)
        create_site(self.vpp_name, self.nmi1, self.address1)
        create_site(self.vpp_name, self.nmi2, self.address2)
        create_battery(self.nmi1, self.manufacturer, self.serial_num1, self.capacity1)
        create_battery(self.nmi2, self.manufacturer, self.serial_num2, self.capacity2)

        # Import test events
        clear_events()
        try:
            import_events(self.filename)
        except FileNotFoundError:
            import_events(os.path.join('test', self.filename))

    def test_create_report_structure(self):
        report = create_report(self.vpp_name, self.year_month)
        self.assertIsInstance(report, str)

        try:
            json_report = json.loads(report)
        except json.JSONDecodeError:
            self.fail("create_report did not return valid JSON")

        expected_keys = ["vpp_name", "year_month", "total_revenue", "vpp_revenue", "site_revenues"]
        for key in expected_keys:
            self.assertIn(key, json_report)

    def test_create_report_values(self):
        report = create_report(self.vpp_name, self.year_month)
        json_report = json.loads(report)

        self.assertEqual(json_report["vpp_name"], self.vpp_name)
        self.assertEqual(json_report["year_month"], self.year_month)

        # Calculate expected total revenue
        total_revenue = (10.5 * 0.15 + 8.2 * 0.14 + 11.0 * 0.15) + (12.3 * 0.16 + 9.7 * 0.15 + 10.5 * 0.14)
        self.assertAlmostEqual(json_report["total_revenue"], total_revenue, places=2)

        # Check VPP revenue (10% of total revenue + daily fees for 2 sites for 28 days)
        expected_vpp_revenue = (total_revenue * 0.1) + (2 * 2.5 * 28)
        self.assertAlmostEqual(json_report["vpp_revenue"], expected_vpp_revenue, places=2)

        # Check site revenues
        self.assertEqual(len(json_report["site_revenues"]), 2)
        for site_revenue in json_report["site_revenues"]:
            self.assertIn("nmi", site_revenue)
            self.assertIn("revenue", site_revenue)
            self.assertIn("daily_fees", site_revenue)

    def test_create_report_site_revenue_distribution(self):
        report = create_report(self.vpp_name, self.year_month)
        json_report = json.loads(report)

        total_site_revenue = sum(site["revenue"] for site in json_report["site_revenues"])
        total_capacity = float(self.capacity1) + float(self.capacity2)

        for site_revenue in json_report["site_revenues"]:
            if site_revenue["nmi"] == self.nmi1:
                # 80% of its own events + 20% distributed by capacity
                expected_total_revenue = (10.5 * 0.15 + 8.2 * 0.14 + 11.0 * 0.15)
                vpp_revenue = expected_total_revenue * (int(self.revenue_percentage) / 100)
                expected_revenue = (0.8 * (expected_total_revenue - vpp_revenue)) + \
                                   (0.2 * total_site_revenue * (float(self.capacity1) / total_capacity))
                self.assertAlmostEqual(site_revenue["revenue"], expected_revenue, places=2)
            elif site_revenue["nmi"] == self.nmi2:
                expected_total_revenue =(12.3 * 0.16 + 9.7 * 0.15 + 10.5 * 0.14)
                vpp_revenue = expected_total_revenue * (int(self.revenue_percentage) / 100)
                expected_revenue = (0.8 * (expected_total_revenue - vpp_revenue)) + \
                                   (0.2 * total_site_revenue * (float(self.capacity2) / total_capacity))
                self.assertAlmostEqual(site_revenue["revenue"], expected_revenue, places=2)

    def test_create_report_daily_fees(self):
        report = create_report(self.vpp_name, self.year_month)
        json_report = json.loads(report)

        for site_revenue in json_report["site_revenues"]:
            self.assertAlmostEqual(site_revenue["daily_fees"], 28 * float(self.daily_fee), places=2)

    def tearDown(self):
        # Clean up any created files or reset any global state
        pass


if __name__ == '__main__':
    unittest.main()