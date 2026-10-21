# Gateway contract decisions (complexity service)

Owner: Sameh. Record each answer with date and who answered. Until answered, Phase 1 follows the rules in `preregistration.md`.
Status "not sent" means nobody has recorded sending it yet; update when sent.

| # | Question for the contract author | Our assumption until answered | Status | Answer / date |
|---|---|---|---|---|
| 1 | May we add an optional `pools: {external: {tier, score}, local: {tier, score}}` next to the top-level fields in `openapi.yaml`? | Gateway sees the more complex of the two pools as top-level `tier` and `score` | not sent | |
| 2 | Is `simple` -> cheap model, `moderate` and `complex` -> strong model the right mapping (lives in the policy)? | Yes | not sent | |
| 3 | Is `score` higher = more complex? | Yes (score = 1 - p) | not sent | |
| 4 | Will pools have more than two models? | Phase 1 models cheap vs strong only | not sent | |
| 5 | Which GPUs and how much VRAM do the two laptops have? | Unknown; may force the 3B -> 8B local stand-in pair | not sent | |
| 6 | Which CPU should the latency target be measured on? | Report CPU model and thread count with the numbers | not sent | |

Also open from the SPROUT side: **license.** SPROUT's Hugging Face page shows no license. Question for Prof. Khalil: "Can we use it for research and report results on it?" Status: not sent.
