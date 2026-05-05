import yaml
import pandas as pd
from pathlib import Path
from functools import lru_cache

DESCRIPTIONS_PATH = Path(__file__).parent / "data" / "major_descriptions.yaml"
_FOS_CSV_PATH = Path(__file__).parent / "data" / "cleaned" / "field_of_study_cleaned.csv"


@lru_cache(maxsize=1)
def load_major_descriptions() -> dict:
    """Load all hand-authored major descriptions keyed by CIP4 string."""
    if not DESCRIPTIONS_PATH.exists():
        return {}
    with open(DESCRIPTIONS_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@lru_cache(maxsize=1)
def _build_cipdesc_lookup() -> dict:
    """Build {cip4_str: canonical_name} from the cleaned FoS CSV.

    All rows are bachelor's-level (credential_level == 3). Canonical name
    is the most common cip_description per CIP4, trailing periods stripped.
    """
    if not _FOS_CSV_PATH.exists():
        return {}
    df = pd.read_csv(
        _FOS_CSV_PATH,
        usecols=["cip_code", "cip_description"],
        low_memory=False,
    )
    df["cip4"] = df["cip_code"].apply(lambda c: f"{int(c):04d}").apply(
        lambda s: f"{s[:2]}.{s[2:]}"
    )
    df["cip_description"] = df["cip_description"].str.rstrip(".").str.strip()
    name_map = df.groupby("cip4")["cip_description"].agg(lambda x: x.mode().iloc[0])
    return name_map.to_dict()


def get_description(cip_code: str) -> dict | None:
    """Return description dict for a CIP4 code, or None if unknown.

    Accepts CIP4 ('11.07') or CIP6 ('11.0701') and normalizes to CIP4.

    Returns a full hand-authored dict if CIP4 is in the YAML,
    a stub dict with is_stub=True if CIP4 is in the FoS dataset but not YAML,
    or None if CIP4 is unknown in both sources.
    """
    if not cip_code:
        return None
    parts = str(cip_code).split(".")
    if len(parts) != 2:
        return None
    cip4 = f"{parts[0]}.{parts[1][:2]}"

    entry = load_major_descriptions().get(cip4)
    if entry is not None:
        return entry

    name = _build_cipdesc_lookup().get(cip4)
    if name is not None:
        return {"name": name, "is_stub": True, "cip4": cip4}

    return None
