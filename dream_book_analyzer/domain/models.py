"""Domain models for the Dream Book Shop Data Analyzer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class BookRecord:
    """Represents a single book record from the dataset."""

    book: str
    author: str
    publication_date: str
    language: str
    book_publisher: str
    isbn: Optional[str]
    bnb_id: str
