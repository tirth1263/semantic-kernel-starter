import unittest

from semantic_kernel_starter.plugins import TimePlugin


class TimePluginTests(unittest.TestCase):
    def test_now_uses_configured_default_timezone(self):
        result = TimePlugin(default_timezone="UTC").now()

        self.assertIn("UTC", result)

    def test_now_reports_unknown_timezone(self):
        result = TimePlugin(default_timezone="UTC").now("Not/AZone")

        self.assertIn("Unknown timezone", result)


if __name__ == "__main__":
    unittest.main()

