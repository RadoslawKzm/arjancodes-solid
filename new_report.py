import pandas as pd

from utils import metrics, readers, writers, filters


class Generator:
    def __init__(
        self,
        reader: readers.Strategy,
        filters_list: list[filters.Strategy],
        metrics_list: list[type[metrics.Strategy]],
        writer: writers.Strategy,
    ):
        self.reader = reader
        self.filters_list = filters_list
        self.metrics_list = metrics_list
        self.writer = writer

    def generate(self):
        report = pd.Series()
        df = self.reader()
        df, report = filters.Strategy.apply(
            filters=self.filters_list,
            df=df,
            report=report,
        )
        report = metrics.Strategy.calculate(
            metrics=self.metrics_list,
            df=df,
            report=report,
        )
        self.writer(report=report)


def main() -> None:
    report = Generator(
        reader=readers.CSVReader(file_path="sales_data.csv"),
        filters_list=[
            filters.DateRange(
                start_date="2024-01-01",
                end_date="2024-12-31",
            )
        ],
        metrics_list=[
            metrics.CustomerCount,
            metrics.AverageOrderValue,
            metrics.ReturnPercentage,
            metrics.TotalSales,
        ],
        writer=writers.JSONWriter(file_path="results.json"),
    )
    report.generate()


if __name__ == "__main__":
    main()
