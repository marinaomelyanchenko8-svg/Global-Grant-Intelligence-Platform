"""Tests for the intelligence analyzer module."""

import unittest
from datetime import datetime, timedelta

from intelligence.analyzer import analyze_grant
from intelligence.topics import detect_topics, TOPIC_KEYWORDS
from intelligence.trends import classify_trend
from intelligence.scoring import calculate_score


class TestAnalyzer(unittest.TestCase):
    """Test cases for grant intelligence analysis."""

    def _future_date(self, months: int) -> str:
        """Helper to generate a future ISO date."""
        future = datetime.now() + timedelta(days=months * 30)
        return future.strftime("%Y-%m-%d")

    def test_high_funding_grant(self):
        """Test grant with high funding amount."""
        grant = {
            "id": "test-001",
            "title": "AI Research Grant",
            "description": "Machine learning and artificial intelligence research",
            "funding_amount": 150000,
            "deadline": self._future_date(8),
            "eligibility": "Global applicants",
        }
        result = analyze_grant(grant)

        self.assertIn("AI", result["topics"])
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
        self.assertIn(result["trend_label"], ["Emerging", "Growing", "Stable", "Declining"])
        self.assertIsInstance(result["explanation"], str)
        self.assertLessEqual(len(result["explanation"]), 100)

    def test_time_sensitive_grant(self):
        """Test time-sensitive grant with urgent deadline."""
        near_date = datetime.now() + timedelta(days=15)
        grant = {
            "id": "test-002",
            "title": "Climate Change Research",
            "description": "Final call for climate and environment proposals",
            "funding_amount": 25000,
            "deadline": near_date.strftime("%Y-%m-%d"),
            "eligibility": "US universities",
        }
        result = analyze_grant(grant)

        self.assertIn("Climate", result["topics"])
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
        self.assertEqual(result["trend_label"], "Declining")

    def test_broad_eligibility_grant(self):
        """Test grant with broad international eligibility."""
        grant = {
            "id": "test-003",
            "title": "Healthcare Innovation",
            "description": "Medical research with innovation and growth focus",
            "funding_amount": 75000,
            "deadline": self._future_date(4),
            "eligibility": "Any international organization",
        }
        result = analyze_grant(grant)

        self.assertIn("Healthcare", result["topics"])
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)
        self.assertIn(result["trend_label"], ["Emerging", "Growing", "Stable", "Declining"])

    def test_emerging_trend_grant(self):
        """Test grant classified as Emerging trend."""
        grant = {
            "id": "test-004",
            "title": "New Education Pilot",
            "description": "First-time pilot program for student learning",
            "funding_amount": 50000,
            "deadline": self._future_date(8),
            "eligibility": "All universities",
        }
        result = analyze_grant(grant)

        self.assertIn("Education", result["topics"])
        self.assertEqual(result["trend_label"], "Emerging")
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_score_range_validation(self):
        """Verify score is always within 0-100 range."""
        test_cases = [
            {"funding_amount": 0, "deadline": self._future_date(1)},
            {"funding_amount": 1000000, "deadline": self._future_date(12)},
            {"funding_amount": 50000, "deadline": self._future_date(3)},
        ]

        for i, data in enumerate(test_cases):
            grant = {
                "id": f"score-test-{i}",
                "title": "Test Grant",
                "description": "Test description",
                **data,
            }
            result = analyze_grant(grant)
            self.assertGreaterEqual(
                result["score"], 0,
                f"Score {result['score']} is below 0 for case {i}"
            )
            self.assertLessEqual(
                result["score"], 100,
                f"Score {result['score']} is above 100 for case {i}"
            )

    def test_topics_from_approved_list(self):
        """Verify detected topics are from approved list."""
        approved_topics = set(TOPIC_KEYWORDS.keys())

        grant = {
            "id": "test-005",
            "title": "AI for Climate and Healthcare",
            "description": "Machine learning in medical treatment and climate research",
            "funding_amount": 100000,
            "deadline": self._future_date(6),
        }
        result = analyze_grant(grant)

        for topic in result["topics"]:
            self.assertIn(
                topic, approved_topics,
                f"Topic '{topic}' is not in approved list {approved_topics}"
            )

    def test_trend_labels_valid(self):
        """Verify trend labels are valid values."""
        valid_labels = {"Emerging", "Growing", "Stable", "Declining"}

        test_grants = [
            {"deadline": self._future_date(8), "description": "new pilot", "funding_amount": 10000},
            {"deadline": self._future_date(4), "description": "expanded program", "funding_amount": 150000},
            {"deadline": self._future_date(2), "description": "standard program", "funding_amount": 50000},
            {"deadline": self._future_date(0), "description": "final call", "funding_amount": 5000},
        ]

        for i, data in enumerate(test_grants):
            grant = {
                "id": f"trend-test-{i}",
                "title": "Test Grant",
                **data,
            }
            result = analyze_grant(grant)
            self.assertIn(
                result["trend_label"], valid_labels,
                f"Trend label '{result['trend_label']}' is not valid"
            )

    def test_empty_grant(self):
        """Test analyzer handles minimal grant data."""
        grant = {
            "id": "test-empty",
            "title": "",
            "description": "",
        }
        result = analyze_grant(grant)

        self.assertIsInstance(result["topics"], list)
        self.assertGreaterEqual(result["confidence"], 0)
        self.assertIn(result["trend_label"], ["Emerging", "Growing", "Stable", "Declining"])
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_original_data_preserved(self):
        """Verify original grant data is preserved in result."""
        grant = {
            "id": "preserve-test",
            "title": "Original Title",
            "description": "Original description",
            "funding_amount": 75000,
            "custom_field": "custom_value",
        }
        result = analyze_grant(grant)

        self.assertEqual(result["id"], "preserve-test")
        self.assertEqual(result["title"], "Original Title")
        self.assertEqual(result["funding_amount"], 75000)
        self.assertEqual(result["custom_field"], "custom_value")
        self.assertIn("topics", result)
        self.assertIn("score", result)

    def test_multiple_topics_detection(self):
        """Test detection of multiple topics in single grant."""
        grant = {
            "id": "multi-topic",
            "title": "Fintech for Social Impact",
            "description": "Blockchain banking solution for community nonprofit equity",
            "funding_amount": 80000,
            "deadline": self._future_date(5),
        }
        result = analyze_grant(grant)

        self.assertGreaterEqual(len(result["topics"]), 2)
        self.assertIn("Fintech", result["topics"])
        self.assertIn("Social Impact", result["topics"])


if __name__ == "__main__":
    unittest.main()
