# Datasets

Document every dataset's source and license here. Do not commit raw data containing real personal information.
Add a row per dataset (sensitivity datasets go in their own rows, owned by the sensitivity team).

| Dataset | Axis | Source | License | Used for | Stored in repo? | Owner |
|---|---|---|---|---|---|---|
| SPROUT (44,241 prompts, 13 models' answers + judge scores) | Difficulty | Hugging Face `CARROT-LLM-Routing/SPROUT` (released with the CARROT paper) | **Resolved 26 Oct 2026** (reported by Heshmat): we may use SPROUT for research and report results on it. The Hugging Face page itself shows no license and an empty README, so link the written confirmation here (name of the license or the reply received) | Train and evaluate the complexity classifier (Phase 1) | Raw data: **no**, fetched by script (`datasets.load_dataset`, about 800 MB). Derived files **yes**: `Complexity/difficulty/labels/labels_v1.csv` (labels + scores), `Complexity/difficulty/notes/` tables and reading samples | Adam Heshmat |
