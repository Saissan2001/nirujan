"""Publisher counts analytics."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, List, Tuple

from dream_book_analyzer.domain.models import BookRecord


class PublisherCountsAnalyzer:
    """Count books published by each publisher."""

    def analyze(self, records: Iterable[BookRecord]) -> List[Tuple[str, int]]:
        counts: Counter[str] = Counter()
        for record in records:
            publisher = record.book_publisher or "Unknown"
            counts[publisher] += 1
        return counts.most_common()
