"""Tests for validators."""

import pytest
from src.core.validators import validate_discipline, validate_modifier_code, validate_ext_rule


class TestValidators:
    """Test validation functions."""

    def test_valid_discipline_not_excluded(self):
        """Test validation of non-excluded discipline."""
        is_valid, msg = validate_discipline('04')
        assert is_valid is True
        assert 'valid' in msg.lower()

    def test_excluded_discipline_detected(self):
        """Test detection of excluded disciplines."""
        is_valid, msg = validate_discipline('37')
        assert is_valid is False
        assert 'exclusion' in msg.lower()

    def test_excluded_disciplines_list(self):
        """Test all excluded disciplines are caught."""
        excluded = ['10', '25', '26', '27', '37', '38', '39', '40', '52', '54', '62', '63', '64', '68']
        for disc in excluded:
            is_valid, _ = validate_discipline(disc)
            assert is_valid is False

    def test_empty_discipline(self):
        """Test empty discipline code."""
        is_valid, msg = validate_discipline('')
        assert is_valid is False
        assert 'required' in msg.lower()

    def test_valid_modifier_codes(self):
        """Test valid modifier codes."""
        for code in ['0036', '0023', '0038', '0039']:
            is_valid, msg = validate_modifier_code(code)
            assert is_valid is True
            assert 'valid' in msg.lower()

    def test_invalid_modifier_code(self):
        """Test invalid modifier code."""
        is_valid, msg = validate_modifier_code('9999')
        assert is_valid is False
        assert 'invalid' in msg.lower()

    def test_ext_rule_non_dental(self):
        """Test EXT rule for non-dental claim."""
        is_valid, msg = validate_ext_rule(25, False)
        assert is_valid is True
        assert 'not a dental' in msg.lower()

    def test_ext_rule_dental_under_10(self):
        """Test EXT rule for dental claim under 10."""
        is_valid, msg = validate_ext_rule(9, True)
        assert is_valid is True
        assert 'ORS' in msg

    def test_ext_rule_dental_10_and_over(self):
        """Test EXT rule for dental claim age 10+."""
        is_valid, msg = validate_ext_rule(15, True)
        assert is_valid is True
        assert 'DPA' in msg
