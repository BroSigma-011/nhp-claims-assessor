"""Tests for chatbot engine."""

import pytest
from src.chatbot.engine import ChatbotEngine
from src.chatbot.rules_kb import RulesKnowledgeBase


class TestChatbotEngine:
    """Test chatbot engine functionality."""

    def test_chatbot_initialization(self, chatbot_engine):
        """Test chatbot initializes correctly."""
        assert chatbot_engine.model is not None
        assert chatbot_engine.provider is not None
        assert chatbot_engine.conversation_history == []

    def test_chatbot_simple_query(self, chatbot_engine):
        """Test basic query handling."""
        response = chatbot_engine.query('What is code 0036?')
        assert 'summary' in response
        assert 'next_steps' in response

    def test_chatbot_with_workflow_context(self, chatbot_engine):
        """Test query with workflow step context."""
        response = chatbot_engine.query(
            'How do I verify membership?',
            current_workflow_step=0,
        )
        assert response['summary'] is not None
        assert 'next_steps' in response

    def test_chatbot_with_claim_context(self, chatbot_engine):
        """Test query with claim context."""
        context = {
            'claim_no': 'TEST-001',
            'discipline': '04',
            'amount': 6450.00,
        }
        response = chatbot_engine.query(
            'Is this discipline eligible for MK?',
            context_claim=context,
        )
        assert response is not None
        assert 'next_steps' in response

    def test_conversation_history_tracking(self, chatbot_engine):
        """Test conversation history is maintained."""
        chatbot_engine.query('Question 1')
        chatbot_engine.query('Question 2')
        history = chatbot_engine.get_conversation_history()
        assert len(history) == 2
        assert history[0]['user'] == 'Question 1'
        assert history[1]['user'] == 'Question 2'

    def test_conversation_reset(self, chatbot_engine):
        """Test resetting conversation history."""
        chatbot_engine.query('Question 1')
        chatbot_engine.reset_conversation()
        history = chatbot_engine.get_conversation_history()
        assert len(history) == 0


class TestRulesKnowledgeBase:
    """Test rules knowledge base."""

    def test_kb_initialization(self):
        """Test knowledge base initializes."""
        kb = RulesKnowledgeBase()
        assert kb.gazette_rules is not None

    def test_get_modifier_rules(self):
        """Test retrieving modifier rules."""
        kb = RulesKnowledgeBase()
        rule = kb.get_modifier_rules('0036')
        assert rule is not None
        assert rule['code'] == '0036'
        assert rule['payment_factor'] == 0.82

    def test_discipline_status_checking(self):
        """Test discipline status checking."""
        kb = RulesKnowledgeBase()
        status = kb.get_discipline_status('04')
        assert status['mk_eligible'] is True
        
        status = kb.get_discipline_status('37')
        assert status['mk_eligible'] is False

    def test_excluded_disciplines_list(self):
        """Test retrieving excluded disciplines."""
        kb = RulesKnowledgeBase()
        excluded = kb.get_mk_excluded_disciplines()
        assert '37' in excluded
        assert '68' in excluded
        assert '04' not in excluded
