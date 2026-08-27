# NHP Claims Assessor Pocket Assistant - 2026

## Overview

A comprehensive Namibian medical-aid claims assessment platform featuring:

- **Structured 7-step workflow** for claims processing
- **AI-powered chatbot** with Gazette/scheme rule references
- **Anaesthetic modifier calculations** (codes 0036, 0023, 0038, 0039)
- **Reverse ICD-10 lookup** with fuzzy matching and ML prediction
- **PDF invoice processing** with OCR and information extraction
- **Productivity tracking** with performance baselines and KPI dashboards
- **Claim flagging** and revision management
- **Multilingual support** (11 languages)
- **Excel export** with formatting and KPI summaries

## Quick Start

### Installation

```bash
git clone https://github.com/BroSigma-011/nhp-claims-assessor.git
cd nhp-claims-assessor
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/ -v --cov=src
```

### Running the Application

#### As a Jupyter Colab Notebook

1. Open `notebooks/nhp_claims_assessor.ipynb` in Google Colab
2. Run cells sequentially
3. Interact with widgets for claims processing

#### As a Standalone CLI Application

```bash
python src/cli_app.py
```

#### As a Web API (FastAPI)

```bash
python src/web_app.py
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── config.py                    # Configuration & reference data
│   ├── core/
│   │   ├── __init__.py
│   │   ├── anaesthetic.py           # Modifier calculation logic
│   │   ├── icd10.py                 # ICD-10 search & ML prediction
│   │   ├── workflow.py              # 7-step workflow state management
│   │   └── validators.py            # Discipline & rule validators
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── engine.py                # AI chatbot core (Ollama/HuggingFace)
│   │   ├── rules_kb.py              # Rules knowledge base (Gazette refs)
│   │   ├── prompts.py               # System prompts & context builders
│   │   └── workflow_guide.py        # Workflow suggestion engine
│   ├── claims/
│   │   ├── __init__.py
│   │   ├── models.py                # Pydantic models (Claim, Flag, etc.)
│   │   ├── processor.py             # Claim processing orchestrator
│   │   └── pdf_extractor.py         # PDF text/invoice extraction
│   ├── tracking/
│   │   ├── __init__.py
│   │   ├── metrics.py               # Time logging & KPI calculation
│   │   └── dashboard.py             # Dashboard visualization data
│   ├── export/
│   │   ├── __init__.py
│   │   └── excel.py                 # Formatted Excel workbook export
│   ├── cli_app.py                   # CLI interface
│   └── web_app.py                   # FastAPI web service
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures
│   ├── test_anaesthetic.py          # Modifier calculator tests
│   ├── test_icd10.py                # ICD-10 search & ML tests
│   ├── test_chatbot.py              # Chatbot engine tests
│   ├── test_validators.py           # Validation rule tests
│   ├── test_workflow.py             # Workflow state tests
│   ├── test_metrics.py              # KPI & tracking tests
│   └── test_integration.py          # End-to-end workflows
├── notebooks/
│   └── nhp_claims_assessor.ipynb    # Jupyter notebook (Colab-compatible)
├── data/
���   ├── sample_claims.csv            # Sample claims dataset
│   ├── icd10_reference.csv          # ICD-10 reference data
│   └── gazette_rules.json           # NHP Gazette rules & tariffs
├── .env.example                     # Environment variables template
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

## Key Features

### 1. AI Chatbot with Gazette References

The chatbot integrates with freeware LLM engines (Ollama/Hugging Face) to provide:

- **Context-aware assistance** on claims, rules, and procedures
- **Gazette & scheme rule citations** from the rules knowledge base
- **Logical workflow suggestions** based on user's current position
- **Multilingual summaries** of complex regulations

```python
from src.chatbot import ChatbotEngine

chatbot = ChatbotEngine(model='llama-2')
response = chatbot.query(
    user_message="What modifier should I apply to code 0036 for 45 minutes?",
    current_workflow_step=3,
    context_claim={'discipline': '04', 'service': 'anaesthesia'}
)
print(response['summary'])      # Concise answer
print(response['citations'])    # References to Gazette/tariffs
print(response['next_steps'])   # Suggested workflow actions
```

### 2. Anaesthetic Modifier Calculator

```python
from src.core.anaesthetic import calculate_modifier

result = calculate_modifier(
    code='0036',
    minutes=45,
    base_tariff=1000.00,
    provider='Anaesthetist'
)
print(result)
# {
#   'code': '0036',
#   'minutes': 45,
#   'units': 9,
#   'gross_value': 1038.50,
#   'payment_factor': 0.82,
#   'modifier_payment': 851.57,
#   'total_claim_value': 1851.57
# }
```

### 3. ICD-10 Reverse Search & ML Prediction

```python
from src.core.icd10 import ICDEngine

icd_engine = ICDEngine()

# Fuzzy search
results = icd_engine.search('sinusitis', limit=5)
print(results)  # Returns J01.90 with match scores

# ML prediction from service description
predicted = icd_engine.predict_from_description(
    "Patient presented with acute upper respiratory infection and fever"
)
print(predicted)  # Returns J06.9 with confidence score
```

### 4. Workflow State Management

```python
from src.core.workflow import WorkflowManager

workflow = WorkflowManager()
workflow.set_step(0, True)   # Mark "Verify membership" complete
workflow.set_step(1, True)   # Mark "Check discipline" complete

print(workflow.progress)     # 2/7 steps complete
print(workflow.next_step)    # Suggests step 2
print(workflow.get_status()) # Full status dict
```

### 5. Claim Flagging & Quality Checks

```python
from src.claims.models import ClaimFlag, FlagReason

flag = ClaimFlag(
    claim_no='SAMPLE-001',
    reason=FlagReason.POTENTIAL_REJECTION_MISSING_AUTH,
    note='Authorization not found in system',
    assessor='John Doe'
)

# Persisted and tracked for dashboard
```

### 6. Excel Export with Formatting

```python
from src.export.excel import ExcelExporter

exporter = ExcelExporter(assessor_name='John Doe')
exporter.add_session_summary(committed_count=15, flags_count=2, avg_minutes=12.5)
exporter.add_flagged_claims(flags_list)
exporter.add_time_logs(claim_times)
exporter.export('output/nhp_session_20260827.xlsx')
```

## Configuration

Create a `.env` file based on `.env.example`:

```bash
# Chatbot Model
CHATBOT_MODEL=llama-2           # or 'mistral', 'neural-chat'
CHATBOT_PROVIDER=ollama         # or 'huggingface'
OLLAMA_BASE_URL=http://localhost:11434
HUGGINGFACE_API_KEY=your_key_here

# Unit Rates (Namibian Dollars)
GP_UNIT_RATE=115.70
ANAESTHETIST_UNIT_RATE=115.50

# ICD-10 ML Model
ICD_MODEL_PATH=models/icd10_model.pkl
ICD_VECTORIZER_PATH=models/tfidf_vectorizer.pkl

# Export Settings
EXPORT_DIR=/content/nhp_exports
```

## Testing

Comprehensive test suite with 50+ test cases:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_anaesthetic.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run only unit tests (exclude integration)
pytest tests/ -m "not integration" -v
```

### Test Coverage

- **Anaesthetic Calculator**: Edge cases (min 6 units, payment factors, rounding)
- **ICD-10 Engine**: Fuzzy matching, ML predictions, database lookups
- **Chatbot**: Context building, rule citations, workflow suggestions
- **Validators**: Discipline checks, modifier validation, rule enforcement
- **Workflow**: State transitions, step completeness, KPI calculations
- **Metrics**: Time tracking, baseline calculation, performance alerts
- **Integration**: Full claim processing pipeline

## Operational Notes

⚠️ **Important**: Rules, tariffs, and sample claims in this application are configurable reference data. **Always confirm current NHP/Universal Healthcare circulars, contracts, authorizations, and tariff schedules before making production determinations.**

### Gazette References

The chatbot's knowledge base includes:
- NHP Benefit Options & Coverage Rules
- Tariff Schedules (NAMAF)
- Anaesthetic Modifier Policies
- Dental EXT Rules (ORS/DPA)
- Discipline Exclusion Lists
- Authorization Requirements

### Multilingual Support

11 languages supported for workflow translation and voice guidance:
English, Afrikaans, isiZulu, isiXhosa, Sesotho, Setswana, Sepedi, isiTsonga, siSwati, Tshivenda, isiNdebele

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see LICENSE file for details.

## Support

For issues, questions, or suggestions, please open a GitHub issue or contact the development team.

---

**Last Updated**: August 2026  
**Version**: 2.0.0 (Refactored with AI Chatbot)  
**Maintainer**: NHP Claims Assessment Team
