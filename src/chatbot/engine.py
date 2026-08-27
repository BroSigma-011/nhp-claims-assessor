"""AI Chatbot engine with LLM integration."""

import requests
from typing import Dict, Optional, List
from src.config import Config
from src.chatbot.rules_kb import RulesKnowledgeBase
from src.chatbot.prompts import SystemPromptBuilder
from src.chatbot.workflow_guide import WorkflowGuide


class ChatbotEngine:
    """Main chatbot engine combining LLM, KB, and workflow guidance."""

    def __init__(self, model: Optional[str] = None, provider: Optional[str] = None):
        self.model = model or Config.CHATBOT_MODEL
        self.provider = provider or Config.CHATBOT_PROVIDER
        self.base_url = Config.OLLAMA_BASE_URL
        self.kb = RulesKnowledgeBase()
        self.prompt_builder = SystemPromptBuilder()
        self.workflow_guide = WorkflowGuide()
        self.conversation_history: List[Dict] = []

    def query(
        self,
        user_message: str,
        current_workflow_step: Optional[int] = None,
        context_claim: Optional[Dict] = None,
    ) -> Dict:
        """Process user query with context."""
        context_prompt = self.prompt_builder.build_context_prompt(
            user_message, current_workflow_step, context_claim
        )
        raw_response = self._call_llm(context_prompt)
        next_steps = self.workflow_guide.suggest_actions(current_workflow_step or 0, context_claim)
        
        response = {
            'summary': raw_response[:200],
            'next_steps': next_steps,
            'raw_response': raw_response,
        }
        self.conversation_history.append({'user': user_message, 'assistant': response})
        return response

    def _call_llm(self, prompt: str) -> str:
        """Call LLM or fallback."""
        try:
            if self.provider == 'ollama':
                response = requests.post(
                    f'{self.base_url}/api/generate',
                    json={'model': self.model, 'prompt': prompt, 'stream': False},
                    timeout=30,
                )
                return response.json().get('response', 'No response')
        except Exception as e:
            pass
        return 'Please consult NHP Gazette and official documentation.'

    def get_conversation_history(self) -> List[Dict]:
        return self.conversation_history.copy()

    def reset_conversation(self) -> None:
        self.conversation_history = []
