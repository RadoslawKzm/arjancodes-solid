import abc
import pandas as pd


READER_NAME = str


class Strategy(abc.ABC):
    registry: dict[READER_NAME, type["Strategy"]] = {}

    def __init__(self, file_path: str):
        self.file_path = file_path

    @classmethod
    def __init_subclass__(cls, **kwargs):
        Strategy.registry[cls.__name__.lower()] = cls

    def __call__(self):
        """Simple call method as `reader` name is self-explanatory"""
        return self.read()

    @abc.abstractmethod
    def read(self) -> pd.DataFrame:
        pass


class CSVReader(Strategy):
    def __init__(self, file_path: str):
        super().__init__(file_path=file_path)

    def read(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, parse_dates=["date"])


class ExcelReader(Strategy):
    def __init__(self, file_path: str):
        super().__init__(file_path=file_path)

    def read(self) -> pd.DataFrame:
        return pd.read_excel(self.file_path)


class JSONReader(Strategy):
    def __init__(self, file_path: str):
        super().__init__(file_path=file_path)

    def read(self) -> pd.DataFrame:
        return pd.read_json(self.file_path)
