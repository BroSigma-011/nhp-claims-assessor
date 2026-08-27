"""FastAPI web application for NHP Claims Assessor."""

from typing import Optional, Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.config import Config
from src.core.anaesthetic import calculate_modifier
from src.core.icd10 import ICDEngine
from src.core.workflow import WorkflowManager
from src.chatbot.engine import ChatbotEngine
from src.claims.models import Claim
from src.claims.processor import ClaimProcessor

app = FastAPI(
    title='NHP Claims Assessor API',
    description='Namibian Medical-Aid Claims Assessment Service',
    version='2.0.0',
)

# Initialize components
icd_engine = ICDEngine()
chatbot = ChatbotEngine()
claim_processor = ClaimProcessor()


class ModifierRequest(BaseModel):
    """Request for modifier calculation."""
    code: str
    minutes: float
    base_tariff: float
    provider: str = 'Anaesthetist'


class ICD10Request(BaseModel):
    """Request for ICD-10 search."""
    query: str
    limit: int = 8


class ChatbotRequest(BaseModel):
    """Request for chatbot query."""
    message: str
    workflow_step: Optional[int] = None
    claim_context: Optional[Dict] = None


class ClaimRequest(BaseModel):
    """Request for claim processing."""
    claim: Claim
    assessor: str
    modifier_code: Optional[str] = None
    modifier_minutes: Optional[float] = None


@app.get('/')
def read_root():
    """API root endpoint."""
    return {'message': 'NHP Claims Assessor API', 'version': '2.0.0'}


@app.post('/api/modifier/calculate')
def calculate_modifier_endpoint(request: ModifierRequest):
    """Calculate anaesthetic modifier."""
    try:
        result = calculate_modifier(
            code=request.code,
            minutes=request.minutes,
            base_tariff=request.base_tariff,
            provider=request.provider,
        )
        return result.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/api/icd10/search')
def search_icd10_endpoint(request: ICD10Request):
    """Search ICD-10 codes."""
    results = icd_engine.search(request.query, limit=request.limit)
    return {'results': results.to_dict(orient='records')}


@app.get('/api/icd10/lookup/{code}')
def lookup_icd10_endpoint(code: str):
    """Lookup specific ICD-10 code."""
    result = icd_engine.lookup_code(code)
    if not result:
        raise HTTPException(status_code=404, detail=f'ICD-10 code {code} not found')
    return result


@app.post('/api/chatbot/query')
def chatbot_query_endpoint(request: ChatbotRequest):
    """Query the chatbot."""
    response = chatbot.query(
        user_message=request.message,
        current_workflow_step=request.workflow_step,
        context_claim=request.claim_context,
    )
    return response


@app.post('/api/claims/process')
def process_claim_endpoint(request: ClaimRequest):
    """Process a claim."""
    result = claim_processor.process_claim(
        claim=request.claim,
        assessor=request.assessor,
        modifier_code=request.modifier_code,
        modifier_minutes=request.modifier_minutes,
    )
    return result


@app.get('/api/health')
def health_check():
    """Health check endpoint."""
    return {'status': 'healthy', 'version': '2.0.0'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
        log_level='info',
    )
