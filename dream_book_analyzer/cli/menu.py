"""CLI menu controller for running analyses."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence

from dream_book_analyzer.analytics.language_distribution import LanguageDistributionAnalyzer
from dream_book_analyzer.analytics.missing_isbn import MissingIsbnAnalyzer
from dream_book_analyzer.analytics.publication_trends import PublicationTrendsAnalyzer
from dream_book_analyzer.analytics.publisher_counts import PublisherCountsAnalyzer
from dream_book_analyzer.analytics.top_authors import TopAuthorsAnalyzer
from dream_book_analyzer.analytics.year_language import YearLanguageAnalyzer
from dream_book_analyzer.data.repository import BookRepository
from dream_book_analyzer.domain.models import BookRecord
from dream_book_analyzer.utils.formatting import format_percentage, format_table
from dream_book_analyzer.visualization.chart_renderer import ChartRenderer


class MenuController:
    """Command-line menu controller."""

    def __init__(
        self,
        repository: BookRepository,
        analyzers: Dict[str, object],
        chart_renderer: ChartRenderer,
    ) -> None:
        self._repository = repository
        self._chart_renderer = chart_renderer
        self._analyzers = analyzers
        self._records = self._repository.list_books()

        self._menu_actions: Dict[str, Callable[[], None]] = {
            "1": self._publication_trends,
            "2": self._top_authors,
            "3": self._language_distribution,
            "4": self._publisher_counts,
            "5": self._missing_isbn,
            "6": self._year_language,
        }

    def run(self) -> None:
        """Start the CLI loop."""
        while True:
            print("\nDream Book Shop Data Analyzer")
            print("1) Publication Trends Over Time")
            print("2) Top 5 Most Prolific Authors")
            print("3) Language Distribution")
            print("4) Number of books published by each publisher")
            print("5) Missing ISBN Analysis")
            print("6) Number of books per year categorized by language")
            print("0) Exit")

            choice = input("Select an option: ").strip()
            if choice == "0":
                print("Goodbye!")
                break

            action = self._menu_actions.get(choice)
            if action:
                action()
            else:
                print("Invalid selection. Please choose a valid option.")

    def _prompt_chart_generation(self) -> bool:
        response = input("Generate chart? (y/n): ").strip().lower()
        return response == "y"

    def _prompt_chart_type(self, allowed: Sequence[str]) -> Optional[str]:
        options_text = "/".join(allowed)
        response = input(f"Select chart type ({options_text}): ").strip().lower()
        if response in allowed:
            return response
        print("Invalid chart type selected. Skipping chart generation.")
        return None

    def _publication_trends(self) -> None:
        analyzer: PublicationTrendsAnalyzer = self._analyzers["publication_trends"]
        results = analyzer.analyze(self._records)
        if not results:
            print("No valid publication years found.")
            return

        rows = [(str(year), str(count)) for year, count in results.items()]
        print("\nPublication Trends Over Time")
        print(format_table(["Year", "Count"], rows))

        if self._prompt_chart_generation():
            chart_type = self._prompt_chart_type(["bar", "line", "pie"])
            if chart_type:
                labels = [str(year) for year in results.keys()]
                values = list(results.values())
                self._render_single_series_chart(
                    chart_type,
                    "Publication Trends Over Time",
                    labels,
                    values,
                    Path("publication_trends.png"),
                    x_label="Year",
                    y_label="Books Published",
                )

    def _top_authors(self) -> None:
        analyzer: TopAuthorsAnalyzer = self._analyzers["top_authors"]
        results = analyzer.analyze(self._records)
        rows = [(author, str(count)) for author, count in results]

        print("\nTop 5 Most Prolific Authors")
        print(format_table(["Author", "Books"], rows))

        if self._prompt_chart_generation():
            chart_type = self._prompt_chart_type(["bar", "line", "pie"])
            if chart_type:
                labels = [author for author, _ in results]
                values = [count for _, count in results]
                self._render_single_series_chart(
                    chart_type,
                    "Top 5 Most Prolific Authors",
                    labels,
                    values,
                    Path("top_authors.png"),
                    x_label="Author",
                    y_label="Books",
                )

    def _language_distribution(self) -> None:
        analyzer: LanguageDistributionAnalyzer = self._analyzers["language_distribution"]
        results = analyzer.analyze(self._records)
        rows = [(language, str(count), format_percentage(percentage)) for language, count, percentage in results]

        print("\nLanguage Distribution")
        print(format_table(["Language", "Count", "Percentage"], rows))

        if self._prompt_chart_generation():
            chart_type = self._prompt_chart_type(["bar", "line", "pie"])
            if chart_type:
                labels = [language for language, _, _ in results]
                values = [count for _, count, _ in results]
                self._render_single_series_chart(
                    chart_type,
                    "Language Distribution",
                    labels,
                    values,
                    Path("language_distribution.png"),
                    x_label="Language",
                    y_label="Books",
                )

    def _publisher_counts(self) -> None:
        analyzer: PublisherCountsAnalyzer = self._analyzers["publisher_counts"]
        results = analyzer.analyze(self._records)
        rows = [(publisher, str(count)) for publisher, count in results]

        print("\nBooks Published by Each Publisher")
        print(format_table(["Publisher", "Books"], rows))

        if self._prompt_chart_generation():
            chart_type = self._prompt_chart_type(["bar", "line", "pie"])
            if chart_type:
                labels = [publisher for publisher, _ in results]
                values = [count for _, count in results]
                self._render_single_series_chart(
                    chart_type,
                    "Books Published by Each Publisher",
                    labels,
                    values,
                    Path("publisher_counts.png"),
                    x_label="Publisher",
                    y_label="Books",
                )

    def _missing_isbn(self) -> None:
        analyzer: MissingIsbnAnalyzer = self._analyzers["missing_isbn"]
        missing, total, percentage = analyzer.analyze(self._records)

        print("\nMissing ISBN Analysis")
        print(f"Missing ISBNs: {missing}")
        print(f"Total Records: {total}")
        print(f"Percentage Missing: {format_percentage(percentage)}")

        if self._prompt_chart_generation():
            chart_type = self._prompt_chart_type(["bar", "pie"])
            if chart_type:
                labels = ["Missing ISBN", "Has ISBN"]
                values = [missing, total - missing]
                if chart_type == "bar":
                    self._chart_renderer.render_bar(
                        "Missing ISBN Analysis",
                        labels,
                        values,
                        Path("missing_isbn.png"),
                        x_label="Status",
                        y_label="Books",
                    )
                elif chart_type == "pie":
                    self._chart_renderer.render_pie(
                        "Missing ISBN Analysis",
                        labels,
                        values,
                        Path("missing_isbn.png"),
                    )

    def _year_language(self) -> None:
        analyzer: YearLanguageAnalyzer = self._analyzers["year_language"]
        results = analyzer.analyze(self._records)
        if not results:
            print("No valid publication years found for language breakdown.")
            return

        years = sorted(results.keys())
        languages = sorted({language for counts in results.values() for language in counts.keys()})

        rows: List[Sequence[str]] = []
        for year in years:
            row = [str(year)]
            for language in languages:
                row.append(str(results[year].get(language, 0)))
            rows.append(row)

        print("\nBooks per Year by Language")
        print(format_table(["Year", *languages], rows))

        if self._prompt_chart_generation():
            chart_type = self._prompt_chart_type(["bar", "line"])
            if chart_type:
                series = []
                for language in languages:
                    series_values = [results[year].get(language, 0) for year in years]
                    series.append((language, series_values))

                if chart_type == "bar":
                    self._chart_renderer.render_multi_series_bar(
                        "Books per Year by Language",
                        [str(year) for year in years],
                        series,
                        Path("year_language_bar.png"),
                        x_label="Year",
                        y_label="Books",
                    )
                elif chart_type == "line":
                    self._chart_renderer.render_multi_series_line(
                        "Books per Year by Language",
                        [str(year) for year in years],
                        series,
                        Path("year_language_line.png"),
                        x_label="Year",
                        y_label="Books",
                    )

    def _render_single_series_chart(
        self,
        chart_type: str,
        title: str,
        labels: Iterable[str],
        values: Iterable[int],
        filename: Path,
        x_label: str,
        y_label: str,
    ) -> None:
        labels_list = list(labels)
        values_list = list(values)
        if chart_type == "bar":
            self._chart_renderer.render_bar(title, labels_list, values_list, filename, x_label, y_label)
        elif chart_type == "line":
            self._chart_renderer.render_line(title, labels_list, values_list, filename, x_label, y_label)
        elif chart_type == "pie":
            self._chart_renderer.render_pie(title, labels_list, values_list, filename)
