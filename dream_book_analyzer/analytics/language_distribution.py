"""Language distribution analytics."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, List, Tuple

from dream_book_analyzer.domain.models import BookRecord


class LanguageDistributionAnalyzer:
    """Calculate counts and percentages by language."""

    def analyze(self, records: Iterable[BookRecord]) -> List[Tuple[str, int, float]]:
        counts: Counter[str] = Counter()
        total = 0
        for record in records:
            language = record.language or "Unknown"
            counts[language] += 1
            total += 1

        results: List[Tuple[str, int, float]] = []
        for language, count in counts.most_common():
            percentage = count / total if total else 0
            results.append((language, count, percentage))

        return results
