import abc
import pandas as pd

WRITER_NAME = str
REPORT = pd.Series


class Strategy(abc.ABC):
    registry: dict[WRITER_NAME, type["Strategy"]] = {}

    def __init__(self, file_path: str):
        self.file_path = file_path

    @classmethod
    def __init_subclass__(cls, **kwargs):
        Strategy.registry[cls.__name__.lower()] = cls

    def __call__(self, report:REPORT):
        return self.write(report=report)

    @abc.abstractmethod
    def write(self, *, report:REPORT):
        pass


class CSVWriter(Strategy):
    def __init__(self, file_path: str):
        super().__init__(file_path=file_path)

    def write(self, *, report:REPORT):
        pd.DataFrame.to_csv(report, self.file_path)


class ExcelWriter(Strategy):
    def __init__(self, file_path: str):
        super().__init__(file_path=file_path)

    def write(self, *, report:REPORT):
        pd.DataFrame.to_excel(report, self.file_path)


class JSONWriter(Strategy):
    def __init__(self, file_path: str):
        super().__init__(file_path=file_path)

    def write(self, *, report:REPORT):
        pd.DataFrame.to_json(report, self.file_path)
