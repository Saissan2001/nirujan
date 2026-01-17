"""Formatting utilities for CLI output."""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple


def format_table(headers: Sequence[str], rows: Iterable[Sequence[str]]) -> str:
    """Create a simple aligned table for console output."""

    rows_list: List[Sequence[str]] = [tuple(row) for row in rows]
    columns = list(zip(*([headers] + rows_list))) if rows_list else [headers]
    col_widths = [max(len(str(cell)) for cell in column) for column in columns]

    def format_row(row: Sequence[str]) -> str:
        return " | ".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))

    separator = "-+-".join("-" * width for width in col_widths)
    table_lines = [format_row(headers), separator]
    for row in rows_list:
        table_lines.append(format_row(row))

    return "\n".join(table_lines)


def format_percentage(value: float) -> str:
    """Format a ratio as a percentage with two decimals."""

    return f"{value * 100:.2f}%"
