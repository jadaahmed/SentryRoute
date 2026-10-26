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

Reading: scores are mostly 0 or 1 but not all (e.g. 0.9 appears); almost nothing sits near 0.5 (at most 0.07%), so the 0.5 cutoff is natural and the rule-sensitivity check (0.4 / 0.6) should change very few labels. Keep the 0.5 cutoff. Histograms: `Complexity/difficulty/notes/stage1/score_histograms.png`.

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
| ragbench (12 sources, 1,827 prompts, 4.1% of data) | 82–167 | 16–39 | 15–39 | 131–241 |

Flags:
- 15 of 20 sources have fewer than 50 prompts in at least one split (all 3 MuSR and all 12 ragbench sources). Per-source AUROC in Stage 6 (needs 50 easy and 50 hard test prompts) will realistically be possible only for openhermes, MMLU-Pro, the two MATH sources and maybe GPQA. Say so in the report.
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

## Judge quality: hand-check results (Stage 1 steps 4 and 6)

Judged model: `openai-gpt-4o`. Reviewed 20 random rows (`sample_20_rows.md`) and a 30-row source-stratified red-flag sample (`redflag_30_rows.md`). **Verdict: the judge is not broken. Proceed to Stage 2.** Every clearly wrong answer got a low score and no clearly wrong answer got a high one.

| Check | Result | 95% interval |
|---|---|---|
| 20 random rows: wrong answers score low? | 17 scored 1.0, 3 scored 0.0. Both clear failures got 0.0. One likely false negative (`abd10cc72465`, 0.0, the question is underspecified and the golden answer assumes an unstated value), two minor borderline 1.0s | 1 of 20 wrong: 0.9% to 23.6% |
| 30-row red-flag: scores that look wrong | 3 wrong (rows 3, 10, 23), 1 borderline (row 24); 26 of 30 correct | 3 of 30: 3.5% to 25.6%; with borderline 4 of 30: 5.3% to 29.7% |

The two samples may overlap, so they are not pooled. Intervals are Wilson intervals: with this few rows they are wide.

**Most disagreements do not change a label.** The cutoff is 0.5. The flagged scores of 0.8 or 0.9 stay above it even when corrected (rows 3, 23, 24), so easy/hard would not change. Rows that could cross the cutoff: `abd10cc72465` (likely false negative, 0.0) and row 10 (golden answer wrong, judge gave 0.8, "should be lower"; by how much is unclear). Row 22 (techqa, 0.0) is defensible. So roughly 1 to 2 of the 50 rows reviewed could flip a label: about 2% to 4%, uncertain. The full 100-row check (Stage 1b) will give the figure the report cites.

**Flagged rows**

| Row | Source | Judge | Issue |
|---|---|---|---|
| 3 | openhermes/teknium | 0.8 | Open-ended creative task. Judge penalized using a sea turtle instead of the golden's octopus; response met all requirements |
| 10 | ragbench/delucionqa | 0.8 | Golden answer is wrong (mixed two manual sections). Judge docked the model for omitting wrong causes |
| 23 | ragbench/msmarco | 0.8 | Golden is about the Broad Run stream in Loudoun County; the model correctly said Broad Run, VA is in Fauquier County |
| 24 | ragbench/hagrid | 0.9 | Garbled sentence in the response (temperature missing); 0.7 to 0.8 is fairer |
| 7 | GPQA | 0.0 | Score right, but the justification says the model was "mostly correct"; it missed a carbocation rearrangement |
| 22 | ragbench/techqa | 0.0 | Score defensible, but the golden answer comes from an unrelated document |

Also noted in the 20-row sample: `97592a440ebb` (borderline 1.0, defensible answer that differs from the golden), `ea71eb800c47` (SGLT2 called an enzyme, still 1.0), and a self-contradicting justification on the reticular-formation row (score right).

**What this means**
- **Bad golden answers in ragbench.** Three of the 30 red-flag rows (10, 22, 23) had broken golden answers, all ragbench. The judge treats the golden as truth. Ragbench is 4.1% of the data (1,827 prompts) and most of its sources are too small for per-source results anyway, but labels there are noisier. State this in the limits. Auditing delucionqa, techqa and msmarco goldens is optional follow-up.
- **Open-ended tasks** are judged against a single reference answer (row 3, and the magic-show row). The stored SPROUT scores cannot be changed, so a judge rule such as "for open-ended tasks, grade against the task requirements" belongs to **Phase 2**, when we label with our own judge on the real pool.
- **Truncated responses.** Rows 1, 7, 12 and 17 (red-flag) and five rows in the sample were cut off before the final answer. The reviewer checked the answers independently where possible (rows 1, 2, 12, 17, 21 verified by hand) but relied on the judge's summary for some. Treat the check as slightly generous to the judge.
- **Single model.** Only `openai-gpt-4o` was checked. Labels use four models, so the 100-row check in Stage 1b should include scores from the other three.

