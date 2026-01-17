"""CSV-backed repository implementation."""

from __future__ import annotations

from pathlib import Path
from typing import List

import pandas as pd

from dream_book_analyzer.data.repository import BookRepository
from dream_book_analyzer.domain.models import BookRecord


class CsvBookRepository(BookRepository):
    """Loads book records from a CSV file."""

    REQUIRED_COLUMNS = {
        "book",
        "author",
        "publication date",
        "language",
        "book publisher",
        "ISBN",
        "BNB id",
    }

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def list_books(self) -> List[BookRecord]:
        if not self._file_path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {self._file_path}. Ensure 'Dataset Books.csv' is present."
            )

        dataframe = pd.read_csv(self._file_path)
        missing_columns = self.REQUIRED_COLUMNS.difference(dataframe.columns)
        if missing_columns:
            missing_list = ", ".join(sorted(missing_columns))
            raise ValueError(f"Missing required columns in dataset: {missing_list}")

        records: List[BookRecord] = []
        for _, row in dataframe.iterrows():
            record = BookRecord(
                book=str(row.get("book", "")).strip(),
                author=str(row.get("author", "")).strip(),
                publication_date=str(row.get("publication date", "")).strip(),
                language=str(row.get("language", "")).strip(),
                book_publisher=str(row.get("book publisher", "")).strip(),
                isbn=None if pd.isna(row.get("ISBN")) else str(row.get("ISBN")).strip(),
                bnb_id=str(row.get("BNB id", "")).strip(),
            )
            records.append(record)

        return records
