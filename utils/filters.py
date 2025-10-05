import abc
import datetime

import pandas as pd

FILTER_NAME = str
DATA_FRAME = pd.DataFrame
REPORT = pd.Series


class Strategy(abc.ABC):
    registry: dict[str, type["Strategy"]] = {}

    def __init__(self):
        pass

    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.registry[cls.__name__.lower()] = cls

    @classmethod
    def apply(
        cls,
        *,
        filters: list["Strategy"],
        df: DATA_FRAME,
        report: REPORT,
    ):
        for _filter in filters:
            df = _filter.apply_filter(df=df, report=report)
        return df

    @abc.abstractmethod
    def apply_filter(self, *, df: DATA_FRAME, report: REPORT):
        pass


class DateRange(Strategy):
    def __init__(
        self,
        start_date: str = None,
        end_date: str = None,
    ):
        if start_date and end_date:
            try:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date

    def apply_filter(
        self,
        *,
        df: DATA_FRAME,
        report: REPORT,
    ) -> tuple[DATA_FRAME, REPORT]:
        report["report_start"] = r"N/A"
        report["report_end"] = r"N/A"
        if self.start_date:
            df = df[df["date"] >= pd.Timestamp(self.start_date)]
            report["report_start"] = self.start_date.strftime("%Y-%m-%d")
        if self.end_date:
            df = df[df["date"] <= pd.Timestamp(self.end_date)]
            report["report_end"] = self.end_date.strftime("%Y-%m-%d")
        return df, report
