# split_v1.csv

Frozen output of `Complexity/difficulty/scripts/stage3_splits.py` (29 Oct 2026, seed 42). Never edit or overwrite; a new version gets a new name (`split_v2.csv`).

- Rows: 43,853. SHA-256: `c55ea3ff9b328c73b0f01b6a4d6e0cfb46cc9eb58e0465c63b18d280bf46a405`
- Columns: `prompt_id` (SPROUT `key`, joins to `labels/labels_v1.csv`), `split` (`train` / `calibration` / `threshold` / `test`)
- 388 prompts from `labels_v1.csv` are **not in this file**: duplicates removed in Stage 3 (`notes/stage3/removed.csv`). Use an inner join, never a left join that keeps them.
  `L.merge(pd.read_csv("split_v1.csv"), on="prompt_id", how="inner")`
- `test` is SPROUT test unchanged (6,637). Locked until Stage 6.
- Counts and decisions: `Complexity/difficulty/notes/stage3_splits.md`
