"""Tests for workflow management."""

import pytest
from src.core.workflow import WorkflowManager


class TestWorkflowManager:
    """Test workflow state management."""

    def test_workflow_initialization(self, workflow_manager):
        """Test workflow initializes with all steps incomplete."""
        status = workflow_manager.get_status()
        assert status['progress'] == '0/7'
        assert status['percentage'] == 0.0
        assert status['all_complete'] is False

    def test_set_step_complete(self, workflow_manager):
        """Test marking a step as complete."""
        workflow_manager.set_step(0, True)
        assert workflow_manager.is_step_complete(0) is True
        assert workflow_manager.progress == '1/7'

    def test_set_multiple_steps_complete(self, workflow_manager):
        """Test marking multiple steps complete."""
        workflow_manager.set_step(0, True)
        workflow_manager.set_step(1, True)
        workflow_manager.set_step(2, True)
        assert workflow_manager.progress == '3/7'
        status = workflow_manager.get_status()
        assert status['percentage'] == pytest.approx(42.857, abs=0.1)

    def test_next_step_suggestion(self, workflow_manager):
        """Test next step suggestion."""
        workflow_manager.set_step(0, True)
        assert workflow_manager.next_step == 1

    def test_all_steps_complete(self, workflow_manager):
        """Test when all steps are complete."""
        for i in range(7):
            workflow_manager.set_step(i, True)
        status = workflow_manager.get_status()
        assert status['all_complete'] is True
        assert status['progress'] == '7/7'
        assert status['percentage'] == 100.0

    def test_workflow_reset(self, workflow_manager):
        """Test resetting workflow."""
        for i in range(7):
            workflow_manager.set_step(i, True)
        workflow_manager.reset()
        assert workflow_manager.progress == '0/7'
        assert workflow_manager.is_step_complete(0) is False
