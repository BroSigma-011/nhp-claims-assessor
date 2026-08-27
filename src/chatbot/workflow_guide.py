"""Workflow guidance engine for suggesting next steps."""

from typing import Dict, List, Optional
from src.config import ReferenceData
from src.core.workflow import WorkflowManager


class WorkflowGuide:
    """Provides workflow guidance and suggestions."""

    STEP_GUIDANCE = {
        0: {'name': 'Verify membership & option', 'tasks': ['Confirm active NHP member', 'Verify benefit level']},
        1: {'name': 'Check discipline', 'tasks': ['Identify discipline code', 'Check MK exclusion list']},
        2: {'name': 'Apply dental EXT codes', 'tasks': ['Check if dental', 'Apply ORS (under 10) or DPA (10+)']},
        3: {'name': 'Calculate modifiers', 'tasks': ['Identify modifier code', 'Record duration', 'Run calculation']},
        4: {'name': 'Validate ICD-10 & tariffs', 'tasks': ['Search ICD-10 code', 'Verify NAMAF compliance']},
        5: {'name': 'Check rejections & auth', 'tasks': ['Verify authorizations', 'Check rejection codes']},
        6: {'name': 'Final quality check & submit', 'tasks': ['Review all details', 'Submit claim']},
    }

    def __init__(self):
        self.workflow_manager = WorkflowManager()

    def get_current_step_guidance(self, step_index: int) -> Optional[Dict]:
        return self.STEP_GUIDANCE.get(step_index)

    def suggest_actions(self, step_index: int, claim_context: Optional[Dict] = None) -> List[str]:
        guidance = self.get_current_step_guidance(step_index)
        return guidance.get('tasks', []) if guidance else []
