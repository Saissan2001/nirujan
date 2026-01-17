"""Application entry point for Dream Book Shop Data Analyzer."""

from __future__ import annotations

from pathlib import Path

from dream_book_analyzer.analytics.language_distribution import LanguageDistributionAnalyzer
from dream_book_analyzer.analytics.missing_isbn import MissingIsbnAnalyzer
from dream_book_analyzer.analytics.publication_trends import PublicationTrendsAnalyzer
from dream_book_analyzer.analytics.publisher_counts import PublisherCountsAnalyzer
from dream_book_analyzer.analytics.top_authors import TopAuthorsAnalyzer
from dream_book_analyzer.analytics.year_language import YearLanguageAnalyzer
from dream_book_analyzer.cli.menu import MenuController
from dream_book_analyzer.data.csv_repository import CsvBookRepository
from dream_book_analyzer.visualization.matplotlib_renderer import MatplotlibChartRenderer


DATASET_FILENAME = "Dataset Books.csv"


def main() -> None:
    """Bootstrap dependencies and start the CLI menu."""
    dataset_path = Path(DATASET_FILENAME)
    repository = CsvBookRepository(dataset_path)
    output_dir = Path("output")

    chart_renderer = MatplotlibChartRenderer(output_dir)

    analyzers = {
        "publication_trends": PublicationTrendsAnalyzer(),
        "top_authors": TopAuthorsAnalyzer(),
        "language_distribution": LanguageDistributionAnalyzer(),
        "publisher_counts": PublisherCountsAnalyzer(),
        "missing_isbn": MissingIsbnAnalyzer(),
        "year_language": YearLanguageAnalyzer(),
    }

    menu = MenuController(repository, analyzers, chart_renderer)
    menu.run()


if __name__ == "__main__":
    main()
