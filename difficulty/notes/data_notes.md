# SPROUT data notes (Stage 1) — Heshmat, 21 Oct 2026

Source: output of `stage1_explore.py` run on the real dataset (`CARROT-LLM-Routing/SPROUT`). Items marked **TODO** need hand reading.

## Splits (differ slightly from the plan)
| split | rows | plan said |
|---|---|---|
| train | 30,968 | 31,000 |
| validation | 6,636 | 6,640 |
| test | 6,637 | 6,640 |
| total | 44,241 | 44,000 |

Calibration/threshold halves will be about 3,318 each. `key` is unique in every split and always 64 characters: use it as `prompt_id`.

## Columns (confirmed, none missing)
`key, dataset, dataset_level, dataset_idx, prompt, golden_answer` + 13 model columns:
aws-claude-3-5-sonnet-v1, aws-titan-text-premier-v1, openai-gpt-4o, openai-gpt-4o-mini, wxai-granite-3-2b-instruct-8k-max-tokens, wxai-granite-3-8b-instruct-8k-max-tokens, wxai-llama-3-1-70b-instruct, wxai-llama-3-1-8b-instruct, wxai-llama-3-2-1b-instruct, wxai-llama-3-2-3b-instruct, wxai-llama-3-3-70b-instruct, wxai-llama-3-405b-instruct, wxai-mixtral-8x7b-instruct-v01.
All four pre-registered models and the backup (llama-3-2-3b) exist. No pre-registration change needed for names.

## Model cell structure (every team member must use these names)
Each model cell is a dict:
- `response` (str): the model's answer
- `judge_response` (str): the judge's output, JSON text with `correctness_score` and `justification`
- `score` (float, 0–1): **the judge score used for labels**
- `num_input_tokens`, `num_output_tokens` (int): token counts (useful for a cost proxy later)

Missing scores for the four pipeline models: 0. Scores outside [0, 1]: 0. (Missing values in the other 9 models were not checked; not needed.)

## Score distributions (all splits pooled, n = 44,241 each)
| model | mean | % exactly 0 or 1 | % strictly between 0.4 and 0.6 | % >= 0.5 |
|---|---|---|---|---|
| gpt-4o | 0.845 | 86.8 | 0.04 | 86.1 |
| gpt-4o-mini | 0.808 | 87.5 | 0.04 | 82.2 |
| llama-3.1-8b | 0.690 | 74.5 | 0.07 | 71.9 |
| llama-3.3-70b | 0.806 | 69.7 | 0.04 | 84.2 |

Reading: scores are mostly 0 or 1 but not all (e.g. 0.9 appears); almost nothing sits near 0.5 (at most 0.07%), so the 0.5 cutoff is natural and the rule-sensitivity check (0.4 / 0.6) should change very few labels. Keep the 0.5 cutoff. Histograms: `difficulty/notes/stage1/score_histograms.png`.

## Label preview at cutoff 0.5 (NOT final; Stage 2 produces the real labels)
| pool | easy | hard | infeasible |
|---|---|---|---|
| external (4o-mini → 4o) | 82.2% | **7.8%** | 10.0% |
| local (8B → 70B) | 71.9% | 17.3% | 10.7% |

Implications for Stage 2:
- External hard is under the plan's 15% line, so that head needs class weights (or the tolerance idea). Decide and record in Stage 2.
- Local pool is not badly unbalanced and infeasible is about 11%, far below 40%, so keep the pre-registered Llama 8B → 70B pair (still subject to the laptop-VRAM check in Stage 0 step 6).
- Infeasible is about 10% in both pools, so the "include infeasible in outcome metrics" rule in Stage 8 matters.

## Sources (20, as expected) and `dataset_level` (7 values, as expected)
- `dataset_level` is `Level 1`–`Level 5` plus `Level ?` (2 rows) for the two MATH sources only; it is an **empty string for all other sources**. It carries no information outside MATH.
- MATH appears as two sources: `lighteval/MATH/all` (7,412) and `lighteval/MATH/all/test` (2,472). MuSR appears as three: `TAUR-Lab/MuSR` (248), `.../object_placements` (250), `.../team_allocation` (250).

| source | train | val | test | total |
|---|---|---|---|---|
| openhermes/teknium | 13,670 | 2,873 | 2,912 | 19,455 |
| TIGER-Lab/MMLU-Pro | 8,264 | 1,750 | 1,772 | 11,786 |
| lighteval/MATH/all | 5,122 | 1,184 | 1,106 | 7,412 |
| lighteval/MATH/all/test | 1,735 | 381 | 356 | 2,472 |
| Idavidrein/gpqa/gpqa_extended | 384 | 63 | 94 | 541 |
| TAUR-Lab/MuSR (3 variants) | 163 / 185 / 176 | 39 / 27 / 35 | 46 / 38 / 39 | 248 / 250 / 250 |
| ragbench (11 sources) | 82–167 | 16–39 | 15–39 | 131–241 |

Flags:
- 15 of 20 sources have fewer than 50 prompts in at least one split (all MuSR and all 11 ragbench sources). Per-source AUROC in Stage 6 (needs 50 easy and 50 hard test prompts) will realistically be possible only for openhermes, MMLU-Pro, the two MATH sources and maybe GPQA. Say so in the report.
- Three sources (openhermes, MMLU-Pro, MATH) are about 93% of the data, so overall AUROC will be dominated by them, and the source-prior baseline is likely to be strong. Keep it in its own labelled row.
- Stage 3 stratification: many source × label cells will be under 2 prompts in the validation halves, so the shared "other" stratum rule is needed.

## `(dataset, dataset_idx)` overlap across splits
0 pairs appear in more than one split (0 of 44,241). Caveat: MATH is split into two source names (`/all` and `/all/test`), so the same problem could appear in both under different names. This check cannot see that. **Stage 3 must rely on the full-text hash and MinHash checks**, including across these two MATH sources.

## Prompt length (ModernBERT tokenizer)
Median 62 tokens, 95th percentile 591, max 18,571 (87,330 characters). Over 2,048: **334** prompts (0.76%). Over 4,096: **225**.

Truncation (2,048, keep first 1,536 + last 512) will hit mostly three sources:
| source | n | over 2,048 | over 4,096 |
|---|---|---|---|
| ragbench/cuad | 215 | 171 (80%) | 121 |
| ragbench/techqa | 132 | 126 (95%) | 87 |
| ragbench/expertqa | 131 | 29 | 16 |
| ragbench/delucionqa | 184 | 4 | 0 |
| ragbench/hagrid | 132 | 2 | 0 |
| gpqa_extended | 541 | 2 | 1 |

Only ragbench sources and 2 GPQA items exceed the limit. For cuad and techqa most prompts are truncated, so expect weaker results there; these are also tiny sources. Record in the limits.

## To fill in by hand
- [ ] 20 random rows read (`notes/sample_20_rows.md`): does a wrong answer get a low score? ______
- [ ] Judge red-flag check, 30 rows (`notes/redflag_30_rows.md`): ___ / 30 judge scores looked wrong
- [ ] Anything odd in a source (broken prompts, empty answers)? ______
