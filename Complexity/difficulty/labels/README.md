# labels_v1.csv

Frozen output of `Complexity/difficulty/scripts/stage2_labels.py` (26 Oct 2026). Never edit or overwrite; a new version gets a new name (`labels_v2.csv`).

- Rows: 44,241 (one per SPROUT prompt). SHA-256: `138bb50c7ec6829ede04ef9b98d9576b74b22d988145ecadee047a4d202676df`
- Columns: `prompt_id` (SPROUT `key`), `dataset`, `dataset_level` (empty outside MATH), `easy_ext`, `easy_loc`, `score_gpt4o_mini`, `score_gpt4o`, `score_llama8b`, `score_llama70b`, `sprout_split` (original SPROUT split; Stage 3 needs it)
- Label values: `1` = easy (cheap model adequate), `0` = hard (only the strong model adequate), `infeasible` (neither). Cutoff 0.5.
- **Read the label columns as text** (`dtype=str`, and `keep_default_na=False` so the empty `dataset_level` is not turned into NaN):
  `pd.read_csv("labels_v1.csv", dtype={"easy_ext": str, "easy_loc": str}, keep_default_na=False)`
- `score_llama8b` / `score_llama70b` hold the local pair's cheap / strong scores (Llama 3.1 8B, Llama 3.3 70B).
- Counts and decisions: `Complexity/difficulty/notes/stage2_labels.md`
