#!/usr/bin/env python3
"""SentryRoute Phase 1, Stage 3: frozen splits. Train / calibration / threshold / test plus the duplicate report.

Run from the repo root:  python Complexity/difficulty/scripts/stage3_splits.py
Reads:  Complexity/difficulty/labels/labels_v1.csv (Stage 2) and SPROUT prompt text (Hugging Face, or --local)
Writes: Complexity/difficulty/splits/split_v1.csv (refuses to overwrite: a new version needs a new name, see --split-out)
        Complexity/difficulty/notes/stage3/*.csv, near_dup_pairs_to_read.md and stage3_notes_DRAFT.md
Rules (plan Stage 3, pre-registered seed 42):
  train = SPROUT train, test = SPROUT test (never altered)
  SPROUT validation -> calibration / threshold halves, stratified on source x easy_ext; cells under 2 prompts -> "other"
  duplicates across parts: exact (normalised full-text hash), same (dataset, dataset_idx), MinHash on word 5-grams >= 0.9
  a train prompt duplicating any other part leaves train; a calibration/threshold prompt duplicating test leaves its half
Removed prompts are left out of split_v1.csv (split values stay train / calibration / threshold / test) and listed in
notes/stage3/removed.csv. Stratification uses easy_ext only, so a later switch of the local pair does not change this split."""
import argparse, hashlib, os, re, sys
import numpy as np, pandas as pd
from datasketch import MinHash, MinHashLSH

ap = argparse.ArgumentParser()
ap.add_argument("--labels", default="Complexity/difficulty/labels/labels_v1.csv")
ap.add_argument("--split-out", default="Complexity/difficulty/splits/split_v1.csv")
ap.add_argument("--notes-dir", default="Complexity/difficulty/notes/stage3")
ap.add_argument("--seed", type=int, default=42, help="pre-registered 42; only change for a documented reason")
ap.add_argument("--near-threshold", type=float, default=0.9)
ap.add_argument("--num-perm", type=int, default=128)
ap.add_argument("--local", help="DIR with train/validation/test.jsonl instead of Hugging Face (testing)")
A = ap.parse_args()
if os.path.exists(A.split_out):
    sys.exit(f"{A.split_out} already exists. Never overwrite a shared file: pick a new name with --split-out (e.g. split_v2.csv).")
os.makedirs(A.notes_dir, exist_ok=True); os.makedirs(os.path.dirname(A.split_out) or ".", exist_ok=True)
out = []
def say(s=""): print(s); out.append(s)

# ---------- load ----------
L = pd.read_csv(A.labels, dtype={"easy_ext": str, "easy_loc": str})
if A.local: splits = {s: pd.read_json(f"{A.local}/{s}.jsonl", lines=True) for s in ["train", "validation", "test"]}
else:
    from datasets import load_dataset
    splits = {k: v.to_pandas() for k, v in load_dataset("CARROT-LLM-Routing/SPROUT").items()}
P = pd.concat([v[["key", "dataset_idx", "prompt"]] for v in splits.values()], ignore_index=True).rename(columns={"key": "prompt_id"})
D = L.merge(P, on="prompt_id", how="left", validate="1:1")
assert D["prompt"].notna().all(), "labels file has prompt_ids that are not in SPROUT"
assert len(D) == len(P), "labels file and SPROUT have different row counts"
D["prompt"] = D["prompt"].astype(str)

# ---------- 1-2. parts ----------
D["split"] = D["sprout_split"].map({"train": "train", "test": "test", "validation": "val"})
V = D[D.split == "val"].copy()
V["stratum"] = V["dataset"] + " | " + V["easy_ext"]
small = V["stratum"].map(V["stratum"].value_counts()) < 2
V.loc[small, "stratum"] = "other"
rng = np.random.default_rng(A.seed)
flip = 0  # carried across strata so odd-sized strata don't all give their extra prompt to the same half
for _, idx in V.groupby("stratum", sort=True).groups.items():
    idx = rng.permutation(np.asarray(idx))
    first, second = ("calibration", "threshold") if flip == 0 else ("threshold", "calibration")
    V.loc[idx[0::2], "split"] = first; V.loc[idx[1::2], "split"] = second
    flip ^= len(idx) % 2
D.loc[V.index, "split"] = V["split"]
PARTS = ["train", "calibration", "threshold", "test"]
assert set(D.split) == set(PARTS)

say("# Stage 3: splits (auto-generated draft)")
say(f"\nSeed {A.seed}. Validation strata: {V['stratum'].nunique()} (source x easy_ext); "
    f"{int(small.sum())} prompts from cells under 2 went to the shared 'other' stratum.")
if A.seed != 42: say("**WARNING: seed differs from the pre-registered 42.**")
src_halves = V.groupby("dataset")["split"].agg(lambda s: set(s) >= {"calibration", "threshold"})
missing_src = sorted(src_halves[~src_halves].index)
say(f"Sources in both validation halves: {int(src_halves.sum())} of {len(src_halves)}"
    + (f". Missing from one half: {missing_src}" if missing_src else "."))

# ---------- 3. duplicates ----------
norm = D["prompt"].str.lower().map(lambda t: re.sub(r"\s+", " ", t).strip())
D["hash"] = norm.map(lambda t: hashlib.sha256(t.encode()).hexdigest())
pairs = []  # (row_a, row_b, kind), only across different parts

def cross_pairs(key, kind):
    for _, g in D.groupby(key, sort=False):
        if len(g) < 2 or g["split"].nunique() < 2: continue
        ix = g.index.to_numpy()
        for i in range(len(ix)):
            for j in range(i + 1, len(ix)):
                if D.at[ix[i], "split"] != D.at[ix[j], "split"]: pairs.append((ix[i], ix[j], kind))
cross_pairs("hash", "exact")
D["item"] = D["dataset"] + "#" + D["dataset_idx"].astype(str)
cross_pairs("item", "same_item")
within = D.duplicated("hash", keep=False) & ~D.groupby("hash")["split"].transform("nunique").gt(1)

# MinHash LSH on word 5-grams; prompts under 5 words become one shingle (the exact hash already covers them)
lsh = MinHashLSH(threshold=A.near_threshold, num_perm=A.num_perm)
mh = {}
for i, t in norm.items():
    w = t.split()
    sh = {" ".join(w[k:k + 5]) for k in range(len(w) - 4)} or {t}
    m = MinHash(num_perm=A.num_perm, seed=1); m.update_batch([s.encode() for s in sh])
    mh[i] = m; lsh.insert(i, m)
seen = set()
for i, m in mh.items():
    for j in lsh.query(m):
        if j <= i or D.at[i, "split"] == D.at[j, "split"] or D.at[i, "hash"] == D.at[j, "hash"]: continue
        if (i, j) in seen: continue
        seen.add((i, j)); sim = m.jaccard(mh[j])
        if sim >= A.near_threshold: pairs.append((i, j, f"near_{sim:.2f}"))

PR = pd.DataFrame(pairs, columns=["a", "b", "kind"])
for s in ("a", "b"):
    PR[f"{s}_id"] = D.loc[PR[s], "prompt_id"].to_numpy(); PR[f"{s}_split"] = D.loc[PR[s], "split"].to_numpy()
    PR[f"{s}_source"] = D.loc[PR[s], "dataset"].to_numpy()
PR["kind_group"] = PR["kind"].str.replace(r"_\d\.\d+$", "", regex=True)

# who leaves: test never; train loses to anything; calibration/threshold lose only to test.
# calibration vs threshold duplicates are reported, not removed (the plan has no rule; both are validation halves).
def loser(sa, sb):
    if "test" in (sa, sb): other = sb if sa == "test" else sa; return None if other == "test" else other
    if "train" in (sa, sb): return "train"
    return None
remove = {}
for r in PR.itertuples():
    lose = loser(r.a_split, r.b_split)
    if lose is None: continue
    row = r.a if r.a_split == lose else r.b
    remove.setdefault(row, r.kind_group)

say("\n## 1. Duplicate pairs across parts")
say(f"Exact (normalised full-text hash), same (dataset, dataset_idx) and MinHash >= {A.near_threshold} on word 5-grams "
    f"({A.num_perm} permutations).")
if len(PR):
    order = {p: k for k, p in enumerate(PARTS)}
    parts = [" / ".join(sorted(t, key=order.get)) for t in zip(PR.a_split, PR.b_split)]
    tab = PR.assign(parts=parts).pivot_table(index="parts", columns="kind_group", values="a",
                                                                         aggfunc="count", fill_value=0)
    say(tab.to_markdown())
else: say("No duplicate pairs across parts.")
say(f"\nExact duplicates inside a single part (kept, not a leak): {int(within.sum())} prompts")
cv = PR[(PR.a_split.isin(["calibration", "threshold"])) & (PR.b_split.isin(["calibration", "threshold"]))]
say(f"Calibration vs threshold pairs (reported, not removed): {len(cv)}")
PR.drop(columns=["a", "b"]).to_csv(f"{A.notes_dir}/duplicate_pairs.csv", index=False)

# 20 near-duplicate pairs to read by hand (plan step 3), spread over sources
near = PR[PR.kind_group == "near"]
smp = near[near.groupby("a_source").cumcount() < 3].head(20)
if len(smp) < 20 and len(near) > len(smp): smp = pd.concat([smp, near.drop(smp.index).head(20 - len(smp))])
md = [f"# Near-duplicate pairs to read (Stage 3 step 3)\n\n{len(near)} flagged pairs; {len(smp)} shown. "
      "For each, write `real duplicate` or `not a duplicate` under the verdict line. Record the count in the Stage 3 notes.\n"]
for k, r in enumerate(smp.itertuples(), 1):
    clip = lambda t: (t[:1500] + " [...]") if len(t) > 1500 else t
    md += [f"## Pair {k}: {r.kind} ({r.a_split}, {r.a_source}) vs ({r.b_split}, {r.b_source})\n",
           f"**A** `{r.a_id[:12]}`\n\n```\n{clip(D.at[r.a, 'prompt'])}\n```\n",
           f"**B** `{r.b_id[:12]}`\n\n```\n{clip(D.at[r.b, 'prompt'])}\n```\n", "Verdict: \n"]
open(f"{A.notes_dir}/near_dup_pairs_to_read.md", "w").write("\n".join(md))

# ---------- removal ----------
R = D.loc[list(remove)].assign(reason=[remove[i] for i in remove])[["prompt_id", "dataset", "split", "reason"]]
R.to_csv(f"{A.notes_dir}/removed.csv", index=False)
say("\n## 2. Removed prompts (test is never altered)")
if len(R): say(R.groupby(["split", "dataset", "reason"]).size().rename("removed").reset_index().to_markdown(index=False))
else: say("None.")
F = D.drop(index=list(remove))

# ---------- sizes ----------
say("\n## 3. Final parts")
rows = []
for p in PARTS:
    s = F[F.split == p]
    rows.append(dict(split=p, n=len(s), removed=int((R.split == p).sum()),
                     ext_easy=int((s.easy_ext == "1").sum()), ext_hard=int((s.easy_ext == "0").sum()),
                     ext_infeasible=int((s.easy_ext == "infeasible").sum()),
                     ext_hard_pct_of_labelled=round(100 * (s.easy_ext == "0").sum() / max(1, s.easy_ext.isin(["1", "0"]).sum()), 1),
                     loc_hard_pct_of_labelled=round(100 * (s.easy_loc == "0").sum() / max(1, s.easy_loc.isin(["1", "0"]).sum()), 1)))
sz = pd.DataFrame(rows); sz.to_csv(f"{A.notes_dir}/split_sizes.csv", index=False); say(sz.to_markdown(index=False))
bysrc = pd.crosstab(F["dataset"], F["split"])[PARTS]; bysrc.to_csv(f"{A.notes_dir}/split_by_source.csv")
say("\n### By source"); say(bysrc.to_markdown())
tr = F[F.split == "train"]; e, h = (tr.easy_ext == "1").sum(), (tr.easy_ext == "0").sum()
say(f"\nExternal class weight from the final train part: easy/hard = {e:,} / {h:,} = {e / h:.2f} "
    "(Stage 2 pre-registered 10.56 from train before duplicate removal; record the difference if it moved).")

# ---------- self-check ----------
test_ids = set(D.loc[D.sprout_split == "test", "prompt_id"])
assert set(F.loc[F.split == "test", "prompt_id"]) == test_ids, "test part was altered"
assert F["prompt_id"].is_unique
for i, j, _ in pairs:  # no surviving cross-part duplicate except the reported calibration/threshold ones
    if i in F.index and j in F.index: assert {D.at[i, "split"], D.at[j, "split"]} <= {"calibration", "threshold"}

# ---------- write ----------
F[["prompt_id", "split"]].to_csv(A.split_out, index=False)
chk = pd.read_csv(A.split_out)
assert len(chk) == len(F) and set(chk.split) == set(PARTS)
say(f"\nWrote {A.split_out} ({len(chk):,} rows; {len(R):,} removed duplicates left out, listed in {A.notes_dir}/removed.csv).")
say("From now on nobody computes anything on the test part until Stage 6.")
open(f"{A.notes_dir}/stage3_notes_DRAFT.md", "w").write("\n".join(out) + "\n")
print(f"\nDone. See {A.notes_dir}/stage3_notes_DRAFT.md and read {A.notes_dir}/near_dup_pairs_to_read.md")
