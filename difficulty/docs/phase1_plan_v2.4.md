# SentryRoute Phase 1 (v2.4): Difficulty Classifier on SPROUT

Scope: train and evaluate the difficulty heads only. A "head" is the small final layer of the classifier that outputs one prediction; there is one head per pool. A "pool" is the group of models a prompt can be sent to: the external pool is cloud models (such as GPT), the local pool is models you host yourselves. Inside each pool, the "cheap model" is the smaller, cheaper one and the "strong model" is the larger, costlier one. The sensitivity detector (the later component that spots personal or confidential content in a prompt) is built by another sub-team and is not part of Phase 1. In the gateway it runs in parallel with our classifier as its own service.
No model is run or paid for in Phase 1: all answers and judge scores come from SPROUT (a public dataset of 44,000 prompts, each with stored answers from 13 AI models and a 0-to-1 quality score for each answer, given by an AI "judge"). The only things you run are the classifier (the model that predicts how hard a prompt is) and the baselines (simple reference methods to compare against).

## What changed in v2.1 to v2.4

**v2.4 change:** the four roles are assigned to named people: Heshmat, Hana, Zeina and Sameh. No method or schedule changes.

**v2.3 changes (gateway contract).** The plan was checked against "SentryRoute — Tech Stack & Gateway API Contract" (21 Oct 2026). Where the two disagreed, the contract won:
1. **Output format replaced.** v2 promised `p_cheap_ext`, `p_small_loc`, `uncertain` and reserved `sensitivity_score` / `sensitive`. The contract's complexity service returns `request_id, tier, score, signals, model_version, latency_ms`, and sensitivity is a separate service. The sensitivity fields are removed from our output. The old names stay as internal names and are converted by a fixed tier rule.
2. **New section "Gateway contract: what Phase 1 must match"** with the binding facts, the mapping from our two heads to the contract, and six open questions for the contract author.
3. **Stage 0:** contract questions, a mock complexity service (the contract's "mocks first" rule) and engineering conventions.
4. **Stage 4:** RouteLLM added as a baseline, because the contract names it as the baseline to beat.
5. **New Stage 5b:** wrap the trained model as `/v1/classify`, and measure CPU latency against the contract's 250 ms deadline and 100 ms target.
6. **Pre-registration:** tier rule, serving input rule, latency budget, and a day-1 check that the local stand-in pair is realistic for the team's laptops.
7. **Stage 8:** "uncertain" becomes tier `moderate`; tier counts are reported.
8. **Team split:** Sameh owns the contract and mock, Zeina owns the serving wrapper.

**v2.2 change:** every abbreviation and technical term now has its plain meaning where it first appears. No method changes.

Changes from v2 are marked **[v2.1]** in the text. The v1 → v2 fixes are now part of the baseline and no longer marked.

1. **Uncertainty margin fixed (Stage 8).** In v2, prompts within 0.1 of tau went to the strong model. Tau (written τ) is the score cutoff: prompts scoring at or above it go to the cheap model, the rest to the strong model. The half below tau already goes to strong, so this silently raised the cutoff to tau + 0.1 and broke the 10% under-routing rule (under-routing = a hard prompt, one that only the strong model answers adequately, wrongly sent to the cheap model). The margin is now only above tau, and results are reported at both operating points.
2. **Near-duplicate check fixed (Stage 3).** "Same first 200 characters" would flag thousands of false duplicates, because many sources share an instruction template or system prompt at the start. Replaced with a full-text hash (a short fingerprint of the whole prompt; identical prompts give identical fingerprints), a (source, index) check and a similarity check.
3. **Outcome metrics now include infeasible prompts (Stage 8).** In deployment you can't know which prompts are infeasible (prompts that neither the cheap nor the strong model answers adequately), so the realistic average score must include them. Labelled-only numbers are reported alongside.
4. **Oracle defined (Stage 8).** The oracle is the best possible routing, used as a ceiling to compare against. It was undefined for infeasible prompts.
5. **Long prompts (Stage 5).** Prompts reach 87,000 characters, longer than the model can read. Truncation (cutting a too-long prompt down to fit) is now fixed in advance: keep the start and the end.
6. **Source-prior baseline caveat (Stage 4).** The source-prior baseline predicts a prompt's difficulty from the average easy-rate (share of prompts the cheap model answers adequately) of its source dataset. It uses the dataset name, which the gateway (the system that receives real user prompts and routes them) will never see, so it is a reference point, not a fair competitor.
7. **Paired comparisons (Stage 6).** "Classifier beats baseline" is now tested with a paired bootstrap (re-sampling the same test prompts many times for both methods and looking at the difference between their scores) which gives a confidence interval (CI: a range the true value very likely lies in) for the difference, instead of comparing two separate intervals.
8. **Known SPROUT facts added (Stage 1).** Actual column names, and `key` as the prompt ID.
9. **Schedule contradictions fixed (team split).** Judge hand-check timing, ablation (an experiment that changes or removes one part to see what it does) training timing, and who may touch the test split now agree between the stages and the team plan.
10. **Pre-registration expanded** (pre-registration = writing your choices down before seeing results, so they can't be tuned afterwards) to include the model pairs, backup pair, margin width and truncation rule.

---

## Pre-registered choices

Write these into `notes/preregistration.md` on day 1, before any result exists. Changing one later is allowed only with a written reason and date.

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

---

## Gateway contract: what Phase 1 must match

Source: "SentryRoute — Tech Stack & Gateway API Contract" (21 Oct 2026, @karim). The machine-readable version, `api/openapi.yaml` in the gateway repo, is the source of truth. **If this plan and the contract disagree, the contract wins and the plan changes.**

**Where we fit.** A request reaches the gateway. Two separate services run in parallel on it: the **sensitivity service** and the **complexity service**. The **policy router** then keeps the strictest sensitivity result and picks the cheapest model that fits the complexity tier: sensitive goes to the local pool (Ollama on two team laptops), the rest to the external pool. **Our Phase 1 classifier is the complexity service.** The sensitivity service, the router and the policy are not our part.

| What the contract says | What Phase 1 does about it |
|---|---|
| Complexity is a small fine-tuned encoder behind `POST /v1/classify`, `GET /v1/info`, `GET /healthz`, on the private network only | Stage 5b wraps the trained model this way (Zeina) |
| Request: `request_id`, `messages`, `deadline_ms` | Serving input rule in the pre-registration table |
| Response: `request_id`, `tier` (`simple` / `moderate` / `complex`), `score`, `signals`, `model_version`, `latency_ms` | Tier rule in the pre-registration table. `signals` is returned as an empty list in Phase 1 |
| Sensitivity is a separate service with its own response (`label`, `score`, `categories`) | The v2 fields `sensitivity_score` and `sensitive` are **removed** from our output |
| Complexity weights the last user turn and may truncate earlier turns | Head + tail truncation keeps the last user turn. SPROUT is single-turn, so multi-turn is untested and goes in the limits |
| 250 ms deadline per check. Timeout or error: the gateway uses `complex` with `degraded: true` | Our service only needs to answer in time; the gateway sets `degraded` |
| Routing overhead target under 100 ms at p95 on CPU, prompts under 2,000 tokens (proposed) | Stage 5b measures it on CPU |
| No prompt text at rest: not in logs, traces or the decision record | The service logs `request_id`, token count and latency only. SPROUT files are public benchmark text, so they may be stored |
| Each team ships a mock in week one | Stage 0 mock complexity service (Sameh) |
| RouteLLM is the baseline to beat, kept in the eval environment only (it depends on LiteLLM, which stays out of the gateway image) | Stage 4 baseline, separate environment |
| Python 3.12, FastAPI, Pydantic v2; `uv` lockfile with hashes; ruff, mypy, pytest in CI | Stage 0 conventions |
| Local models are small 4-bit models sized to two laptops' VRAM; the external models are still to be chosen | Day-1 check on the local stand-in pair (Stage 0) |
| Images and audio are out of scope for v1 | Text only |

**Update 26 Oct 2026:** question 1 below is answered. Contract v2 adds an optional `pools: {external, local}` to the complexity response (each `{tier, score}`), keeps the top-level `tier`/`score` as the more complex of the two, and the router reads `pools[locality]`. Question 3 (higher score = more complex) is answered yes. Where this section says the gateway sees only the more complex pool, read it as the fallback for consumers that ignore `pools`. See `notes/contract_decisions.md`.

**Our two heads, in contract terms.** The contract has one `tier` and one `score`, but we have a head per pool. Internally we keep `p_cheap_ext` (external pool) and `p_small_loc` (local pool), each the probability that the pool's cheap model is adequate. The tier rule converts each to a tier. The gateway sees the more complex of the two as the top-level `tier` and `score`, so it works with the contract as it stands. Per-pool results are kept in our own files.

**Open questions for the contract author (send on day 1):**
1. The contract has one tier for both pools. May we add an optional field, for example `pools: {external: {tier, score}, local: {tier, score}}`, next to the top-level fields? It needs a change to `openapi.yaml`.
2. With two models per pool, is this tier to model mapping right: `simple` goes to the cheap model, `moderate` and `complex` go to the strong model? That mapping lives in the policy.
3. Is `score` higher = more complex? We assume yes (it matches the fallback rule and the sensitivity example).
4. Will pools have more than two models? Three tiers suggest so; Phase 1 only models cheap versus strong.
5. Which GPUs and how much VRAM do the two laptops have? (Also an open question in the contract.)
6. Which CPU should the latency target be measured on?

---

## Stage 0: Setup (day 1) — SAMEH

Goal: remove everything that could block you later.

1. **Kaggle GPU.** Kaggle is a free website for running code notebooks; a GPU is a graphics processor that trains neural networks much faster than a normal CPU.
   - Every team member creates an account and verifies their phone number (without it the GPU option stays locked). Each account has its own quota, which the team split relies on.
   - Create a notebook, set Accelerator to GPU (2x T4 or P100: types of NVIDIA GPU that Kaggle offers), turn Internet on.
   - Quota is about 30 GPU hours a week per account; a session stops after 12 hours.
2. **Shared folder.** Google Drive or team repo with `data/`, `labels/`, `splits/`, `models/`, `scores/`, `results/`, `notes/`. Rule: nobody renames or overwrites files in place; new version = new name.
3. **SPROUT license question.** SPROUT's Hugging Face page (Hugging Face is the website that hosts open datasets and models) has no license (the legal permission to use it) and an empty README (the dataset's description page). Message your supervisor: "SPROUT's Hugging Face page shows no license. Can we use it for research and report results on it?" Record the question and date; don't wait for the answer to start.
4. **[v2.3] Read the gateway contract and settle the output with its author.** Read the section above. Phase 1 serves the contract's complexity response, not the old v2 fields. Send the six open questions on day 1 and record the answers in `notes/contract_decisions.md`. Until answered, use the rules in the pre-registration table.
5. **[v2.3] Mock complexity service (days 2-3).** The contract says each team ships a mock in week one. Build a small FastAPI service with `POST /v1/classify`, `GET /v1/info` (tiers `simple`, `moderate`, `complex`) and `GET /healthz`. It returns fixed tiers chosen by keyword, in the contract's exact response shape. Check its responses against `api/openapi.yaml` (ask for access to the gateway repo). Zeina reuses these checks in Stage 5b.
6. **[v2.3] Local pair check.** Ask which GPUs and how much VRAM the two team laptops have. A 70B model will not fit in typical laptop VRAM even at 4-bit. If the real local pool is limited to small models, switch the local stand-in pair to `wxai-llama-3-2-3b-instruct` → `wxai-llama-3-1-8b-instruct` (both in SPROUT) **before any labels are computed**, and update the pre-registration file.
7. **[v2.3] Engineering conventions from the contract.** Python 3.12, FastAPI and Pydantic v2 for anything that becomes a service. Pin dependencies with a `uv` lockfile with hashes. Run ruff, mypy and pytest on code that is merged. Notebooks are for experiments only.
8. **Pre-registration file.** Copy the table above into `notes/preregistration.md` and share it.

You end up with: GPU notebooks for all four people, the shared folder, a sent supervisor message, the sent contract questions, a conforming mock service, a confirmed local pair, and the pre-registration file.

Common mistake: skipping phone verification and discovering on day 5 that there is no GPU.

---

## Stage 1: Get and understand the data (days 1-2) — HESHMAT

Goal: understand SPROUT before using it.

1. Download with `datasets` (Hugging Face's Python library for downloading data): `CARROT-LLM-Routing/SPROUT` (CARROT is the research paper that released SPROUT). Expect train (31,000), validation (6,640), test (6,640).
2. **[v2.1] Confirm the columns.** From the dataset page, SPROUT should have:
   - `key` (64-character ID; **use this as `prompt_id` everywhere**), `dataset` (20 sources), `dataset_level` (7 values; a difficulty or grade label within a source), `dataset_idx` (the item's position inside its original source), `prompt`, `golden_answer` (the reference correct answer).
   - 13 model columns, including the four you need: `openai-gpt-4o`, `openai-gpt-4o-mini`, `wxai-llama-3-1-8b-instruct`, `wxai-llama-3-3-70b-instruct`.
   - Check these names in your own download. If any differ, update the pre-registration file before going further.
3. **[v2.1] Open one model cell.** Each model column holds a structure, not a single number. Find which field is the response, which is the judge output, and which is the score. Confirm the score is in [0, 1] and check for missing values. Write the field names into the data notes; everyone's code must use the same ones.
4. Read 20 random rows: `prompt`, `golden_answer`, `dataset`, `dataset_level`, and for one model its response, judge output and score. Ask: does a wrong answer get a low score?
5. **Score distribution.** Histogram (a bar chart counting how many scores fall in each range) of scores for each of the four models.
   - Almost all 0 or 1: the 0.5 cutoff is natural.
   - Continuous: record the share of scores between 0.4 and 0.6. Stage 2 uses it.
6. **[v2.1] Quick judge red-flag check (30 rows, day 2).** Read 30 rows across sources and mark whether each score looks right. This is only to catch a badly broken judge before labels are built. The full 100-row hand-check happens in Stage 1b.
7. Work out what `dataset_level` means and which values go with which sources. If it looks like MATH levels (MATH is a benchmark of competition math problems graded by difficulty levels 1 to 5), write that down.
8. Count prompts per source in each split. Flag tiny sources.
9. **[v2.1] Check `(dataset, dataset_idx)` pairs.** If the same pair appears in more than one split, it is the same original item; Stage 3 uses this.
10. Prompt length in ModernBERT tokens (ModernBERT is the open-source text-understanding model, 149 million parameters, that you will fine-tune; a token is a word piece): median (middle value), 95th percentile (the length 95% of prompts stay under), and counts over 2,048 and over 4,096. Note which sources have the long prompts (likely RAG, retrieval-augmented generation, where retrieved documents are pasted in before the question, or other long-context ones); Stage 5 truncation will hit them hardest.
11. Write `notes/data_notes.md` with all of the above.

You end up with: data notes, score histograms, the field names, and the red-flag check.

Common mistake: training straight away, then finding weeks later that one source has broken prompts or empty answers.

### Stage 1b: Full judge hand-check (days 5-7) — HESHMAT

Runs in parallel with training. It doesn't block anything, but it must finish before the report.

1. Sample 100 rows, stratified across sources (so every source is represented), with about 20 whose scores are near 0.5.
2. For each, read the prompt, golden answer and model response. Mark whether the judge score is right.
3. Record the disagreement rate overall, near the cutoff, and per source where possible.

This is the label-quality figure the report cites.

---

## Stage 2: Labels (days 2-3) — HESHMAT

Goal: turn stored model scores into easy / hard / infeasible labels for each pool.

**The rule (already pre-registered).** For each pool, with a cheap and a strong model:

| Condition | Label |
|---|---|
| cheap score >= 0.5 | **easy** (the cheap model is adequate) |
| cheap score < 0.5 and strong score >= 0.5 | **hard** (only the strong model is adequate) |
| both < 0.5 | **infeasible** (neither is adequate) |

Pools:
- External: cheap = GPT-4o-mini, strong = GPT-4o → label `easy_ext` (1 if the cheap external model is adequate).
- Local: cheap = Llama 3.1 8B, strong = Llama 3.3 70B → label `easy_loc` (same idea for the local pool).

Why this rule: it checks adequacy first, matching the literature review's definition of difficulty as required capability under a stated quality criterion. A rule like "cheap >= strong" would call "both scored 0" easy.

Steps:
1. Apply the rule to every prompt in all three SPROUT splits. Each prompt gets one label per pool: 1 (easy), 0 (hard) or `infeasible`.
2. Counts table: per pool, % easy / hard / infeasible, overall and per source, plus the share within 0.1 of the cutoff.
3. **Rule sensitivity.** Recompute labels with cutoffs 0.4 and 0.6 and report how many change. If many change, list it as a limitation.
4. **Balance check.**
   - If hard is under about 15% of labelled prompts in a pool, use class weights (making errors on the rarer class count more during training, preferred) or the tolerance idea (count the cheap model as easy if its score is within a small gap t of the strong model's, from the Hybrid LLM paper). Write down which.
   - **[v2.1]** If a local pool is badly unbalanced or more than about 40% infeasible, switch to the pre-registered backup pair now, before any training, and record the reason. Don't switch after seeing classifier results.
5. Infeasible prompts stay in the files but don't train that pool's head. Report their counts per pool and per source.
6. Overlap: how many prompts are infeasible in one pool but easy/hard in the other. This feeds RQ3 (RQ = research question; RQ3 asks whether one difficulty predictor can pick adequate models in both the local and external pools).

You end up with: `labels/labels_v1.csv`, the counts table, the rule-sensitivity table.

Common mistake: treating infeasible as hard. That teaches the classifier that "send to the big model" fixes prompts the big model also fails.

---

## Stage 3: Splits (day 3) — HESHMAT

Goal: four separate groups of prompts, fixed for the rest of the project.

1. **Train** = SPROUT train. **Test** = SPROUT test, kept exactly as released so results stay comparable with other SPROUT users.
2. Split SPROUT validation into two halves with seed 42:
   - **Calibration (~3,320):** used only to fit T in Stage 7 (T, the temperature, is one number that rescales the classifier's confidence so its scores match reality).
   - **Threshold (~3,320):** used for baselines, picking the best epoch (one full pass over the training data), and picking tau in Stage 8.
   - **[v2.1] Stratify (split so both halves have the same mix) on source × `easy_ext` label** (easy / hard / infeasible). Any source-label cell with fewer than 2 prompts goes into a shared "other" stratum so the split doesn't fail. Check that every source appears in both halves.
3. **[v2.1] Duplicates across the four parts.**
   - Exact: lowercase, collapse whitespace, hash the **full** prompt, compare hashes.
   - Same item: identical `(dataset, dataset_idx)` across parts (from Stage 1 step 9).
   - Near-duplicates: MinHash (a fast method for estimating how similar two texts are) on word 5-grams (every run of 5 consecutive words) using the `datasketch` Python library, flag pairs with estimated similarity >= 0.9, and read 20 flagged pairs to confirm they really are duplicates.
   - Don't use "same first N characters": many sources start every prompt with the same instruction text, so it would flag thousands of distinct prompts.
   - **Never alter the test set.** A train prompt that duplicates any other part is removed from train. A calibration or threshold prompt that duplicates a test prompt is removed from its half. Report how many were removed and from which sources.
4. Save `splits/split_v1.csv` (`prompt_id, split`) and announce it frozen.
5. From now on, nobody computes anything on the test part until Stage 6.

You end up with: one frozen split file and a duplicate report.

Common mistake: each teammate making their own random split, so nobody's numbers can be compared.

---

## Stage 4: Baselines (day 4) — HANA

Goal: know what "good" means before training the expensive model.

All baselines predict `easy_ext` and `easy_loc` and are scored on the **threshold** split only.

1. **Random.** A random score per prompt. AUROC should be about 0.5; if not, the evaluation code has a bug.
2. **Prompt length.** Logistic regression on log(token length), fitted on train, so the direction is learned rather than assumed.
3. **Source prior.** Score = the train easy-rate of the prompt's `dataset` (second version: `dataset` + `dataset_level`).
   - **[v2.1]** This baseline uses the source name, which the gateway will never have for real requests. It is a reference showing how much difficulty is explained by "which benchmark is this", not a deployable router. Report it in its own row, clearly labelled.
4. **TF-IDF + logistic regression.** Word and word-pair TF-IDF, one model per pool, balanced class weights if needed. Basic settings only.
5. **Frozen ModernBERT embeddings + logistic regression.** Embeddings (each prompt turned into a list of numbers that captures its meaning), averaged over all tokens (mean-pooled), from untouched ("frozen") ModernBERT-base, same truncation as Stage 5. Needs a GPU, so run it on your own Kaggle account.
6. **[v2.3] RouteLLM, the baseline the contract says to beat.** RouteLLM is an existing open-source router built for a strong and weak model pair. Score each threshold-split prompt with one of its pre-trained routers that runs locally, and use 1 − its "strong model needed" probability as the easy score. Check its documentation for which routers need no paid API. If only API-based ones work, skip it and say so rather than spending credits. It depends on LiteLLM, which the contract keeps out of the gateway image, so run it in a separate evaluation environment only. It was not trained on SPROUT labels, so it is an off-the-shelf reference, not a like-for-like competitor.
7. AUROC with bootstrap 95% confidence intervals (1,000 resamples) for every baseline × both pools.
8. **Gate 1:** if TF-IDF AUROC is below 0.6, text barely predicts difficulty under these labels. Stop and write a team decision before going on.
9. Save baseline models and threshold-split scores. Test-split scores are produced in Stage 6, after the freeze.

You end up with: an AUROC table (baselines × 2 pools, with CIs) and the Gate 1 decision.

Common mistake: tuning TF-IDF for hours. It only needs to be a fair reference.

---

## Stage 5: Train (days 5-7) — ZEINA

Goal: a trained ModernBERT classifier with two heads.

1. **Model.** ModernBERT-base (149M = 149 million parameters, the adjustable numbers inside the model). Mean-pool (average) token vectors into one prompt vector, feed it to two linear heads (`easy_ext`, `easy_loc`). The input is the prompt text only: never the source name or level. At serving time the `messages` list is flattened to one text by the serving input rule in the pre-registration table.
2. **Loss.** Binary cross-entropy (the standard loss, i.e. the penalty number training tries to minimise, for yes/no predictions) per head, masked so each head learns only from prompts labelled for its pool (infeasible skipped). Total loss = average of the two heads' losses. Class weights if decided in Stage 2.
3. **[v2.1] Long prompts.** Truncate to 2,048 tokens by keeping the first 1,536 and the last 512, so both the instruction and the final question survive in long RAG-style prompts. Use the same rule everywhere (baselines, training, inference). Record how many prompts were truncated, per source.
4. **Settings for T4 GPUs.**

| Setting | Value |
|---|---|
| Max length | 2,048 tokens, head + tail truncation |
| Learning rate | 2e-5 to 5e-5 (start at 3e-5): how big each training update is; 2e-5 means 0.00002 |
| Batch size | 4 per device, gradient accumulation 4 (effective 16): batch size = prompts processed at once; gradient accumulation = add up 4 small batches before each update, to act like a batch of 16 without the memory cost |
| Padding | dynamic, with length-grouped batching: padding fills shorter prompts with blanks so a batch lines up; dynamic = only up to the longest prompt in that batch; length-grouped = batch similar-length prompts together |
| Epochs | 2-3 |
| Precision | fp16 (16-bit numbers: faster and lighter on memory; T4 lacks bf16, a more stable 16-bit format); watch for NaN loss (the loss becomes "not a number", meaning training broke) and lower the learning rate if it appears |
| Attention | FlashAttention (a faster, memory-saving way to compute attention, the part of the model that relates words to each other) isn't supported on T4, so the standard attention path is used; check your `transformers` version (Hugging Face's Python library that provides ModernBERT) supports ModernBERT |

5. **Trial run first:** 2,000 prompts, 1 epoch. Check that loss goes down, nothing crashes, no NaN, predictions aren't all the same.
6. Full run on all train prompts. Checkpoint (a saved copy of the model's weights) every epoch (sessions stop at 12 hours).
7. After each epoch, AUROC on the threshold split. Keep the epoch with the best mean AUROC across the two heads.
8. **Seeds.** If quota allows, 2 more seeds and report mean and spread. Otherwise say one seed was used.
9. **[v2.1] Ablation training (for RQ3), started here, not on day 8.** Using the same script and settings, on another teammate's Kaggle account:
   - (a) one shared head trained only on `easy_ext`, later applied to both pools;
   - (c) two separate single-head models, one per pool.
   Pick each model's epoch on the threshold split, same as the main model. If quota is short, train (a) only and record (c) as future work.
10. Training log: settings, time per epoch, AUROC per epoch, GPU used, truncation counts.
11. **Gate 2:** the best checkpoint must beat TF-IDF AUROC for both pools on the threshold split. If not, check for bugs first (labels misaligned with prompts?), then try another learning rate or the 4,096 length.
12. Also compare against the frozen-embedding and source-prior baselines, and report it honestly either way.

You end up with: a saved model, ablation models, a training log, and the Gate 2 decision.

Common mistake: skipping the trial run and losing 6 GPU hours to a bug that would have shown up in 10 minutes.

---

## Stage 5b: Serving wrapper and latency check (days 8-10) — ZEINA

Goal: show the trained model can sit behind the gateway's complexity contract and answer in time.

1. **Wrap the frozen model** in a small FastAPI service with `POST /v1/classify`, `GET /v1/info` (name, version, tiers) and `GET /healthz` (model loaded), with request and response shapes exactly as in the contract. It reads the two frozen taus from a config file that Sameh fills on day 9, applies the tier rule, and returns the more complex pool's tier and score at the top level.
2. **Conformance.** Run Sameh's mock test checks against it, and validate its responses against `api/openapi.yaml`.
3. **Latency on CPU, not the Kaggle GPU.** Use prompts from the threshold split (prompts only, no labels needed), batch size 1, including some near 2,000 tokens. Report p50 and p95 and the CPU model and thread count. Try PyTorch first; if p95 is over budget, export to ONNX Runtime and measure again. Compare with the 250 ms deadline and the under-100 ms target.
4. **Logging rule.** The service logs only `request_id`, token count and latency. It never writes request text.
5. **If it is too slow:** report the numbers and the options (shorter maximum length, a smaller encoder, ONNX) with their effect on AUROC, and let the team and the contract author choose. Don't change the frozen model silently.

You end up with: a service folder, a conformance result and a latency table.

Common mistake: measuring speed on the GPU notebook. The gateway runs the classifier on CPU.

---

## Stage 6: Check 1, ranking (day 8) — HANA (ablation scores: ZEINA)

Goal: show the classifier puts easy prompts above hard ones.

1. **Freeze** the main model and the ablation models. No retraining after this point.
2. Zeina produces scores for the calibration, threshold and test splits (raw logits: the head's number before it is converted to a 0-to-1 probability) and puts them in `scores/`.
3. Test-split AUROC per head with bootstrap 95% CIs. This is allowed now because AUROC doesn't depend on T or tau.
4. **[v2.1] Paired comparison.** For each baseline, bootstrap the **difference** (classifier AUROC − baseline AUROC) by resampling the same prompts for both. Claim "the classifier beats X" only if the 95% interval of the difference is above 0.
5. Per source: AUROC for each `dataset` with at least 50 easy and 50 hard test prompts; others are labelled "too few to judge".
6. Final table: random / length / TF-IDF / frozen embeddings / classifier, both pools, with the source prior in a separate labelled row.
7. Mistakes: sort by "most confident and wrong" and read the top 20 in each direction. "Said easy, was hard" is the dangerous direction. Write down patterns.
8. **RQ3 pilot ablation.** Test AUROC for the local pool under (a) shared head, (b) the two-head model, (c) separate models, with paired bootstrap differences against (b).

You end up with: the AUROC tables (overall, per source, paired differences), the ablation table, and the mistake notes.

Common mistake: reporting only the overall number. One weak source can cause most bad routing later.

---

## Stage 7: Check 2, honest scores (days 8-9) — SAMEH

Goal: make a score of 0.8 mean "about 80% chance the cheap model is adequate". This is called calibration.

1. **Before fixing:** on the calibration split, 10 equal-width score bins; compare average score with the real share of easy prompts. Reliability diagram per head (a plot of predicted probability against the real share of easy prompts; a perfectly calibrated classifier lies on the diagonal).
2. ECE (expected calibration error: the average gap between predicted probability and how often prompts are really easy; 0 is perfect), Brier score (average squared error of the predicted probabilities; lower is better) and log-loss (a penalty that is large when the classifier is confidently wrong; lower is better).
3. Fit temperature T per head on the calibration split (raw logit ÷ T before the sigmoid, the function that squashes any number into a 0-to-1 probability; choose T with the lowest log-loss). T > 1 means overconfident, T < 1 means too timid. **Freeze T before looking at test calibration.**
4. On the test split: reliability diagram, ECE, Brier and log-loss, before and after T, with bootstrap CIs on ECE.
5. Target ECE about 0.05 or lower after T. This is a pre-registered target, not a standard. If it is clearly higher, record it as a weak spot; don't adjust anything to fix the test result.
6. Per-source ECE for sources with enough prompts.

You end up with: before/after reliability diagrams for both heads, a metrics table, the T values.

Common mistake: fitting T on the test split. The "after" result then looks perfect but means nothing.

---

## Stage 8: Check 3, decisions and outcomes (day 9) — SAMEH

Goal: turn scores into routing decisions and measure what they deliver.

**8A. Pick tau.**
1. Rule (pre-registered): tau = the lowest threshold at which at most 10% of hard prompts get a score >= tau.
2. On the threshold split, calibrated scores, labelled prompts only (infeasible excluded): try tau = 0.00, 0.01, ..., 1.00 and take the lowest that meets the rule. Freeze tau for each pool **before** any test-split routing number is computed.

**8B. [v2.1] Two operating points.**

Sending "unsure" prompts to the strong model is the same as raising the threshold, so state both operating points plainly (an operating point is one particular cutoff setting, which fixes the trade-off between cheapness and quality):

| Operating point | Sent to cheap if | Use |
|---|---|---|
| **Plain** | score >= tau | Meets the 10% rule by construction |
| **With margin** | score >= tau + 0.1 | Safer; costs more over-routing |

Prompts with tau <= score < tau + 0.1 get tier `moderate` (the unsure band) for the gateway; below tau is `complex` and at or above tau + 0.1 is `simple`. Sameh writes both taus into the config file used by Stage 5b, and reports the share of test prompts in each tier per pool. Below tau they already go to the strong model, so there is no "unsure" zone below tau.

Every result in 8C to 8E is reported for both operating points.

**8C. Four-box table on the test split, per pool** (labelled prompts only; a 2×2 count of easy/hard prompts against cheap/strong decisions):

| | Sent to cheap | Sent to strong |
|---|---|---|
| Really easy | correct, saved cost | over-routing (an easy prompt wasted on the strong model) |
| Really hard | under-routing (bad answer) | correct |

With 95% bootstrap CIs:
- under-routing % = hard sent to cheap ÷ all hard
- over-routing % = easy sent to strong ÷ all easy
- share sent to cheap

**8D. Outcome metrics.**

For each test prompt, the routed score is the stored score of whichever model it was sent to. Per pool:
1. **[v2.1] Average routed score and share sent to cheap, over all test prompts including infeasible ones.** This is the realistic number, since the gateway can't tell which prompts are infeasible. Report the labelled-only version alongside.
2. The same two numbers for:
   - **always-strong**
   - **always-cheap**
   - **random routing** at the same cheap share (expected value)
   - **[v2.1] oracle**: send to cheap when the cheap model is adequate *or* when both fail; send to strong only for hard prompts. This is the best possible routing given the labels. If scores are continuous rather than 0/1, note that on infeasible prompts the strong model can still score slightly higher, so the oracle gives up a little score there.
3. **Trade-off curve:** sweep tau from 0 to 1, plot average routed score against share sent to cheap, mark always-strong, always-cheap, random and oracle, and both operating points.
4. "Share sent to cheap" is a proxy for cost, not money. Don't call it a cost saving without real prices.

**8E. Uncertainty zone analysis.**
- Share of prompts flagged uncertain.
- Under-routing among flagged prompts vs. among prompts above tau + 0.1. If the flag is useful, the flagged group should be clearly worse.
- For later: in the full system, an uncertain *sensitive* request must escalate to the strongest permitted local model, never to an external one.

**8F. Gate 3.** Test under-routing at the plain operating point vs. the 10% target, using its CI. About 12% or lower: the threshold carries over to new prompts. Far off: the threshold and test splits behave differently; report it honestly.

You end up with: tau per pool, four-box tables and outcome tables at both operating points, trade-off curves, the uncertainty analysis, and the Gate 3 decision.

Common mistake: trying several tau values on the test split and keeping the best-looking one.

---

## Stage 9: Report (day 10) — SAMEH assembles; everyone writes their own section

Goal: one to two pages the team, mentor and supervisor can read in five minutes.

1. **Headline**, one line, written after the results.
2. **Setup in 3 lines:** data and splits, model pairs, label rule.
3. **Label quality:** red-flag and 100-row hand-check disagreement rates, rule-sensitivity result.
4. **Check 1:** AUROC tables with CIs and paired differences, worst sources, mistake patterns, RQ3 ablation.
5. **Check 2:** reliability diagrams, ECE / Brier / log-loss, T values.
6. **Check 3:** tau, both operating points, four-box and outcome tables, trade-off curve, uncertainty analysis.
7. **Gates:** pass/fail for Gates 1-3, with numbers. Also **contract fit**: conformance result, CPU latency table, and the status of the six questions to the contract author.
8. **Weak spots and limits:**
   - Stand-in models (GPT-4o pair, Llama pair: substitutes used because SPROUT contains them), not the real pool.
   - Labels come from SPROUT's AI judge; hand-check disagreement was X%.
   - The threshold split was reused for epoch choice, baselines and tau, so those numbers are slightly optimistic.
   - **[v2.1]** Long prompts were truncated (head + tail); N prompts affected, mostly from sources Y.
   - **[v2.1]** The source-prior baseline uses metadata the gateway won't have.
   - Seeds used and their spread.
   - Small sources that couldn't be judged.
   - Share sent to cheap is a proxy, not measured cost or latency.
   - No sensitivity component yet, so RQ1 and RQ2 are untested.
   - **[v2.3]** SPROUT prompts are single-turn, so multi-turn conversations, which the gateway will send, are untested.
   - **[v2.3]** The local pair is a stand-in sized by what SPROUT contains, not by what the team's laptops can run, unless Stage 0 step 6 changed it.
9. **Next (Phase 2):** real-pool labels (labels made from your own real models instead of SPROUT's stand-ins), measuring how reliably the sensitivity detector finds personal and confidential content (RQ2), the comparison of joint, separate and shared-head predictors (RQ1: one model doing both jobs, two independent models, or one shared encoder with two heads), full-system cost and latency (RQ4: money and response time), and LLMRouterBench (a published benchmark and common framework for comparing LLM routing methods, cited in your proposal).

You end up with: the results page in the shared folder, presented at the sprint review.

Common mistake: hiding bad results. A clear "it fails on long RAG prompts" is worth more to examiners than a page of only good numbers.

---

## Team split (4 people)

Split by who owns which output, with fixed file formats between people. Everyone builds and tests their part on stand-in data until the real labels exist.

### Roles

| Person | Owns | Stages |
|---|---|---|
| **Heshmat: Data and labels** | Data notes, labels, splits, judge checks | 1, 1b, 2, 3 |
| **Hana: Baselines and evaluation code** | Baselines plus the shared metrics library (AUROC, bootstrap and paired bootstrap, four-box, outcome curves) | 4, 6 |
| **Zeina: Training** | Training script, GPU runs, ablation models, all classifier score files, serving wrapper and latency check | 5, 5b, plus ablation scores in 6 |
| **Sameh: Calibration, decisions and report** | Admin, gateway contract and mock service, calibration, tau, outcomes, report assembly | 0, 7, 8, 9 |

### Who is who

| Person | Role | Why this fit |
|---|---|---|
| **Heshmat** | Data and labels (Stages 1, 1b, 2, 3) | Everything waits on the frozen labels and split file, so this role needs the person who knows the plan best and can keep it consistent |
| **Hana** | Baselines and evaluation code (Stages 4, 6) | Statistics and metrics code: AUROC, bootstrap, the RouteLLM baseline and the final tables |
| **Zeina** | Training and serving (Stages 5, 5b, ablation scores) | The most hands-on GPU and model work, and the service wrapper that ends the phase |
| **Sameh** | Calibration, decisions, contract and report (Stages 0, 7, 8, 9) | Already assigned |

These three assignments are my suggestion, made without knowing anyone's skills. They can be swapped freely: only the owner names change, the work and the file formats stay the same. If someone is stronger at coding, put them on training (Zeina's role); if someone is stronger at writing and careful checking, put them on data and labels (Heshmat's role).

### Timeline

**Days 1-3 (everyone builds on stand-in data):**
- **Heshmat** is the critical path (the chain of tasks that sets the earliest finish date; if it slips, everything slips). Everything waits on the frozen labels and split file, so Heshmat does nothing else until day 3.
- **Hana** writes the metrics library and tests it on random scores and fake labels (random scores should give AUROC about 0.5).
- **Zeina** writes the training script with masked loss and head + tail truncation, and runs it on a tiny dummy dataset so GPU problems show up now.
- **Sameh** does Stage 0, including reading the contract, sending the open questions and building the mock complexity service by day 3, and writes the calibration, tau and outcome code against fake scores.

**Day 3:** Heshmat announces the frozen labels and split. This is the only hard sync point (a moment when everyone must be working from the same files).

**Day 4:** Hana runs the baselines on the threshold split and reports Gate 1. Zeina does the trial run (2,000 prompts).

**Days 5-7:**
- **Zeina** runs the full training on their Kaggle account.
- **Heshmat** runs the ablation training (Stage 5 step 9) on their own Kaggle account using Zeina's script unchanged, and does the 100-row hand-check (Stage 1b).
- **Hana** finishes the baselines and builds the mistake-reading tooling.
- **Sameh** reviews the Stage 7 and 8 code and drafts the report skeleton.

**Day 8:** Zeina freezes all models, delivers the score files, then builds the Stage 5b serving wrapper (days 8-10). Hana runs Stage 6. Heshmat and Hana split the mistake reading, 20 per direction each.

**Days 8-9:** Sameh runs Stage 7, then Stage 8.

**Day 10:** each person writes their own section; Sameh assembles; everyone checks the numbers in their section against the files.

### File formats to agree on day 1

- **Labels file:** `prompt_id (= SPROUT key), dataset, dataset_level, easy_ext, easy_loc, score_gpt4o_mini, score_gpt4o, score_llama8b, score_llama70b`
- **Split file:** `prompt_id, split` (values: train / calibration / threshold / test)
- **Scores file (Zeina produces, Hana and Sameh consume):** `prompt_id, split, model_name, head, raw_logit`. Raw logits, so Sameh can fit T without retraining. `model_name` distinguishes the main model from the ablation models.

- **[v2.3] Gateway shapes:** requests and responses follow `api/openapi.yaml` exactly. Our internal names `p_cheap_ext` and `p_small_loc` appear only in our own files, never in the gateway response.

### Rules that keep it safe

- **The test split is locked until day 8.** Nobody scores, plots or inspects test results before the models are frozen.
- **[v2.1] Order of unlocking after day 8:** test AUROC (Stage 6) is allowed once models are frozen; test calibration only after T is frozen; test routing numbers only after tau is frozen.
- **Only Zeina produces classifier scores.** Hana produces baseline test scores, also only after day 8.
- **Sameh owns T and tau.** Nobody else tunes thresholds.
- **Use every Kaggle account.** Each has its own quota; that's why Heshmat runs the ablation training in parallel with Zeina's main run.
- **[v2.3] The contract wins.** If the plan and the gateway contract disagree, change the plan. Changes to the contract itself go through its author.
- **Keep the work balanced.** If one person is stronger at coding, move the seed runs to them.
