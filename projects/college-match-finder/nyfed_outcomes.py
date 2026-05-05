import pandas as pd
from pathlib import Path
from functools import lru_cache

PARQUET_PATH = Path(__file__).parent / "data" / "processed" / "nyfed_outcomes.parquet"

_METRIC_COLS = [
    "unemployment_rate",
    "underemployment_rate",
    "median_wage_early_career",
    "median_wage_mid_career",
    "share_with_graduate_degree",
]


@lru_cache(maxsize=1)
def _load_outcomes_df() -> pd.DataFrame:
    return pd.read_parquet(PARQUET_PATH)


def get_nyfed_outcomes(cip4: str) -> dict | None:
    if not cip4:
        return None
    cip4 = str(cip4).strip()
    # Handle 4-digit format without dot: "1107" -> "11.07"
    if "." not in cip4 and len(cip4) == 4 and cip4.isdigit():
        cip4 = f"{cip4[:2]}.{cip4[2:]}"
    parts = cip4.split(".")
    if len(parts) != 2:
        return None
    cip4 = f"{parts[0]}.{parts[1][:2]}"

    df = _load_outcomes_df()
    row = df[df["cip4"] == cip4]
    if row.empty:
        return None
    r = row.iloc[0]
    return {col: r[col] for col in _METRIC_COLS}
