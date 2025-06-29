from pathlib import Path

import pytest

from reportlab.pdfgen import canvas

from autofile.core import extract_invoice_details, extract_text_from_pdf


# Fixtures
@pytest.fixture
def sample_text():
    return """
        Invoice number AUDGB-INV-GB-2025-999444555
        Invoice date 20 Jun 2025
        Invoice total GBP 8.99
        Audible Limited
    """


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    sample_text = "Invoice total GBP 5.00"
    pdf_path = tmp_path / "invoice.pdf"

    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 750, sample_text)
    c.save()

    return pdf_path


@pytest.fixture
def sample_invoice_1() -> str:
    return Path("tests/sample-data/text/invoice_01.txt").read_text()


@pytest.fixture
def sample_invoice_2() -> str:
    return Path("tests/sample-data/text/invoice_02.txt").read_text()


# Tests
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
    assert details["reference"] == "AUDGB-INV-GB-2025-999444555"


def test_extract_text_from_pdf(sample_pdf):
    text = extract_text_from_pdf(sample_pdf)
    assert "GBP 5.00" in text


def test_invoice_01_sample_text():
    path = Path("tests/sample-data/invoice_01.txt")
    text = path.read_text()
    assert "Invoice number TEST-INV-0001" in text
    assert "Amount due $24.00 USD" in text
    assert "Vendor1, LLC" in text


def test_invoice_02_sample_text():
    path = Path("tests/sample-data/invoice_02.txt")
    text = path.read_text()
    assert "Invoice number TEST-INV-0002" in text
    assert "Amount due £18.87" in text
    assert "Vendor2 Ltd" in text
