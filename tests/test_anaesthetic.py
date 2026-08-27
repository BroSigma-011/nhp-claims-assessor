"""Tests for anaesthetic modifier calculator."""

import pytest
from src.core.anaesthetic import calculate_modifier


class TestModifierCalculation:
    """Test anaesthetic modifier calculations."""

    def test_code_0036_30_minutes(self):
        """Test code 0036 with 30 minutes (2 quarters)."""
        result = calculate_modifier('0036', 30, 1000.00)
        assert result.code == '0036'
        assert result.minutes == 30
        assert result.rounded_15_min_units == 2
        assert result.units == 6  # Minimum units
        assert result.payment_factor == 0.82
        assert result.modifier_payment == round(6 * 115.50 * 0.82, 2)

    def test_code_0023_60_minutes(self):
        """Test code 0023 with 60 minutes (full hour)."""
        result = calculate_modifier('0023', 60, 500.00)
        assert result.code == '0023'
        assert result.rounded_15_min_units == 4  # 4 quarters in 1 hour
        assert result.units == max(2 * 4, 6)  # 8 units, exceeds minimum
        assert result.payment_factor == 1.00
        assert result.modifier_payment == result.gross_units_value

    def test_code_0036_45_minutes(self):
        """Test code 0036 with 45 minutes (3 quarters)."""
        result = calculate_modifier('0036', 45, 1000.00)
        assert result.code == '0036'
        assert result.rounded_15_min_units == 3
        assert result.units == 6  # 2*3 = 6, meets minimum
        assert result.payment_factor == 0.82

    def test_code_0036_90_minutes(self):
        """Test code 0036 with 90 minutes (90/15 = 6 quarters, 4+2 later)."""
        result = calculate_modifier('0036', 90, 1200.00)
        assert result.code == '0036'
        assert result.rounded_15_min_units == 6
        # 2*4 (first hour) + 3*2 (later) = 8 + 6 = 14 units
        assert result.units == 14
        assert result.payment_factor == 0.82

    def test_minimum_units_enforcement(self):
        """Test that minimum 6 units is enforced."""
        result = calculate_modifier('0023', 5, 300.00)
        assert result.units == 6
        assert result.rounded_15_min_units == 1

    def test_gp_provider_rate(self):
        """Test GP provider uses correct unit rate."""
        result = calculate_modifier('0036', 60, 1000.00, provider='GP')
        assert result.unit_rate == 115.70
        gp_gross = 8 * 115.70
        assert result.gross_units_value == round(gp_gross, 2)

    def test_invalid_code_raises_error(self):
        """Test that invalid code raises ValueError."""
        with pytest.raises(ValueError, match='Supported codes are'):
            calculate_modifier('9999', 60, 1000.00)

    def test_negative_minutes_raises_error(self):
        """Test that negative minutes raises ValueError."""
        with pytest.raises(ValueError, match='Minutes must be positive'):
            calculate_modifier('0036', -30, 1000.00)

    def test_negative_tariff_raises_error(self):
        """Test that negative tariff raises ValueError."""
        with pytest.raises(ValueError, match='Base tariff cannot be negative'):
            calculate_modifier('0036', 60, -1000.00)

    def test_total_claim_value(self):
        """Test total claim value calculation."""
        result = calculate_modifier('0023', 60, 500.00)
        expected_total = 500.00 + result.modifier_payment
        assert result.total_claim_value == round(expected_total, 2)

    def test_rounding_accuracy(self):
        """Test rounding to 2 decimal places."""
        result = calculate_modifier('0036', 33, 777.77)
        assert isinstance(result.modifier_payment, float)
        assert len(str(result.modifier_payment).split('.')[-1]) <= 2
