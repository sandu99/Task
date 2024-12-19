import pandas as pd
import numpy as np
from typing import List, Optional, Dict
from datetime import datetime
from app.schemas import Filters, ColumnSummary


def filter_data(data: pd.DataFrame, filters: Optional[Filters]) -> pd.DataFrame:

    if not filters:
        return data

    if filters.date_range:
        data["date"] = pd.to_datetime(data["date"])
        start_date = datetime.strptime(filters.date_range.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(filters.date_range.end_date, "%Y-%m-%d")
        data = data[(data["date"] >= start_date) & (data["date"] <= end_date)]

    if filters.category:
        data = data[data["category"].isin(filters.category)]

    if filters.product_ids:
        data = data[data["product_id"].isin(filters.product_ids)]

    return data

def calculate_summary_statistics(data: pd.DataFrame, columns: List[str]) -> Dict[str, ColumnSummary]:
    summary = {}
    for column in columns:
        if column not in data.columns:
            continue
        summary[column] = ColumnSummary(
            mean            =round(data[column].mean(), 1),
            median          =round(data[column].median(), 1),
            mode            =data[column].mode().iloc[0],
            std_dev         =round(data[column].std(), 1),
            percentile_25   =round(np.percentile(data[column], 25), 1),
            percentile_75   =round(np.percentile(data[column], 75), 1),
        )
    return summary
