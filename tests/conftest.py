"""Pytest configuration and fixtures."""

import pytest
from src.config import Config, ReferenceData
from src.core.anaesthetic import calculate_modifier
from src.core.icd10 import ICDEngine
from src.core.workflow import WorkflowManager
from src.claims.models import Claim, ClaimFlag, FlagReason
from src.claims.processor import ClaimProcessor
from src.tracking.metrics import MetricsTracker
from src.chatbot.engine import ChatbotEngine


@pytest.fixture
def sample_claim():
    """Create a sample claim for testing."""
    return Claim(
        claim_no='TEST-001',
        provider='Test Hospital',
        service='Surgery',
        icd10='J01.90',
        description='Acute sinusitis',
        discipline='04',
        amount=6450.00,
    )


@pytest.fixture
def claim_processor():
    """Create a claim processor instance."""
    return ClaimProcessor()


@pytest.fixture
def metrics_tracker():
    """Create a metrics tracker instance."""
    return MetricsTracker()


@pytest.fixture
def workflow_manager():
    """Create a workflow manager instance."""
    return WorkflowManager()


@pytest.fixture
def icd_engine():
    """Create an ICD engine instance."""
    return ICDEngine()


@pytest.fixture
def chatbot_engine():
    """Create a chatbot engine instance."""
    return ChatbotEngine(provider='ollama')
