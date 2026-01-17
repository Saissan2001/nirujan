"""Matplotlib chart renderer implementation."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np

from dream_book_analyzer.visualization.chart_renderer import ChartRenderer


class MatplotlibChartRenderer(ChartRenderer):
    """Render charts using Matplotlib."""

    def __init__(self, output_dir: Path) -> None:
        self._output_dir = output_dir
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def render_bar(
        self,
        title: str,
        labels: Sequence[str],
        values: Sequence[int],
        output_path: Path,
        x_label: str,
        y_label: str,
    ) -> None:
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        self._save(output_path)

    def render_line(
        self,
        title: str,
        labels: Sequence[str],
        values: Sequence[int],
        output_path: Path,
        x_label: str,
        y_label: str,
    ) -> None:
        plt.figure(figsize=(10, 6))
        plt.plot(labels, values, marker="o")
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        self._save(output_path)

    def render_pie(self, title: str, labels: Sequence[str], values: Sequence[int], output_path: Path) -> None:
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        plt.title(title)
        plt.tight_layout()
        self._save(output_path)

    def render_multi_series_bar(
        self,
        title: str,
        x_labels: Sequence[str],
        series: Iterable[tuple[str, Sequence[int]]],
        output_path: Path,
        x_label: str,
        y_label: str,
    ) -> None:
        plt.figure(figsize=(12, 7))
        indices = np.arange(len(x_labels))
        series_list = list(series)
        bar_width = 0.8 / max(len(series_list), 1)

        for index, (name, values) in enumerate(series_list):
            positions = indices + index * bar_width
            plt.bar(positions, values, width=bar_width, label=name)

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(indices + bar_width * (len(series_list) - 1) / 2, x_labels, rotation=45, ha="right")
        plt.legend()
        plt.tight_layout()
        self._save(output_path)

    def render_multi_series_line(
        self,
        title: str,
        x_labels: Sequence[str],
        series: Iterable[tuple[str, Sequence[int]]],
        output_path: Path,
        x_label: str,
        y_label: str,
    ) -> None:
        plt.figure(figsize=(12, 7))
        for name, values in series:
            plt.plot(x_labels, values, marker="o", label=name)

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(rotation=45, ha="right")
        plt.legend()
        plt.tight_layout()
        self._save(output_path)

    def _save(self, output_path: Path) -> None:
        full_path = self._output_dir / output_path
        plt.savefig(full_path)
        plt.close()
