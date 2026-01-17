"""Repository abstractions for book data."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from dream_book_analyzer.domain.models import BookRecord


class BookRepository(ABC):
    """Abstract repository interface for book data."""

    @abstractmethod
    def list_books(self) -> List[BookRecord]:
        """Return all book records from the data source."""
        raise NotImplementedError
