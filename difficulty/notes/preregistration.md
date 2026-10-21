# Pre-registration (Phase 1 difficulty classifier)

Copied verbatim from `difficulty/docs/phase1_plan_v2.4.md` on 21 Oct 2026, before any labels, splits, baselines or classifier results existed.
Changing a choice later is allowed only with a written reason and date, added to the change log at the bottom.

Honesty note: Stage 1 (descriptive statistics of SPROUT, including a rough easy/hard/infeasible preview at cutoff 0.5) had already been run when this file was written. No model was trained and no baseline was scored.

## Choices

| Choice | Value |
|---|---|
| External pair (cheap → strong) | `openai-gpt-4o-mini` → `openai-gpt-4o` (GPT-4o is OpenAI's large cloud model; GPT-4o-mini is its smaller, cheaper version) |
| Local pair (cheap → strong) | `wxai-llama-3-1-8b-instruct` → `wxai-llama-3-3-70b-instruct` (Llama is Meta's open-source model family that you can host yourselves; 8B and 70B mean 8 and 70 billion parameters, i.e. model size) |
| **[v2.1]** Backup local pair | `wxai-llama-3-2-3b-instruct` → `wxai-llama-3-3-70b-instruct`, used only if the Stage 2 balance check fails, decided before any training |
| Adequacy cutoff | 0.5: the judge score at or above which an answer counts as good enough (revisit only in Stage 1, after seeing the score distribution, with a written reason) |
| Under-routing target | at most 10% of hard prompts sent to the cheap model (a hard prompt is one only the strong model answers adequately) |
| **[v2.1]** Uncertainty margin | 0.1, above tau only (prompts scoring between tau and tau + 0.1 become tier `moderate`, the unsure band) |
| **[v2.1]** Max length and truncation | 2,048 tokens (a token is a word piece, about three-quarters of a word): keep the first 1,536 + last 512 |
| Gate 1 (a go/no-go checkpoint) | TF-IDF (a simple method that turns text into word-frequency numbers) with logistic regression (a simple classifier that outputs a probability) reaches AUROC >= 0.6 on the threshold split (the validation half used to pick tau; see Stage 3). AUROC = area under the ROC curve: the chance that a random easy prompt scores higher than a random hard prompt; 0.5 is random guessing, 1.0 is perfect |
| Gate 2 | Classifier AUROC > TF-IDF AUROC, both pools, threshold split |
| Gate 3 | Test under-routing about 12% or lower, judged with its CI |
| Seed | 42 (a fixed starting number for random choices, so anyone can recreate the same split) |
| **[v2.3]** Tier rule (per pool, p = P(cheap model adequate)) | `simple`: p >= tau + 0.1 · `moderate`: tau <= p < tau + 0.1 · `complex`: p < tau. Contract `score` = 1 − p (higher = more complex) |
| **[v2.3]** Tier and score the gateway sees | The more complex of the two pools' results (safe: never routes cheaper than either pool allows), pending the contract author's answer to open question 1 |
| **[v2.3]** Serving input rule | Flatten `messages` to one text: all turns in order, separated by blank lines, last user turn last. If over 2,048 tokens, keep the first 1,536 and last 512. A single-turn SPROUT prompt is already in this form |
| **[v2.3]** Latency budget | 250 ms deadline per check; target routing overhead under 100 ms at p95 on CPU for prompts under 2,000 tokens (the contract's proposed target) |


## Checks against real data (Stage 1, 21 Oct 2026)

| Item | Result |
|---|---|
| All four pre-registered models and the backup model exist in SPROUT | yes |
| Score range | all in [0, 1], none missing |
| Scores within 0.4 to 0.6 (cutoff-sensitivity) | at most 0.07% per model; keep the 0.5 cutoff |
| Local pair vs laptop VRAM (Stage 0 step 6) | **still open**: depends on the team's answer. Decide before any label is computed |

## Change log

| Date | Change | Reason | By |
|---|---|---|---|
| | | | |
