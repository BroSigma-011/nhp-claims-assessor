"""Rules Knowledge Base for chatbot - Gazette and scheme references."""

from typing import Dict, List, Optional
from src.config import GazetteRules, ReferenceData, Config


class RulesKnowledgeBase:
    """Provides context and references from NHP Gazette and scheme rules."""

    def __init__(self):
        """Initialize knowledge base."""
        self.gazette_rules = GazetteRules.RULES_KNOWLEDGE_BASE
        self.reference_data = ReferenceData()

    def get_modifier_rules(self, code: str) -> Optional[Dict]:
        modifiers = self.gazette_rules.get('anaesthetic_modifiers', {})
        for rule in modifiers.get('rules', []):
            if rule['code'] == code:
                return rule
        return None

    def get_discipline_status(self, discipline: str) -> Dict:
        is_excluded = ReferenceData.is_mk_excluded(discipline)
        return {
            'discipline': discipline,
            'mk_eligible': not is_excluded,
            'status': 'Direct Benefit (excluded from MK)' if is_excluded else 'MK Eligible',
            'gazette_ref': 'NHP Scheme Administration Circular 2026',
        }

    def get_mk_excluded_disciplines(self) -> List[str]:
        return list(ReferenceData.MK_EXCLUDED_DISCIPLINES)
