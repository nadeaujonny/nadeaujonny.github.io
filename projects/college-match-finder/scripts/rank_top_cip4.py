"""
Rank top 60 CIP4 majors by IPEDSCOUNT1 (degrees conferred, bachelor's-level).

NaN values in IPEDSCOUNT1 are treated as 0 (suppressed small-cell data;
omitting them would under-count programs with many suppressed rows).
"""

import os
import pandas as pd

RAW = "data/raw/Most-Recent-Cohorts-Field-of-Study.csv"
V1_CSV = "data/processed/top_60_cip4.csv"
OUT = "data/processed/top_60_cip4_v2.csv"
ALREADY_AUTHORED = {"11.07", "14.19", "42.01"}


def to_cip4(cipcode) -> str:
    """4-digit integer CIPCODE -> 'XX.XX' string (e.g. 5202 -> '52.02')"""
    s = str(int(cipcode)).zfill(4)
    return f"{s[:2]}.{s[2:]}"


def main():
    # Load only needed columns; full file is ~229k rows
    cols = ["CIPCODE", "CIPDESC", "CREDLEV", "IPEDSCOUNT1"]
    df = pd.read_csv(RAW, usecols=cols)

    # Filter bachelor's only
    bach = df[df["CREDLEV"] == 3].copy()
    print(f"Bachelor's rows: {len(bach):,}")

    # NaN IPEDSCOUNT1 -> 0 (small-cell suppression; documented in header above)
    suppressed = bach["IPEDSCOUNT1"].isna().sum()
    print(f"Suppressed (NaN) IPEDSCOUNT1 rows set to 0: {suppressed:,}")
    bach["IPEDSCOUNT1"] = bach["IPEDSCOUNT1"].fillna(0)

    # Derive CIP4
    bach["cip4"] = bach["CIPCODE"].apply(to_cip4)

    # Canonical major name: mode of CIPDESC per CIP4 (strip trailing period)
    bach["CIPDESC"] = bach["CIPDESC"].str.rstrip(".")
    name_map = bach.groupby("cip4")["CIPDESC"].agg(lambda x: x.mode().iloc[0])

    # Aggregate completions
    totals = (
        bach.groupby("cip4")["IPEDSCOUNT1"]
        .sum()
        .rename("total_completions")
        .astype(int)
    )
    ranked = totals.to_frame().join(name_map).sort_values("total_completions", ascending=False)
    ranked["rank"] = range(1, len(ranked) + 1)

    # -- Coverage curve --------------------------------------------------------
    grand_total = ranked["total_completions"].sum()
    print(f"\nTotal bachelor's completions across all CIP4s: {grand_total:,}")
    cumsum = ranked["total_completions"].cumsum()
    for n in [30, 60, 100, 200]:
        pct = cumsum.iloc[n - 1] / grand_total * 100
        print(f"  Top {n:>3} CIP4s cover {pct:.1f}% of completions")
    for target in [0.90, 0.95, 0.99]:
        needed = (cumsum / grand_total < target).sum() + 1
        print(f"  CIP4s needed for {int(target*100)}% coverage: {needed}")

    # -- Top 15 console display ------------------------------------------------
    print(f"\nTop 15 CIP4 majors by completions:")
    print(f"{'rank':>4} | {'cip4':<7} | {'completions':>11} | major_name")
    print("-" * 70)
    for _, row in ranked.head(15).iterrows():
        print(f"  #{int(row['rank']):>2} | {row.name:<7} | {int(row['total_completions']):>11,} | {row['CIPDESC']}")

    # -- Delta vs V1 ----------------------------------------------------------─
    v1 = pd.read_csv(V1_CSV, usecols=["cip4", "rank"], dtype={"cip4": str})
    v1_rank = dict(zip(v1["cip4"], v1["rank"]))
    v1_set = set(v1["cip4"])

    top60_v2 = ranked.head(60)
    v2_set = set(top60_v2.index)

    print(f"\n-- Delta from V1 (institution-count ranking) --")
    # Biggest rank improvements
    deltas = []
    for cip4, row in top60_v2.iterrows():
        v2r = int(row["rank"])
        if cip4 in v1_rank:
            v1r = v1_rank[cip4]
            deltas.append((cip4, row["CIPDESC"], v1r, v2r, v1r - v2r))
    deltas.sort(key=lambda x: x[4], reverse=True)
    print("Top 5 biggest rank improvements (V1 -> V2):")
    for cip4, name, v1r, v2r, delta in deltas[:5]:
        print(f"  {cip4}  {name[:45]:<45}  #{v1r} -> #{v2r}  (+{delta})")

    dropped = v1_set - v2_set
    if dropped:
        print(f"\nIn V1 top 60 but NOT in V2 top 60 ({len(dropped)}):")
        for cip4 in sorted(dropped):
            name = v1[v1["cip4"] == cip4]["cip4"].values  # just print cip4
            print(f"  {cip4}  (V1 rank #{v1_rank[cip4]})")
    else:
        print("\nNo CIP4s dropped out of top 60 (same set).")

    new_entries = v2_set - v1_set
    if new_entries:
        print(f"\nIn V2 top 60 but NOT in V1 top 60 ({len(new_entries)}):")
        for cip4 in sorted(new_entries):
            r = int(top60_v2.loc[cip4, "rank"])
            nm = top60_v2.loc[cip4, "CIPDESC"]
            print(f"  {cip4}  {nm[:45]:<45}  V2 rank #{r}")
    else:
        print("No new CIP4s entered top 60 vs V1.")

    # -- Write output ----------------------------------------------------------
    out_df = top60_v2.copy()
    out_df.index.name = "cip4"
    out_df = out_df.reset_index()
    out_df["already_authored"] = out_df["cip4"].isin(ALREADY_AUTHORED)
    out_df = out_df.rename(columns={"CIPDESC": "major_name"})
    out_df = out_df[["cip4", "major_name", "total_completions", "rank", "already_authored"]]

    os.makedirs("data/processed", exist_ok=True)
    out_df.to_csv(OUT, index=False)
    print(f"\nOutput written to: {OUT}")


if __name__ == "__main__":
    main()
