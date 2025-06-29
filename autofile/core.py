import re

from datetime import datetime
from pathlib import Path

import pdfplumber


def extract_invoice_details(text: str) -> dict[str, str | None]:
    date_pattern = r"(\d{1,2} \w{3,9} \d{4})"
    price_pattern = r"(?:GBP|£)\s?(\d+\.\d{2})"
    reference_pattern = (
        r"(?:Invoice|Bill)\s*(?:#|number|reference)?\s*[:\-]?\s*([A-Z0-9\-]+)"
    )

    date_match = re.search(date_pattern, text)
    price_match = re.search(price_pattern, text)
    ref_match = re.search(reference_pattern, text)

    invoice_date = None
    if date_match:
        try:
            invoice_date = datetime.strptime(
                date_match.group(1), "%d %b %Y"
            ).strftime("%Y-%m-%d")
        except ValueError:
            pass

    vendor = next(
        (
            line.strip()
            for line in text.splitlines()
            if "Limited" in line and "SAGE PANDA" not in line
        ),
        "UnknownVendor",
    ).split()[0]

    return {
        "date": invoice_date,
        "price": price_match.group(1) if price_match else None,
        "vendor": vendor,
        "reference": ref_match.group(1) if ref_match else None,
    }


def extract_text_from_pdf(pdf_path: Path) -> str:
    try:
        with pdfplumber.open(pdf_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception as e:
        # Optional: log or re-raise depending on your error handling approach
        raise RuntimeError(f"Failed to extract text from {pdf_path}") from e
