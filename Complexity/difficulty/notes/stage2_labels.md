# Stage 2: labels (Heshmat, 26 Oct 2026)

Produced by `difficulty/scripts/stage2_labels.py` on the full SPROUT download. Rule and pairs are the pre-registered ones: adequacy cutoff 0.5; external pair GPT-4o-mini to GPT-4o; local pair Llama 3.1 8B to Llama 3.3 70B (stand-in; the laptop-VRAM check is still open, see below). Tables are in `notes/stage2/`. The labels file is committed as `difficulty/labels/labels_v1.csv` (44,241 rows, 5 MB; see `difficulty/labels/README.md`).

## Result

| Pool | Easy | Hard | Infeasible |
|---|---|---|---|
| External | 36,382 (82.2%) | 3,454 (7.8%) | 4,405 (10.0%) |
| Local | 31,820 (71.9%) | 7,666 (17.3%) | 4,755 (10.7%) |

Checks: 44,241 rows, `prompt_id` unique, no missing scores, all four score columns in [0, 1]. Totals match the Stage 1 preview exactly. SPROUT's train / validation / test splits have nearly the same label mix (external hard 7.8% / 7.5% / 8.2%; local hard 17.3% / 17.4% / 17.6%), so a threshold chosen on one transfers.

## The cutoff hardly matters

Only 0.07% (external) and 0.11% (local) of prompts have a cheap or strong score within 0.1 of 0.5.

| Cutoff | External labels changed | Local labels changed |
|---|---|---|
| 0.4 | 120 (0.27%) | 368 (0.83%) |
| 0.6 | 22 (0.05%) | 45 (0.10%) |

No limitation to report beyond a one-line mention.

## Decisions (made from the numbers above, before any training)

| Decision | Value | Reason |
|---|---|---|
| External head | **Class weights on the hard class**, computed from the **training split only**: easy/hard = 25,465 / 2,411 = **10.56** | Hard is 8.6% of labelled training prompts (under the plan's 15% line) |
| Local head | No class weights | Hard is 19.4% of labelled prompts (over 15%) |
| Fallback if weight 10.56 destabilises training | Zeina may use the square root, 3.25, and must say so in the training log | Large weights can hurt calibration; Stage 7's temperature T corrects part of that. AUROC does not depend on the weight |
| Infeasible prompts | Stay in the file, excluded from training for that pool's head | Plan rule |
| Local pair | Keep Llama 8B to 70B for now | Infeasible is 10.7% (far below 40%), hard 17.3%. The laptop-VRAM check is open; if the team later says only small models fit, rerun this script with `--local-cheap wxai-llama-3-2-3b-instruct --local-strong wxai-llama-3-1-8b-instruct --labels-out labels_v2.csv` **before any training** |
| Cutoff | 0.5 unchanged | Pre-registered, and shown insensitive |

## What the numbers say about the design

**The two pools disagree often.** For the 37,344 prompts labelled in both pools, 6,508 (17.4%) get different labels. The big group is **easy for the external pool but hard for the local one: 5,194 prompts (11.7% of all, 14.3% of the externally easy prompts)**. A single top-level tier ("the more complex of the two") would send those to the strong model although the cheap external model is enough. This is the case for the optional per-pool field in the complexity response (open question in `CLAUDE.md`). The opposite case (hard externally, easy locally) is 1,314 prompts (3.0%). These are label counts, not classifier predictions, so they show the size of the effect, not a measured saving.

Another 4,634 prompts (10.5%) are infeasible in only one pool; 2,263 are infeasible in both.

**Difficulty depends heavily on the source.** External easy rate: openhermes 92.7%, MMLU-Pro 67.6%, MATH about 81%, GPQA 42.1%, ragbench 82% to 99%. A classifier can partly learn "which benchmark is this", and the source-prior baseline will be strong. Keep it in its own labelled row (plan Stage 4). Ragbench sources are nearly all easy (hard counts 1 to 12 per source), so nothing can be learned or evaluated per ragbench source.

**Per-source AUROC (Stage 6) is possible for few sources.** Rule: at least 50 easy and 50 hard test prompts.
- External pool: MMLU-Pro (1,186 easy / 320 hard), MATH/all (914 / 61), openhermes (2,693 / 91). Three sources.
- Local pool: MMLU-Pro, MATH/all, MATH/all/test (209 / 78), openhermes. Four sources.
All other sources are reported as "too few to judge".

**Training sizes.** External head: 27,876 labelled training prompts (2,411 hard). Local head: 27,605 (5,343 hard).

## Still open

- Laptop GPU / VRAM answer (decides the local pair; see above).
- Stage 3 (frozen splits) is next. Nobody trains until it is frozen.
