import pytest

from autofile.core import extract_invoice_details


@pytest.fixture
def sample_text():
    return """
        Invoice number AUDGB-INV-GB-2025-22768692
        Invoice date 20 Jun 2025
        Invoice total GBP 8.99
        Audible Limited
    """


def test_extracts_date(sample_text):
    details = extract_invoice_details(sample_text)
    assert details["date"] == "2025-06-20"


def test_extracts_price(sample_text):
    details = extract_invoice_details(sample_text)
    assert details["price"] == "8.99"


def test_extracts_vendor(sample_text):
    details = extract_invoice_details(sample_text)
    assert details["vendor"] == "Audible"


def test_extracts_reference(sample_text):
    details = extract_invoice_details(sample_text)
    assert details["reference"] == "AUDGB-INV-GB-2025-22768692"
