"""
Utilities for working with dataframes - dataframe inspection / cleaning helpers
"""

import pandas as pd


def search_df_columns(df: pd.DataFrame, name: str | list[str]) -> list[str]:
    if isinstance(name, str):
        name = [name]

    cleaned_name = [search_term.lower().strip() for search_term in name]

    return [
        col
        for col in df.columns
        if any(search_term in col.lower().strip() for search_term in cleaned_name)
    ]
