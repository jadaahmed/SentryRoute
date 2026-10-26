# Gateway contract decisions (complexity service)

Owner: Sameh. Record each answer with date and who answered. Until answered, Phase 1 follows the rules in `preregistration.md`.
Status "not sent" means nobody has recorded sending it yet; update when sent.

| # | Question for the contract author | Our assumption until answered | Status | Answer / date |
|---|---|---|---|---|
| 1 | May we add an optional `pools: {external: {tier, score}, local: {tier, score}}` next to the top-level fields in `openapi.yaml`? | Gateway sees the more complex of the two pools as top-level `tier` and `score` | **answered** | Yes, 26 Oct 2026 (Karim). Top-level stays as the more complex pool; `GET /v1/info` lists `pools`; router reads `pools[locality]`. Contract v2 doc, and the schema is in `api/openapi.yaml` / `api/classifier.openapi.yaml` (draft, Karim to confirm); Zeina/Sameh return `pools` and update the mock |
| 2 | Is `simple` -> cheap model, `moderate` and `complex` -> strong model the right mapping (lives in the policy)? | Yes | not sent | |
| 3 | Is `score` higher = more complex? | Yes (score = 1 - p) | **answered** | Yes, written into contract v2 (26 Oct 2026) |
| 4 | Will pools have more than two models? | Phase 1 models cheap vs strong only | not sent | |
| 5 | Which GPUs and how much VRAM do the two laptops have? | Unknown; may force the 3B -> 8B local stand-in pair | not sent | |
| 6 | Which CPU should the latency target be measured on? | Report CPU model and thread count with the numbers | not sent | |

SPROUT license: **resolved 26 Oct 2026** (see `Complexity/data/README.md`).
