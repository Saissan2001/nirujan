"""Missing ISBN analytics."""

from __future__ import annotations

from typing import Iterable, Tuple

from dream_book_analyzer.domain.models import BookRecord


class MissingIsbnAnalyzer:
    """Analyze missing ISBN values."""

    def analyze(self, records: Iterable[BookRecord]) -> Tuple[int, int, float]:
        total = 0
        missing = 0
        for record in records:
            total += 1
            isbn = record.isbn
            if isbn is None or not str(isbn).strip():
                missing += 1
        percentage = missing / total if total else 0
        return missing, total, percentage
