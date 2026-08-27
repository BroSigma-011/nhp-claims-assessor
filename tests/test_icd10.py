"""Tests for ICD-10 engine."""

import pytest
from src.core.icd10 import ICDEngine


class TestICDEngine:
    """Test ICD-10 search and prediction."""

    def test_icd_engine_initialization(self, icd_engine):
        """Test engine initializes with reference data."""
        assert icd_engine.icd_df is not None
        assert len(icd_engine.icd_df) > 0

    def test_search_by_code(self, icd_engine):
        """Test search by exact code."""
        results = icd_engine.search('J01.90', limit=5)
        assert not results.empty
        assert 'J01.90' in results['code'].values

    def test_search_by_description(self, icd_engine):
        """Test search by description keyword."""
        results = icd_engine.search('sinusitis', limit=5)
        assert not results.empty
        assert any('sinusitis' in str(desc).lower() for desc in results['description'])

    def test_search_fuzzy_matching(self, icd_engine):
        """Test fuzzy matching for partial matches."""
        results = icd_engine.search('sinus', limit=5)
        assert not results.empty

    def test_lookup_code_found(self, icd_engine):
        """Test lookup of existing code."""
        result = icd_engine.lookup_code('J01.90')
        assert result is not None
        assert result['code'] == 'J01.90'
        assert 'description' in result

    def test_lookup_code_not_found(self, icd_engine):
        """Test lookup of non-existing code."""
        result = icd_engine.lookup_code('ZZZ.99')
        assert result is None

    def test_search_empty_query(self, icd_engine):
        """Test search with empty query returns all."""
        results = icd_engine.search('', limit=5)
        assert not results.empty
        assert len(results) <= 5

    def test_reference_data_retrieval(self, icd_engine):
        """Test retrieving all reference data."""
        data = icd_engine.get_reference_data()
        assert not data.empty
        assert 'code' in data.columns
        assert 'description' in data.columns
