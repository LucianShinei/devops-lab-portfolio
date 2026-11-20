import os
import unittest


class PipelineValidationTests(unittest.TestCase):
    def test_controlled_failure(self):
        self.assertNotEqual(
            os.environ.get("FORCE_TEST_FAILURE", "false").lower(),
            "true",
            "Controlled failure requested for the Jenkins demonstration.",
        )
