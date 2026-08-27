"""Productivity metrics and KPI calculations."""

from typing import List, Dict, Optional
from datetime import datetime
import statistics


class MetricsTracker:
    """Tracks productivity metrics and KPIs."""

    def __init__(self, baseline_threshold: float = 1.15):
        """Initialize metrics tracker."""
        self.time_logs: List[Dict] = []
        self.baseline_average: Optional[float] = None
        self.baseline_threshold = baseline_threshold
        self.committed_count = 0

    def log_claim_time(
        self,
        claim_no: str,
        minutes: float,
        delegated: int = 0,
    ) -> None:
        """Log processing time for a claim."""
        self.time_logs.append({
            'claim_no': claim_no,
            'minutes': minutes,
            'delegated': delegated,
            'timestamp': datetime.now().isoformat(timespec='seconds'),
        })
        self.committed_count += 1

        if len(self.time_logs) == 3 and self.baseline_average is None:
            self.baseline_average = self.get_average_time()

    def get_average_time(self, recent_n: Optional[int] = None) -> float:
        """Get average processing time."""
        if not self.time_logs:
            return 0.0
        logs = self.time_logs[-recent_n:] if recent_n else self.time_logs
        times = [log['minutes'] for log in logs]
        return statistics.mean(times) if times else 0.0

    def get_performance_alert(self, recent_n: int = 3) -> Optional[str]:
        """Check if performance has degraded."""
        if self.baseline_average is None or len(self.time_logs) <= recent_n:
            return None
        recent_avg = self.get_average_time(recent_n)
        ratio = recent_avg / self.baseline_average
        if ratio > self.baseline_threshold:
            percentage = round((ratio - 1) * 100, 1)
            return f'Performance feedback: {percentage}% slower than baseline.'
        return None

    def get_summary(self) -> Dict:
        """Get comprehensive metrics summary."""
        if not self.time_logs:
            return {'committed_count': 0, 'average_minutes': 0.0, 'baseline_minutes': None, 'total_minutes': 0.0}
        times = [log['minutes'] for log in self.time_logs]
        return {
            'committed_count': self.committed_count,
            'average_minutes': round(self.get_average_time(), 2),
            'baseline_minutes': round(self.baseline_average, 2) if self.baseline_average else None,
            'total_minutes': round(sum(times), 2),
            'min_time': round(min(times), 2),
            'max_time': round(max(times), 2),
            'std_dev': round(statistics.stdev(times), 2) if len(times) > 1 else 0.0,
        }
