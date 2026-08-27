"""Integration tests for end-to-end workflows."""

import pytest
from src.claims.models import Claim, ClaimFlag, FlagReason
from src.claims.processor import ClaimProcessor
from src.core.anaesthetic import calculate_modifier
from src.core.icd10 import ICDEngine
from src.tracking.metrics import MetricsTracker


class TestEndToEndClaims:
    """Test complete claim processing workflows."""

    def test_full_claim_processing_workflow(self, sample_claim, claim_processor):
        """Test processing a claim through full validation pipeline."""
        result = claim_processor.process_claim(
            sample_claim,
            assessor='Test Assessor',
            modifier_code='0036',
            modifier_minutes=45,
        )
        
        assert result['claim_no'] == 'TEST-001'
        assert result['processed'] is True
        assert len(result['validations']) > 0
        assert 'modifiers' in result
        assert result['modifiers']['code'] == '0036'

    def test_claim_flagging_workflow(self, sample_claim, claim_processor):
        """Test flagging a claim during processing."""
        flag = ClaimFlag(
            claim_no=sample_claim.claim_no,
            reason=FlagReason.NEEDS_REVIEW,
            note='Requires verification',
            assessor='Test Assessor',
        )
        claim_processor.add_flag(flag)
        
        flags = claim_processor.get_flags_for_claim(sample_claim.claim_no)
        assert len(flags) == 1
        assert flags[0].reason == FlagReason.NEEDS_REVIEW

    def test_time_tracking_during_processing(self, claim_processor):
        """Test time logging for claims."""
        claim_processor.add_time_log('CLAIM-001', 12.5)
        claim_processor.add_time_log('CLAIM-002', 14.0)
        claim_processor.add_time_log('CLAIM-003', 13.5)
        
        avg_time = claim_processor.get_average_time()
        assert avg_time == pytest.approx(13.33, abs=0.1)

    def test_complex_claim_scenario(self):
        """Test complex real-world scenario."""
        processor = ClaimProcessor()
        metrics = MetricsTracker()
        
        # Process multiple claims
        for i in range(5):
            claim = Claim(
                claim_no=f'CLAIM-{i:03d}',
                provider=f'Provider {i}',
                service='Service',
                icd10='J01.90',
                description='Test',
                discipline='04',
                amount=1000.00 + (i * 100),
            )
            
            result = processor.process_claim(claim, 'Assessor')
            processor.add_time_log(claim.claim_no, 12.0 + i)
            metrics.log_claim_time(claim.claim_no, 12.0 + i)
        
        assert processor.get_average_time() == pytest.approx(14.0, abs=0.1)
        assert metrics.committed_count == 5
        summary = metrics.get_summary()
        assert summary['committed_count'] == 5
