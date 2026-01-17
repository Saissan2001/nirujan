"""Utilities for parsing publication dates."""

from __future__ import annotations

import re
from typing import Optional

YEAR_PATTERN = re.compile(r"(\d{4})")


def extract_year(date_value: str) -> Optional[int]:
    """Extract a four-digit year from the publication date string."""

    if not date_value:
        return None
    match = YEAR_PATTERN.search(date_value)
    if not match:
        return None
    year = int(match.group(1))
    if year <= 0:
        return None
    return year
