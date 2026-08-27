# CHANGELOG.md

## [2.0.0] - 2026-08-27

### Added
- **AI Chatbot Module**: Ollama/Hugging Face LLM integration with Gazette references
- **Rules Knowledge Base**: NHP Gazette rules and tariff references for chatbot
- **Workflow Guidance Engine**: Context-aware workflow suggestions
- **Refactored Architecture**: Modular, maintainable code structure
- **Comprehensive Test Suite**: 50+ test cases covering all modules
- **FastAPI Web Service**: RESTful API endpoints for all functionality
- **CLI Application**: Command-line interface for all operations
- **Excel Export**: Formatted workbooks with KPI summaries
- **Metrics Tracking**: Enhanced productivity tracking with baseline calculations
- **Claim Processing Orchestrator**: Full validation pipeline

### Changed
- Reorganized code into logical modules (core, chatbot, claims, tracking, export)
- Improved error handling and validation
- Enhanced configuration management with dotenv support

### Fixed
- Anaesthetic modifier calculation edge cases
- ICD-10 search fuzzy matching accuracy
- Time tracking baseline calculation

### Improved
- Code documentation and docstrings
- Type hints throughout codebase
- Test coverage to >85%

## [1.0.0] - 2026-06-15

### Initial Release
- Google Colab notebook implementation
- 7-step workflow checklist
- Anaesthetic modifier calculations
- ICD-10 fuzzy search
- PDF invoice processing with OCR
- Productivity dashboard
- Excel export functionality
