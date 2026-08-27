"""Dashboard data preparation for visualizations."""

from typing import List, Dict
import pandas as pd


class DashboardData:
    """Prepares data for dashboard visualizations."""

    def __init__(self, time_logs: List[Dict], flags: List[Dict]):
        """Initialize dashboard data."""
        self.time_logs_df = pd.DataFrame(time_logs) if time_logs else pd.DataFrame()
        self.flags_df = pd.DataFrame(flags) if flags else pd.DataFrame()

    def get_time_series_data(self) -> Dict:
        """Get data for time series visualization."""
        if self.time_logs_df.empty:
            return {'claim_no': [], 'minutes': []}
        return {
            'claim_no': self.time_logs_df['claim_no'].tolist(),
            'minutes': self.time_logs_df['minutes'].tolist(),
        }

    def get_flag_distribution(self) -> Dict:
        """Get flag reason distribution."""
        if self.flags_df.empty:
            return {}
        return self.flags_df['reason'].value_counts().to_dict()

    def get_performance_gauge_data(self, baseline: float, recent_avg: float) -> int:
        """Get gauge data (0-200) representing performance vs baseline."""
        if baseline == 0:
            return 100
        ratio = (recent_avg / baseline) * 100
        return max(0, min(200, int(ratio)))
