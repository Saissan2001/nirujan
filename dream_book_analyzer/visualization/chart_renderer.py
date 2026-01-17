"""Chart rendering abstractions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, Sequence


class ChartRenderer(ABC):
    """Abstract chart rendering interface."""

    @abstractmethod
    def render_bar(self, title: str, labels: Sequence[str], values: Sequence[int], output_path: Path,
                   x_label: str, y_label: str) -> None:
        """Render a bar chart."""
        raise NotImplementedError

    @abstractmethod
    def render_line(self, title: str, labels: Sequence[str], values: Sequence[int], output_path: Path,
                    x_label: str, y_label: str) -> None:
        """Render a line chart."""
        raise NotImplementedError

    @abstractmethod
    def render_pie(self, title: str, labels: Sequence[str], values: Sequence[int], output_path: Path) -> None:
        """Render a pie chart."""
        raise NotImplementedError

    @abstractmethod
    def render_multi_series_bar(
        self,
        title: str,
        x_labels: Sequence[str],
        series: Iterable[tuple[str, Sequence[int]]],
        output_path: Path,
        x_label: str,
        y_label: str,
    ) -> None:
        """Render a grouped bar chart for multiple series."""
        raise NotImplementedError

    @abstractmethod
    def render_multi_series_line(
        self,
        title: str,
        x_labels: Sequence[str],
        series: Iterable[tuple[str, Sequence[int]]],
        output_path: Path,
        x_label: str,
        y_label: str,
    ) -> None:
        """Render a multi-series line chart."""
        raise NotImplementedError
