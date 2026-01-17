"""Publication trends analytics."""

from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable

from dream_book_analyzer.domain.models import BookRecord
from dream_book_analyzer.utils.date_parsing import extract_year


class PublicationTrendsAnalyzer:
    """Analyze counts of books published per year."""

    def analyze(self, records: Iterable[BookRecord]) -> Dict[int, int]:
        counts: Counter[int] = Counter()
        for record in records:
            year = extract_year(record.publication_date)
            if year is None:
                continue
            counts[year] += 1
        return dict(sorted(counts.items()))
