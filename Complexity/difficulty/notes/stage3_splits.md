# Stage 3: splits (Heshmat, 29 Oct 2026)

Produced by `Complexity/difficulty/scripts/stage3_splits.py` from `labels/labels_v1.csv` and the SPROUT prompt text, seed 42 (pre-registered). Tables are in `notes/stage3/`. The split file is `Complexity/difficulty/splits/split_v1.csv` (see `splits/README.md`). **Frozen from this commit.**

## Result

| Split | Prompts | Removed as duplicates | External hard % of labelled | Local hard % of labelled |
|---|---|---|---|---|
| train | 30,621 | 347 | 8.7 | 19.4 |
| calibration | 3,302 | 16 | 8.4 | 20.5 |
| threshold | 3,293 | 25 | 8.4 | 18.4 |
| test | 6,637 | 0 (never altered) | 9.1 | 19.7 |

43,853 rows; 388 duplicates left out (listed in `notes/stage3/removed.csv`). Infeasible prompts stay in the file; each head skips its own infeasible rows.

Calibration / threshold: SPROUT validation split in half, stratified on source x `easy_ext` (43 strata; 4 prompts from cells under 2 went to the shared "other" stratum). All 20 sources appear in both halves. Per-source counts: `notes/stage3/split_by_source.csv`.

## Duplicates across parts

| Parts | Exact (full-text hash) | Near (MinHash >= 0.9, word 5-grams) |
|---|---|---|
| train / test | 54 | 161 |
| train / calibration | 38 | 70 |
| train / threshold | 28 | 51 |
| calibration / test | 5 | 13 |
| threshold / test | 12 | 13 |
| calibration / threshold | 8 | 9 |

- Same `(dataset, dataset_idx)` across parts: 0 pairs (as in Stage 1).
- 301 prompts have an exact duplicate inside their own part. That is not a leak, so they are kept.
- 17 calibration / threshold pairs are reported, not removed. The plan has no rule for them, and both halves are validation data.
- The removal rule follows the plan: test never changes, train loses to any other part, and calibration / threshold lose only to test.

### What the near-duplicates are (spot check of pairs from each large source)

| Source | Near pairs | What differs | Verdict |
|---|---|---|---|
| openhermes | 45 | A trailing `ENDINSTRUCTION`; same golden answer | real duplicate |
| MMLU-Pro | 6 | Same question, answer options reshuffled or trimmed | real duplicate |
| ragbench/cuad | 99 | Same contract (20k to 43k characters), different clause question | **same passage, different question** |
| MuSR/object_placements | 147 | Same story, asked about a different object or person | **same passage, different question** |

**Decision:** shared-passage pairs are removed like duplicates. A classifier that has seen the same 40k-character contract in train is not being tested on new text. This costs 171 train prompts (0.6% of train) plus 19 calibration / threshold prompts, all from two tiny sources that are already "too few to judge" per source. Test is untouched either way. Logged in `preregistration.md`.

The plan's hand check of 20 flagged pairs is in `notes/stage3/near_dup_pairs_to_read.md`. **Still to do:** write a verdict under each pair and record the count here.

## Effect on Stage 2 decisions

- External class weight from the final train part: 25,179 / 2,390 = **10.54** (Stage 2 said 10.56 before duplicate removal). Zeina should use 10.54. The square-root fallback stays 3.25.
- Local head: still no class weights (hard is 19.4% of labelled train).
- The split depends only on `easy_ext` and the prompt text. If the local pair changes later (`labels_v2.csv`), this split stays valid.

## Rules from now on

- Everyone uses `split_v1.csv`. Nobody makes their own split.
- **Nobody computes anything on `test` until Stage 6.** Then, in order: AUROC once the models are frozen, calibration once T is frozen, routing once tau is frozen.
- `calibration` is used only to fit T (Sameh). `threshold` is for baselines, picking the epoch and picking tau.
