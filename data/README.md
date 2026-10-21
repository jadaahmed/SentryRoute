# Datasets

Document every dataset's source and license here. Do not commit raw data containing real personal information.
Add a row per dataset (sensitivity datasets go in their own rows, owned by the sensitivity team).

| Dataset | Axis | Source | License | Used for | Stored in repo? | Owner |
|---|---|---|---|---|---|---|
| SPROUT (44,241 prompts, 13 models' answers + judge scores) | Difficulty | Hugging Face `CARROT-LLM-Routing/SPROUT` (released with the CARROT paper) | **Unknown: the HF page shows no license and an empty README.** Question sent to supervisor: not yet recorded | Train and evaluate the complexity classifier (Phase 1) | No raw copy. Derived summary tables in `difficulty/notes/stage1/` | Adam Heshmat |
