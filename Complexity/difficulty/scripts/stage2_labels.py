#!/usr/bin/env python3
"""SentryRoute Phase 1, Stage 2: labels. Turns SPROUT's stored judge scores into easy / hard / infeasible labels per pool.

Run from the repo root (or any folder):  python Complexity/difficulty/scripts/stage2_labels.py
Writes: Complexity/difficulty/labels/labels_v1.csv (refuses to overwrite: a new version needs a new name, see --labels-out)
        Complexity/difficulty/notes/stage2/*.csv and stage2_notes_DRAFT.md
Rule (pre-registered, Complexity/difficulty/notes/preregistration.md): cutoff 0.5.
  cheap >= cutoff                      -> easy        (label 1)
  cheap <  cutoff and strong >= cutoff -> hard        (label 0)
  both  <  cutoff                      -> infeasible
Uses the same SPROUT field names found in Stage 1: cell dict with key `score`."""
import argparse, json, ast, os, sys
import numpy as np, pandas as pd

M_EXT_CHEAP, M_EXT_STRONG = "openai-gpt-4o-mini", "openai-gpt-4o"
M_LOC_CHEAP, M_LOC_STRONG = "wxai-llama-3-1-8b-instruct", "wxai-llama-3-3-70b-instruct"

ap = argparse.ArgumentParser()
ap.add_argument("--labels-out", default="Complexity/difficulty/labels/labels_v1.csv")
ap.add_argument("--notes-dir", default="Complexity/difficulty/notes/stage2")
ap.add_argument("--cutoff", type=float, default=0.5, help="pre-registered 0.5; only change for a documented reason")
ap.add_argument("--local-cheap", default=M_LOC_CHEAP); ap.add_argument("--local-strong", default=M_LOC_STRONG)
ap.add_argument("--score-field", default="score")
ap.add_argument("--local", help="DIR with train/validation/test.jsonl instead of Hugging Face (testing)")
A = ap.parse_args()
if os.path.exists(A.labels_out):
    sys.exit(f"{A.labels_out} already exists. Never overwrite a shared file: pick a new name with --labels-out (e.g. labels_v2.csv).")
os.makedirs(A.notes_dir, exist_ok=True); os.makedirs(os.path.dirname(A.labels_out) or ".", exist_ok=True)
out = []
def say(s=""): print(s); out.append(s)

# ---------- load ----------
if A.local: splits = {s: pd.read_json(f"{A.local}/{s}.jsonl", lines=True) for s in ["train", "validation", "test"]}
else:
    from datasets import load_dataset
    splits = {k: v.to_pandas() for k, v in load_dataset("CARROT-LLM-Routing/SPROUT").items()}
def as_obj(x):
    if isinstance(x, (dict, list)) or x is None: return x
    for f in (json.loads, ast.literal_eval):
        try: return f(x)
        except Exception: pass
    return x
def get_score(x):
    o = as_obj(x); v = o.get(A.score_field) if isinstance(o, dict) else o
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else np.nan
models = [M_EXT_CHEAP, M_EXT_STRONG, A.local_cheap, A.local_strong]
D = pd.concat([v.assign(sprout_split=k) for k, v in splits.items()], ignore_index=True)
for m in models:
    if m not in D: sys.exit(f"model column missing: {m}")
S = pd.DataFrame({"prompt_id": D["key"], "dataset": D["dataset"], "dataset_level": D["dataset_level"],
                  "sprout_split": D["sprout_split"]})
for name, m in [("gpt4o_mini", M_EXT_CHEAP), ("gpt4o", M_EXT_STRONG), ("llama_cheap", A.local_cheap), ("llama_strong", A.local_strong)]:
    S[f"score_{name}"] = D[m].map(get_score)

def label(cheap, strong, cutoff):
    """1 = easy, 0 = hard, 'infeasible', 'missing' if a score is absent."""
    lab = np.where(cheap >= cutoff, "1", np.where(strong >= cutoff, "0", "infeasible")).astype(object)
    lab[np.isnan(cheap) | np.isnan(strong)] = "missing"
    return pd.Series(lab, index=cheap.index)
def pool_labels(cutoff):
    return (label(S["score_gpt4o_mini"], S["score_gpt4o"], cutoff), label(S["score_llama_cheap"], S["score_llama_strong"], cutoff))
S["easy_ext"], S["easy_loc"] = pool_labels(A.cutoff)

say("# Stage 2: labels (auto-generated draft)")
say(f"\nRule: cutoff {A.cutoff}. External pair {M_EXT_CHEAP} -> {M_EXT_STRONG}. Local pair {A.local_cheap} -> {A.local_strong} "
    f"(stand-in; the laptop-VRAM check from Stage 0 is still open).")
if A.cutoff != 0.5: say("**WARNING: cutoff differs from the pre-registered 0.5.**")
say(f"\nRows: {len(S):,}; prompt_id unique: {S['prompt_id'].is_unique}; rows with a missing score: "
    f"{int((S[['easy_ext','easy_loc']] == 'missing').any(axis=1).sum())}")

# ---------- sanity ----------
valid = {"1", "0", "infeasible", "missing"}
assert set(S["easy_ext"]) <= valid and set(S["easy_loc"]) <= valid
assert S["prompt_id"].is_unique, "prompt_id (SPROUT key) is not unique"

# ---------- 2. counts ----------
def counts(group=None):
    rows = []
    for pool, col in [("external", "easy_ext"), ("local", "easy_loc")]:
        g = S.groupby(group)[col] if group else [("ALL", S[col])]
        for k, s in g:
            n = len(s); vc = s.value_counts()
            rows.append(dict(pool=pool, group=k, n=n, easy=int(vc.get("1", 0)), hard=int(vc.get("0", 0)), infeasible=int(vc.get("infeasible", 0)),
                             easy_pct=round(100 * vc.get("1", 0) / n, 1), hard_pct=round(100 * vc.get("0", 0) / n, 1),
                             infeasible_pct=round(100 * vc.get("infeasible", 0) / n, 1)))
    return pd.DataFrame(rows)
say("\n## 1. Counts per pool (all rows)"); c_all = counts(); say(c_all.drop(columns="group").to_markdown(index=False))
c_split = counts("sprout_split"); c_src = counts("dataset")
c_split.to_csv(f"{A.notes_dir}/counts_by_sprout_split.csv", index=False); c_src.to_csv(f"{A.notes_dir}/counts_by_source.csv", index=False)
say("\n### By SPROUT split"); say(c_split.to_markdown(index=False))
say("\n### By source (external pool; local pool is in counts_by_source.csv)")
say(c_src[c_src.pool == "external"].sort_values("n", ascending=False).drop(columns="pool").to_markdown(index=False))
say("\n### Local pool by source"); say(c_src[c_src.pool == "local"].sort_values("n", ascending=False).drop(columns="pool").to_markdown(index=False))

# share of prompts whose label could change: cheap or strong score within 0.1 of the cutoff
def near(col): return (np.round((S[col] - A.cutoff).abs(), 6) < 0.1)
near_ext = near("score_gpt4o_mini") | near("score_gpt4o"); near_loc = near("score_llama_cheap") | near("score_llama_strong")
say(f"\nShare of prompts with the cheap or strong score within 0.1 of the cutoff: external {100*near_ext.mean():.2f}%, local {100*near_loc.mean():.2f}%")

# ---------- 3. cutoff sensitivity ----------
say("\n## 2. Rule sensitivity (cutoffs 0.4 and 0.6 vs the chosen cutoff)")
rows = []
for cut in (0.4, 0.6):
    e2, l2 = pool_labels(cut)
    for pool, old, new in [("external", S["easy_ext"], e2), ("local", S["easy_loc"], l2)]:
        ch = old != new
        rows.append(dict(cutoff=cut, pool=pool, labels_changed=int(ch.sum()), pct_of_all=round(100 * ch.mean(), 2),
                         easy_pct=round(100 * (new == "1").mean(), 1), hard_pct=round(100 * (new == "0").mean(), 1),
                         infeasible_pct=round(100 * (new == "infeasible").mean(), 1)))
sens = pd.DataFrame(rows); sens.to_csv(f"{A.notes_dir}/cutoff_sensitivity.csv", index=False); say(sens.to_markdown(index=False))
say("If many labels change, list it as a limitation in the report.")

# ---------- 4. balance ----------
say("\n## 3. Balance check (labelled prompts only: easy + hard)")
bal = []
for pool, col in [("external", "easy_ext"), ("local", "easy_loc")]:
    s = S[col]; e, h, inf = (s == "1").sum(), (s == "0").sum(), (s == "infeasible").sum()
    hp = 100 * h / (e + h)
    bal.append(dict(pool=pool, easy=int(e), hard=int(h), hard_pct_of_labelled=round(hp, 1), infeasible_pct_of_all=round(100 * inf / len(s), 1),
                    needs_class_weights=bool(hp < 15), suggested_weight_on_hard_class=round(e / h, 2),
                    flag_backup_pair=bool(inf / len(s) > 0.40)))
bal = pd.DataFrame(bal); bal.to_csv(f"{A.notes_dir}/balance_check.csv", index=False); say(bal.to_markdown(index=False))
say("Plan: hard under about 15% of labelled prompts -> class weights (preferred) or the tolerance idea. "
    "Infeasible over about 40% -> switch to the backup local pair BEFORE any training. Record the decision in notes/preregistration.md.")

# ---------- 5/6. infeasible + overlap ----------
say("\n## 4. Overlap between pools (rows = external label, columns = local label)")
ov = pd.crosstab(S["easy_ext"].map({"1": "easy", "0": "hard", "infeasible": "infeasible", "missing": "missing"}),
                 S["easy_loc"].map({"1": "easy", "0": "hard", "infeasible": "infeasible", "missing": "missing"}), margins=True)
ov.to_csv(f"{A.notes_dir}/pool_overlap.csv"); say(ov.to_markdown())
mixed = ((S.easy_ext == "infeasible") & S.easy_loc.isin(["1", "0"])).sum() + ((S.easy_loc == "infeasible") & S.easy_ext.isin(["1", "0"])).sum()
say(f"\nPrompts infeasible in one pool but easy/hard in the other: {int(mixed)} ({100*mixed/len(S):.1f}% of all)")
dis = ((S.easy_ext.isin(["1", "0"])) & (S.easy_loc.isin(["1", "0"])) & (S.easy_ext != S.easy_loc))
say(f"Prompts labelled in both pools where the two labels differ (easy in one, hard in the other): {int(dis.sum())} ({100*dis.mean():.1f}% of all)")

# ---------- write ----------
cols = ["prompt_id", "dataset", "dataset_level", "easy_ext", "easy_loc", "score_gpt4o_mini", "score_gpt4o", "score_llama_cheap", "score_llama_strong", "sprout_split"]
S[cols].rename(columns={"score_llama_cheap": "score_llama8b", "score_llama_strong": "score_llama70b"}).to_csv(A.labels_out, index=False)
chk = pd.read_csv(A.labels_out, dtype={"easy_ext": str, "easy_loc": str})
assert len(chk) == len(S) and chk["prompt_id"].is_unique
say(f"\nWrote {A.labels_out} ({len(chk):,} rows). Columns follow the agreed labels format plus a trailing `sprout_split` (needed by Stage 3).")
open(f"{A.notes_dir}/stage2_notes_DRAFT.md", "w").write("\n".join(out) + "\n")
print(f"\nDone. See {A.notes_dir}/stage2_notes_DRAFT.md")
