"""Year and language breakdown analytics."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Dict, Iterable

from dream_book_analyzer.domain.models import BookRecord
from dream_book_analyzer.utils.date_parsing import extract_year


class YearLanguageAnalyzer:
    """Analyze the number of books per year categorized by language."""

    def analyze(self, records: Iterable[BookRecord]) -> Dict[int, Dict[str, int]]:
        year_language_counts: Dict[int, Counter[str]] = defaultdict(Counter)
        for record in records:
            year = extract_year(record.publication_date)
            if year is None:
                continue
            language = record.language or "Unknown"
            year_language_counts[year][language] += 1

        sorted_counts: Dict[int, Dict[str, int]] = {}
        for year in sorted(year_language_counts.keys()):
            sorted_counts[year] = dict(year_language_counts[year])

        return sorted_counts
