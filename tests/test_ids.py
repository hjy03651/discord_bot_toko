"""Tests for ids.py module."""

import pytest
from ids import increment_alpha


class TestIncrementAlpha:
    """Test cases for increment_alpha function."""

    def test_simple_increment(self):
        """Test simple alpha increments."""
        assert increment_alpha("A") == "B"
        assert increment_alpha("B") == "C"
        assert increment_alpha("Y") == "Z"

    def test_wraparound_single_char(self):
        """Test wraparound from Z to A."""
        assert increment_alpha("Z") == "A"

    def test_multi_char_increment(self):
        """Test multi-character increments."""
        assert increment_alpha("AA") == "AB"
        assert increment_alpha("AZ") == "BA"
        assert increment_alpha("ZZ") == "AA"

    def test_three_char_increment(self):
        """Test three-character increments."""
        assert increment_alpha("AAA") == "AAB"
        assert increment_alpha("AAZ") == "ABA"
        assert increment_alpha("AZZ") == "BAA"
        assert increment_alpha("ZZZ") == "AAA"

    def test_mixed_cases(self):
        """Test various mixed scenarios."""
        assert increment_alpha("ABC") == "ABD"
        assert increment_alpha("XYZ") == "XZA"
        assert increment_alpha("AZZZ") == "BAAA"
