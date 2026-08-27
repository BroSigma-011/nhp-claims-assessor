"""Claim processing orchestrator."""

from typing import List, Dict, Optional
from src.claims.models import Claim, ClaimFlag, TimeLog
from src.core.validators import validate_discipline, validate_modifier_code
from src.core.anaesthetic import calculate_modifier
from src.core.icd10 import ICDEngine


class ClaimProcessor:
    """Orchestrates claim processing through 7-step workflow."""

    def __init__(self):
        """Initialize claim processor."""
        self.icd_engine = ICDEngine()
        self.processed_claims: List[Claim] = []
        self.flags: List[ClaimFlag] = []
        self.time_logs: List[TimeLog] = []

    def process_claim(
        self,
        claim: Claim,
        assessor: str,
        modifier_code: Optional[str] = None,
        modifier_minutes: Optional[float] = None,
    ) -> Dict:
        """Process a claim through validation pipeline."""
        result = {
            'claim_no': claim.claim_no,
            'validations': [],
            'warnings': [],
            'modifiers': {},
            'processed': True,
        }

        # Discipline validation
        is_valid, msg = validate_discipline(claim.discipline)
        result['validations'].append({'type': 'discipline', 'valid': is_valid, 'message': msg})
        if not is_valid:
            result['warnings'].append(msg)

        # Modifier calculation
        if modifier_code and modifier_minutes:
            is_valid, msg = validate_modifier_code(modifier_code)
            if is_valid:
                try:
                    mod_result = calculate_modifier(
                        code=modifier_code,
                        minutes=modifier_minutes,
                        base_tariff=claim.amount,
                    )
                    result['modifiers'] = mod_result.to_dict()
                except Exception as e:
                    result['warnings'].append(f'Modifier calculation failed: {e}')
            else:
                result['warnings'].append(msg)

        # ICD-10 validation
        icd_lookup = self.icd_engine.lookup_code(claim.icd10)
        if icd_lookup:
            result['validations'].append({
                'type': 'icd10',
                'valid': True,
                'message': f'ICD-10 {claim.icd10} found: {icd_lookup.get("description", "")}',
            })
        else:
            result['warnings'].append(f'ICD-10 code {claim.icd10} not found in reference data')

        return result

    def add_time_log(self, claim_no: str, minutes: float, delegated: int = 0) -> None:
        """Log processing time for a claim."""
        self.time_logs.append(
            TimeLog(claim_no=claim_no, minutes=minutes, delegated=delegated)
        )

    def add_flag(self, flag: ClaimFlag) -> None:
        """Add a flag to a claim."""
        self.flags.append(flag)

    def get_flags_for_claim(self, claim_no: str) -> List[ClaimFlag]:
        """Get all flags for a specific claim."""
        return [f for f in self.flags if f.claim_no == claim_no]

    def get_average_time(self) -> float:
        """Calculate average processing time."""
        if not self.time_logs:
            return 0.0
        total_minutes = sum(log.minutes for log in self.time_logs)
        return total_minutes / len(self.time_logs)
