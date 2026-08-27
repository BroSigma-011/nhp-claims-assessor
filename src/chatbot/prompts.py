"""System prompts and context builders for chatbot."""

from typing import Dict, Optional
from src.config import ReferenceData
from src.chatbot.rules_kb import RulesKnowledgeBase


class SystemPromptBuilder:
    """Builds system prompts for AI chatbot with context."""

    BASE_SYSTEM_PROMPT = """You are an expert NHP Claims Assessment Assistant.
Your role is to provide concise answers about NHP claims processing.
Always cite Gazette rules and suggest next workflow steps."""

    def __init__(self):
        self.kb = RulesKnowledgeBase()

    def build_system_prompt(self) -> str:
        return self.BASE_SYSTEM_PROMPT

    def build_context_prompt(
        self,
        user_message: str,
        current_workflow_step: Optional[int] = None,
        context_claim: Optional[Dict] = None,
    ) -> str:
        parts = []
        if current_workflow_step is not None:
            step_name = ReferenceData.WORKFLOW_STEPS[current_workflow_step] if 0 <= current_workflow_step < len(ReferenceData.WORKFLOW_STEPS) else 'Unknown'
            parts.append(f'Workflow Step {current_workflow_step + 1}/7: {step_name}')
        if context_claim:
            parts.append('Claim Context: ' + str(context_claim))
        parts.append(f'Question: {user_message}')
        return '\n'.join(parts)
