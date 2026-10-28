# Difficulty (complexity) classifier: Phase 1

This folder is the **complexity service's** research and training work: a classifier that predicts how hard a prompt is, so the router can pick the cheapest adequate model. It is trained and evaluated on **SPROUT**, a public dataset with stored answers and judge scores from 13 models. No model is run or paid for in Phase 1.

**Boundary.** This folder is complexity only. The sensitivity detector lives elsewhere in the repo and is a separate service. Nothing here reads, writes or depends on sensitivity code or data. Keep it that way: do not import across, and never put sensitivity test sets anywhere near this folder's training code.

Source of truth for the full method: [`docs/phase1_plan_v2.4.md`](docs/phase1_plan_v2.4.md). Pre-registered choices (model pairs, cutoffs, gates): [`notes/preregistration.md`](notes/preregistration.md). If the plan and `api/openapi.yaml` disagree, the contract wins and the plan changes.

## Who does what

| Person | Role | Stages |
|---|---|---|
| Adam Heshmat | Data and labels | 1, 1b, 2, 3 |
| Hana Salah | Baselines and evaluation code | 4, 6 |
| Zeina Reda | Training, serving wrapper, latency | 5, 5b |
| Mohamed Sameh | Contract and mock, calibration, tau, report | 0, 7, 8, 9 |

## Status

| Stage | Owner | Status |
|---|---|---|
| 0 Setup, contract questions, mock service | Sameh | not started in this repo |
| 1 Understand SPROUT | Heshmat | **done.** Analysis and judge hand-check in [`notes/data_notes.md`](notes/data_notes.md): judge not broken, proceed to Stage 2 |
| 1b 100-row judge hand-check | Heshmat | later (days 5-7) |
| 2 Labels | Heshmat | **done.** [`notes/stage2_labels.md`](notes/stage2_labels.md), `labels/labels_v1.csv` (open: laptop VRAM check for the local pair; does not affect the split) |
| 3 Splits (frozen) | Heshmat | **done, frozen 29 Oct 2026.** [`notes/stage3_splits.md`](notes/stage3_splits.md), `splits/split_v1.csv` |
| 4-9 | others | **unblocked**: use `labels_v1.csv` + `split_v1.csv`; test locked until Stage 6 |

## Stage 1 findings that affect everyone

- 44,241 prompts: train 30,968 / validation 6,636 / test 6,637. Use `key` as `prompt_id`.
- Model cell fields: `response`, `judge_response`, `score` (0-1, the label source), `num_input_tokens`, `num_output_tokens`.
- External pool has only about 7.8% hard prompts, so that head needs class weights (decide in Stage 2). Local is about 17.3% hard.
- Three sources (openhermes, MMLU-Pro, MATH) are about 93% of data. 15 of 20 sources are too small for per-source AUROC.
- MATH appears under two source names; duplicate checks in Stage 3 must use full-text hash and MinHash, not just `(dataset, dataset_idx)`.
- 334 prompts exceed 2,048 tokens, nearly all ragbench (80% of `cuad`, 95% of `techqa`).

## Reproduce Stage 1

Use a fresh virtual environment (the `dev` conda env had a NumPy 1.x clash with current `pyarrow`).

```bash
python3 -m venv .venv-sprout && source .venv-sprout/bin/activate
pip install -r Complexity/difficulty/requirements-stage1.txt
python Complexity/difficulty/scripts/stage1_explore.py --out Complexity/difficulty/notes/stage1 \
  --response-field response --judge-field judge_response --score-field score
```

Needs internet for Hugging Face (`CARROT-LLM-Routing/SPROUT` and the `answerdotai/ModernBERT-base` tokenizer). `--samples-only` regenerates just the reading files. `--local DIR` reads `train/validation/test.jsonl` from a folder (for testing).

## Shared file formats (agreed so work can be done in parallel)

- **Labels** `labels/labels_v1.csv`: `prompt_id, dataset, dataset_level, easy_ext, easy_loc, score_gpt4o_mini, score_gpt4o, score_llama8b, score_llama70b` (`easy_*` is 1, 0 or `infeasible`)
- **Split** `splits/split_v1.csv`: `prompt_id, split` with split in `train / calibration / threshold / test`
- **Scores** `scores/*.csv`: `prompt_id, split, model_name, head, raw_logit` (raw logits, so T can be fitted without retraining)
- **Gateway shapes** follow `api/openapi.yaml` exactly. Internal names `p_cheap_ext` and `p_small_loc` appear only in our own files, never in a gateway response.

Never rename or overwrite a shared file in place: a new version gets a new name (`labels_v2.csv`).

## Rules for this folder

- **The test split is locked until the models are frozen (day 8).** Unlock order: test AUROC after models are frozen, test calibration after T is frozen, test routing numbers after tau is frozen. Only Sameh tunes T and tau.
- **No secrets in the repo.** Tokens and keys go in `.env` (gitignored).
- **Dependencies:** this is the eval/training environment, not the gateway image. Anything new needs team approval first. RouteLLM (needs LiteLLM) may only ever live in a separate eval environment, never the gateway.
- **No prompt text at rest** applies to the serving wrapper (Stage 5b): log only `request_id`, token count and latency. SPROUT files are public benchmark text, so they may be stored here; never commit real or customer data.
- **Trained weights** are not committed. See `models/README.md`.
- Dataset source and license notes live in [`/data/README.md`](../data/README.md). SPROUT's license question is resolved (26 Oct 2026); the shared derived files, including `labels/labels_v1.csv`, are committed.

## Relationship to the root `CLAUDE.md`

`CLAUDE.md` was updated on 22 Oct 2026 to describe this Phase 1 design (two heads, tier rule, SPROUT labels, latency split). If this folder and `CLAUDE.md` disagree, fix both in the same PR. The per-pool `pools` field was agreed on 26 Oct 2026 (contract v2); the only pending contract item is the tier to model mapping, in its Open questions table.
