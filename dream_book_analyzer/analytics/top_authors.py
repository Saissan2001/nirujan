"""Top authors analytics."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, List, Tuple

from dream_book_analyzer.domain.models import BookRecord


class TopAuthorsAnalyzer:
    """Identify the most prolific authors in the dataset."""

    def analyze(self, records: Iterable[BookRecord], limit: int = 5) -> List[Tuple[str, int]]:
        counts: Counter[str] = Counter()
        for record in records:
            author = record.author or "Unknown"
            counts[author] += 1
        return counts.most_common(limit)
