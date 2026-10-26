#!/usr/bin/env python3
"""SentryRoute Phase 1, Stage 1: understand SPROUT. Run: python stage1_explore.py [--out notes] [--local DIR]
Writes everything into --out (default ./notes). Needs: datasets pandas numpy matplotlib (transformers optional, for exact ModernBERT token counts).
--local DIR: read DIR/{train,validation,test}.jsonl instead of Hugging Face (used for testing)."""
import argparse, json, os, re, sys, ast
import numpy as np, pandas as pd

MODELS = ["openai-gpt-4o", "openai-gpt-4o-mini", "wxai-llama-3-1-8b-instruct", "wxai-llama-3-3-70b-instruct"]
EXPECTED = ["key", "dataset", "dataset_level", "dataset_idx", "prompt", "golden_answer"]
ap = argparse.ArgumentParser()
ap.add_argument("--out", default="notes"); ap.add_argument("--local")
ap.add_argument("--score-field"); ap.add_argument("--response-field"); ap.add_argument("--judge-field")
ap.add_argument("--no-tokenizer", action="store_true")
ap.add_argument("--samples-only", action="store_true", help="stop after writing the 20-row and 30-row reading files")
A = ap.parse_args()
os.makedirs(A.out, exist_ok=True)
notes = []
def say(s=""): print(s); notes.append(s)

# ---------- 1. load ----------
if A.local:
    splits = {s: pd.read_json(f"{A.local}/{s}.jsonl", lines=True) for s in ["train", "validation", "test"]}
else:
    from datasets import load_dataset
    ds = load_dataset("CARROT-LLM-Routing/SPROUT")
    splits = {k: v.to_pandas() for k, v in ds.items()}
say("## 1. Splits")
for k, v in splits.items(): say(f"- {k}: {len(v):,} rows (plan expects train 31,000 / validation 6,640 / test 6,640)")
cols = list(splits["train"].columns)
say("\n## 2. Columns")
say(f"All columns ({len(cols)}): {cols}")
missing = [c for c in EXPECTED + MODELS if c not in cols]
say(f"Expected columns missing: {missing or 'none'}")
extra_models = [c for c in cols if c not in EXPECTED]
say(f"Model columns found ({len(extra_models)}; plan expects 13): {extra_models}")
if missing: say("**ACTION: update notes/preregistration.md with the real names before going on.**")
for k, v in splits.items():
    say(f"- {k}: key unique={v['key'].is_unique}, key length set={sorted(v['key'].astype(str).str.len().unique())[:3]}")

# ---------- 3. model cell structure ----------
def as_obj(x):
    if isinstance(x, (dict, list)) or x is None: return x
    if isinstance(x, str):
        for f in (json.loads, ast.literal_eval):
            try: return f(x)
            except Exception: pass
    return x
tr = splits["train"]
say("\n## 3. Model cell structure")
m0 = MODELS[0] if MODELS[0] in cols else extra_models[0]
cell = as_obj(tr[m0].iloc[0])
say(f"Column `{m0}`: python type {type(tr[m0].iloc[0]).__name__}, parsed type {type(cell).__name__}")
def describe(o, pre=""):
    if isinstance(o, dict):
        for k, v in o.items(): say(f"  {pre}{k!r}: {type(v).__name__} = {str(v)[:100]!r}"); 
    else: say(f"  {str(o)[:200]!r}")
describe(cell)

def find_fields(cell):
    """Guess response / judge / score fields. Override with --*-field if wrong."""
    if not isinstance(cell, dict): return None, None, None
    keys = list(cell)
    score = A.score_field or next((k for k in keys if re.search(r"score|reward|grade|quality|metric", k, re.I)
                                   and isinstance(cell[k], (int, float))), None)
    if score is None:
        score = next((k for k in keys if isinstance(cell[k], (int, float)) and not isinstance(cell[k], bool)), None)
    resp = A.response_field or ("response" if "response" in cell else next((k for k in keys if re.search(r"answer|output|text|completion|generat|resp", k, re.I) and "judge" not in k.lower()), None))
    judge = A.judge_field or ("judge_response" if "judge_response" in cell else None) or next((k for k in keys if re.search(r"judge|eval|reason|feedback|explan", k, re.I) and k != score), None)
    return resp, judge, score
RESP, JUDGE, SCORE = find_fields(cell)
say(f"\nGuessed fields -> response: `{RESP}`, judge output: `{JUDGE}`, score: `{SCORE}`  (CHECK THESE; override with --response-field/--judge-field/--score-field)")
if SCORE is None and not isinstance(cell, dict):
    say("Cell is not a dict. If the cell is a bare number it is the score; edit get_score() below."); 
def get_score(x):
    o = as_obj(x)
    if isinstance(o, dict): 
        v = o.get(SCORE); 
        return float(v) if isinstance(v, (int, float)) else np.nan
    return float(o) if isinstance(o, (int, float)) else np.nan

for k in splits:
    for m in MODELS:
        if m in splits[k]: splits[k][f"s::{m}"] = splits[k][m].map(get_score)
S = pd.concat([v.assign(split=k) for k, v in splits.items()], ignore_index=True)

# ---------- 4. 20 random rows ----------
rng = np.random.RandomState(42)
samp = tr.sample(20, random_state=42)
with open(f"{A.out}/sample_20_rows.md", "w") as f:
    for _, r in samp.iterrows():
        f.write(f"### {r['key'][:12]} | {r['dataset']} | level={r['dataset_level']}\n**PROMPT:** {str(r['prompt'])[:1500]}\n\n**GOLDEN:** {str(r['golden_answer'])[:500]}\n\n")
        c = as_obj(r[m0]); f.write(f"**{m0}**: " + (json.dumps({k: (str(v)[:800]) for k, v in c.items()}, indent=1) if isinstance(c, dict) else str(c)[:800]) + "\n\n---\n")
say("\n## 4. 20 random rows written to sample_20_rows.md (read them; does a wrong answer get a low score?)")

# ---------- 5. score distributions ----------
say("\n## 5. Score distributions (all splits pooled)")
rows = []
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 4, figsize=(16, 3.2), sharey=True)
for a, m in zip(ax, MODELS):
    c = f"s::{m}"
    if c not in S: continue
    s = S[c]
    a.hist(s.dropna(), bins=20, range=(0, 1)); a.set_title(m, fontsize=8)
    rows.append(dict(model=m, n=len(s), missing=int(s.isna().sum()), min=s.min(), max=s.max(), mean=round(s.mean(), 3),
                     pct_exact_0_or_1=round(100 * s.isin([0, 1]).mean(), 1), pct_0_4_to_0_6=round(100 * s.between(0.4, 0.6, inclusive="neither").mean(), 2),
                     pct_ge_0_5=round(100 * (s >= 0.5).mean(), 1)))
plt.tight_layout(); plt.savefig(f"{A.out}/score_histograms.png", dpi=130)
dist = pd.DataFrame(rows); say(dist.to_markdown(index=False)); dist.to_csv(f"{A.out}/score_distribution.csv", index=False)
say("Reading: if pct_exact_0_or_1 is ~100 the 0.5 cutoff is natural; otherwise note pct_0_4_to_0_6 for Stage 2. Also check min>=0, max<=1.")
bad = {m: int(((S[f's::{m}'] < 0) | (S[f's::{m}'] > 1)).sum()) for m in MODELS if f"s::{m}" in S}
say(f"Scores outside [0,1]: {bad}")

# ---------- 6. 30-row red-flag sample ----------
_sh = S.sample(frac=1, random_state=1); rf = _sh.groupby("dataset").head(2).sample(frac=1, random_state=1).head(30)
with open(f"{A.out}/redflag_30_rows.md", "w") as f:
    f.write("Mark each: score looks right? (Y/N)\n\n")
    for i, (_, r) in enumerate(rf.iterrows(), 1):
        c = as_obj(r[m0])
        f.write(f"### {i}. {r['dataset']} | {r['key'][:12]} | {m0} score={r.get(f's::{m0}')}\nPROMPT: {str(r['prompt'])[:800]}\nGOLDEN: {str(r['golden_answer'])[:300]}\nRESPONSE: {str(c.get(RESP) if isinstance(c, dict) else c)[:800]}\nJUDGE: {str(c.get(JUDGE) if isinstance(c, dict) and JUDGE else '')[:400]}\n\n[ ] judge right   [ ] judge wrong\n\n---\n")
say("\n## 6. Red-flag sample: fill in redflag_30_rows.md by hand (30 rows, mark Y/N), report the N count here: ___ / 30")

if A.samples_only:
    print("Samples written (samples-only mode)."); sys.exit(0)

# ---------- 7. dataset_level ----------
say("\n## 7. dataset_level by dataset (check: MATH-like 1-5?)")
xt = pd.crosstab(S["dataset"], S["dataset_level"].astype(str)); xt.to_csv(f"{A.out}/dataset_x_level.csv")
say(f"dataset_level values: {sorted(S['dataset_level'].astype(str).unique())}")
say(xt.to_markdown())

# ---------- 8. per-source counts ----------
say("\n## 8. Prompts per source per split (flag < 50 in any split)")
pc = pd.crosstab(S["dataset"], S["split"])[["train", "validation", "test"]]; pc["total"] = pc.sum(axis=1)
pc.to_csv(f"{A.out}/source_counts.csv"); say(pc.to_markdown())
tiny = pc[(pc[["train", "validation", "test"]] < 50).any(axis=1)].index.tolist(); say(f"Small sources (<50 in some split): {tiny or 'none'}")
say(f"Number of sources: {S['dataset'].nunique()} (plan expects 20); levels: {S['dataset_level'].nunique()} (expects 7)")

# ---------- 9. (dataset, dataset_idx) overlap ----------
say("\n## 9. (dataset, dataset_idx) overlap across splits")
S["pair"] = S["dataset"].astype(str) + "||" + S["dataset_idx"].astype(str)
g = S.groupby("pair")["split"].agg(lambda x: tuple(sorted(set(x))))
multi = g[g.map(len) > 1]
say(f"Pairs in more than one split: {len(multi):,} of {len(g):,}")
if len(multi): say(multi.value_counts().to_string())
dup_in = S.duplicated("pair", keep=False).sum(); say(f"Rows sharing a pair with another row (any split): {dup_in}")
S[S["pair"].isin(multi.index)][["key", "split", "dataset", "dataset_idx"]].to_csv(f"{A.out}/pair_overlap.csv", index=False)

# ---------- 10. lengths ----------
say("\n## 10. Prompt length (ModernBERT tokens)")
tok = None
if not A.no_tokenizer:
    try:
        from transformers import AutoTokenizer; tok = AutoTokenizer.from_pretrained("answerdotai/ModernBERT-base")
    except Exception as e: say(f"(tokenizer unavailable: {e}; using chars/4 estimate)")
txt = S["prompt"].astype(str)
S["ntok"] = [len(x) for x in tok(list(txt), add_special_tokens=False)["input_ids"]] if tok else (txt.str.len() / 4).round().astype(int)
say(f"Method: {'ModernBERT tokenizer' if tok else 'chars/4 ESTIMATE - rerun with transformers installed'}")
q = S["ntok"].quantile([.5, .95]).tolist()
say(f"median={q[0]:.0f}, p95={q[1]:.0f}, >2048: {(S.ntok>2048).sum()}, >4096: {(S.ntok>4096).sum()}, max={S.ntok.max()}, max chars={txt.str.len().max()}")
lg = S.groupby("dataset").agg(n=("ntok", "size"), median=("ntok", "median"), p95=("ntok", lambda x: x.quantile(.95)), over2048=("ntok", lambda x: (x > 2048).sum()), over4096=("ntok", lambda x: (x > 4096).sum())).sort_values("over2048", ascending=False)
lg.to_csv(f"{A.out}/length_by_source.csv"); say(lg.round(0).to_markdown())

# ---------- extras useful for Stage 2 ----------
say("\n## Extra: quick easy-rate preview at cutoff 0.5 (NOT final labels; Stage 2 makes those)")
for cheap, strong, nm in [(MODELS[1], MODELS[0], "external"), (MODELS[2], MODELS[3], "local")]:
    if f"s::{cheap}" in S and f"s::{strong}" in S:
        c, s_ = S[f"s::{cheap}"], S[f"s::{strong}"]
        ok = c.notna() & s_.notna()
        say(f"- {nm}: easy {100*(c[ok]>=.5).mean():.1f}% | hard {100*((c[ok]<.5)&(s_[ok]>=.5)).mean():.1f}% | infeasible {100*((c[ok]<.5)&(s_[ok]<.5)).mean():.1f}% (rows with both scores: {ok.sum()})")
open(f"{A.out}/data_notes_DRAFT.md", "w").write("# SPROUT data notes (auto-generated draft, Stage 1)\n\n" + "\n".join(notes) +
    "\n\n## Field names for the team (fill in after reading)\n- response field: ___\n- judge field: ___\n- score field: ___\n\n## Judge red-flag result\n___ / 30 looked wrong\n\n## Observations\n___\n")
print(f"\nDone. See {A.out}/data_notes_DRAFT.md")
