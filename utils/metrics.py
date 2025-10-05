import abc
import pandas as pd

METRIC_NAME = str
DATA_FRAME = pd.DataFrame
REPORT = pd.Series


class Strategy(abc.ABC):
    registry: dict[METRIC_NAME, "Strategy"] = {}
    report_var_name: str = ""

    def __init__(self):
        pass

    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.registry[cls.__name__.lower()] = cls()

    @classmethod
    def calculate(
        cls,
        *,
        metrics: list[type["Strategy"]],
        df: DATA_FRAME,
        report: REPORT,
    ) -> REPORT:
        for metric in metrics:
            result = metric().compute(df=df)
            report[metric.report_var_name] = result
        return report

    @abc.abstractmethod
    def compute(self, *, df: DATA_FRAME):
        pass


class CustomerCount(Strategy):
    report_var_name: str = "number_of_customers"

    def __init__(self):
        super().__init__()

    def compute(self, *, df: DATA_FRAME):
        return df["name"].nunique()


class AverageOrderValue(Strategy):
    report_var_name: str = "average_order_value (pre-tax)"

    def __init__(self):
        super().__init__()

    def compute(self, *, df: DATA_FRAME):
        avg_order_value = 0
        if not df[df["price"] > 0].empty:
            avg_order_value = df[df["price"] > 0]["price"].mean()
        return round(avg_order_value, 2) or 0


class ReturnPercentage(Strategy):
    report_var_name: str = "percentage_of_returns"

    def __init__(self):
        super().__init__()

    def compute(self, *, df: DATA_FRAME):
        returns = df[df["price"] < 0]
        returns_pct = (len(returns) / len(df)) * 100 if len(df) > 0 else 0
        return round(returns_pct, 2)


class TotalSales(Strategy):
    report_var_name: str = "total_sales_in_period (pre-tax)"

    def __init__(self):
        super().__init__()

    def compute(self, df):
        return round(df["price"].sum(), 2)
