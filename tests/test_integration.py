"""
Integration tests — require real AWS credentials and live AWS services.

Run with: poetry run pytest tests/test_integration.py -v
Skip with: poetry run pytest tests/ --ignore=tests/test_integration.py
"""
import pytest


@pytest.mark.integration
def test_placeholder_integration():
    """Placeholder: replace with real integration tests when AWS credentials are available."""
    pytest.skip("Integration tests require real AWS credentials — skipping in CI.")
