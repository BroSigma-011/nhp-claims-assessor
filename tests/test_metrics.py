"""Tests for productivity metrics."""

import pytest
from src.tracking.metrics import MetricsTracker


class TestMetricsTracker:
    """Test metrics tracking and KPI calculations."""

    def test_metrics_initialization(self, metrics_tracker):
        """Test metrics tracker initializes."""
        assert metrics_tracker.committed_count == 0
        assert metrics_tracker.baseline_average is None
        assert len(metrics_tracker.time_logs) == 0

    def test_log_single_claim(self, metrics_tracker):
        """Test logging a single claim."""
        metrics_tracker.log_claim_time('CLAIM-001', 15.5)
        assert metrics_tracker.committed_count == 1
        assert len(metrics_tracker.time_logs) == 1

    def test_baseline_calculation(self, metrics_tracker):
        """Test baseline calculation after 3 claims."""
        metrics_tracker.log_claim_time('CLAIM-001', 12.0)
        assert metrics_tracker.baseline_average is None
        metrics_tracker.log_claim_time('CLAIM-002', 13.0)
        assert metrics_tracker.baseline_average is None
        metrics_tracker.log_claim_time('CLAIM-003', 14.0)
        assert metrics_tracker.baseline_average == 13.0

    def test_average_time_calculation(self, metrics_tracker):
        """Test average time calculation."""
        metrics_tracker.log_claim_time('CLAIM-001', 10.0)
        metrics_tracker.log_claim_time('CLAIM-002', 20.0)
        metrics_tracker.log_claim_time('CLAIM-003', 30.0)
        avg = metrics_tracker.get_average_time()
        assert avg == 20.0

    def test_recent_average(self, metrics_tracker):
        """Test recent N average calculation."""
        metrics_tracker.log_claim_time('CLAIM-001', 10.0)
        metrics_tracker.log_claim_time('CLAIM-002', 20.0)
        metrics_tracker.log_claim_time('CLAIM-003', 30.0)
        metrics_tracker.log_claim_time('CLAIM-004', 40.0)
        recent_avg = metrics_tracker.get_average_time(recent_n=2)
        assert recent_avg == 35.0

    def test_performance_alert_threshold(self, metrics_tracker):
        """Test performance alert when threshold exceeded."""
        metrics_tracker.log_claim_time('CLAIM-001', 10.0)
        metrics_tracker.log_claim_time('CLAIM-002', 10.0)
        metrics_tracker.log_claim_time('CLAIM-003', 10.0)
        assert metrics_tracker.baseline_average == 10.0
        
        metrics_tracker.log_claim_time('CLAIM-004', 12.0)
        metrics_tracker.log_claim_time('CLAIM-005', 12.0)
        metrics_tracker.log_claim_time('CLAIM-006', 12.0)
        alert = metrics_tracker.get_performance_alert(recent_n=3)
        assert alert is not None
        assert 'slower' in alert.lower()

    def test_summary_generation(self, metrics_tracker):
        """Test summary generation."""
        metrics_tracker.log_claim_time('CLAIM-001', 15.0)
        metrics_tracker.log_claim_time('CLAIM-002', 20.0)
        metrics_tracker.log_claim_time('CLAIM-003', 25.0)
        summary = metrics_tracker.get_summary()
        
        assert summary['committed_count'] == 3
        assert summary['average_minutes'] == 20.0
        assert summary['total_minutes'] == 60.0
        assert summary['min_time'] == 15.0
        assert summary['max_time'] == 25.0
