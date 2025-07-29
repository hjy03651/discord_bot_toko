"""Tests for embedding.py module."""

import pytest
from unittest.mock import MagicMock, patch
import discord
from embedding import pagination, get_embed


class TestPagination:
    """Test cases for pagination function."""

    def test_single_page(self):
        """Test pagination with results fitting in one page."""
        query = "test"
        result = [
            ("ID1", "Book 1", "1", "A1", "대출가능"),
            ("ID2", "Book 2", "2", "A2", "대출중"),
        ]

        embeds = pagination(query, result)

        assert len(embeds) == 1
        assert embeds[0].title == "test에 대한 검색 결과 (1–2/2)"
        assert len(embeds[0].fields) == 2

    def test_multiple_pages(self):
        """Test pagination with results spanning multiple pages."""
        query = "test"
        # Create 25 dummy results
        result = [
            (f"ID{i}", f"Book {i}", str(i), f"A{i}", "대출가능") for i in range(1, 26)
        ]

        embeds = pagination(query, result)

        assert len(embeds) == 3
        assert embeds[0].title == "test에 대한 검색 결과 (1–10/25)"
        assert embeds[1].title == "test에 대한 검색 결과 (11–20/25)"
        assert embeds[2].title == "test에 대한 검색 결과 (21–25/25)"
        assert len(embeds[0].fields) == 10
        assert len(embeds[1].fields) == 10
        assert len(embeds[2].fields) == 5

    def test_empty_results(self):
        """Test pagination with empty results."""
        query = "test"
        result = []

        embeds = pagination(query, result)

        assert len(embeds) == 0


class TestGetEmbed:
    """Test cases for get_embed function."""

    def test_default_embed(self):
        """Test default embed creation."""
        embed = get_embed("Test description")

        assert embed.description == "Test description"
        assert embed.title is None
        assert embed.color.value == 0x23A55A

    def test_error_embed_without_title(self):
        """Test error embed without custom title."""
        embed = get_embed("Error description", error=True)

        assert embed.description == "Error description"
        assert embed.title == "오류가 발생했습니다."
        assert embed.color.value == 0xDB5060

    def test_error_embed_with_title(self):
        """Test error embed with custom title."""
        embed = get_embed("Error description", error=True, title="Custom Error")

        assert embed.description == "Error description"
        assert embed.title == "Custom Error"
        assert embed.color.value == 0xDB5060

    def test_pumpkin_cultivation_color(self):
        """Test special color for pumpkin cultivation."""
        embed = get_embed("Description", title="호박 재배 중입니다")

        assert embed.color.value == 0xDB810B

    def test_special_pumpkin_color(self):
        """Test special color for special pumpkin titles."""
        embed1 = get_embed("Description", title="호박(?) 재배")
        embed2 = get_embed("Description", title="호...호 불면은")

        assert embed1.color.value == 0x77B255
        assert embed2.color.value == 0x77B255

    def test_bug_cultivation_color(self):
        """Test special color for bug cultivation."""
        embed = get_embed("Description", title="벌레 재배")

        assert embed.color.value == 0x844823

    def test_custom_title_default_color(self):
        """Test custom title with default color."""
        embed = get_embed("Description", title="Custom Title")

        assert embed.title == "Custom Title"
        assert embed.color.value == 0x23A55A
