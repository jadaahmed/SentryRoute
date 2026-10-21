# SentryRoute

Sensitivity- and difficulty-aware LLM routing for regulated enterprises. Graduation project, Computer & AI Engineering, Ain Shams University (dual degree with University of East London).

- **Sponsor:** CloudzLab (official Salesforce partner)
- **Supervisor:** Prof. Mahmoud Khalil
- **Team (8):** Karim Marwan, Yousef Waleed, Mohamed Sameh, Adam Heshmat, Zeina Reda, Joumana Elsewefie, Hana Salah, Jada Ahmed
- **Runs:** late Sep 2026 to end of June 2027

## Sources of truth

1. **`api/openapi.yaml`** is the machine-readable gateway contract. If anything here disagrees with it, the spec wins. Change the spec first, then the code, then regenerate the TypeScript client. CI runs a spec-drift check.
2. **This file** holds decisions, rules and context.
3. **Design docs:** Tech Stack & Gateway API Contract (Oct 21, 2026), Graduation Project Proposal, Timeline & Sponsor Support Requirements (Sep 28, 2026).

---

## The problem

- **Cost.** Every request goes to the most capable model, including the many that never needed it (summaries, rewrites, classification, short factual questions). Budget vs. frontier models differ by roughly 100× per token.
- **Compliance.** Banks, insurers and telecoms can't send customer records, national IDs or internal financials to foreign-hosted APIs. Today it's all-or-nothing: block LLMs for whole departments, or self-host one local model and accept weaker quality on every task.
- **Gap.** Routers (RouteLLM, OpenRouter, Portkey, LiteLLM, cloud managed routers) route on difficulty/cost and treat every prompt as safe to send anywhere. Data-protection gateways filter or redact but make no cost decision.

## What SentryRoute does

A routing layer between an organisation's apps and its model pool. Every prompt is scored on two **independent** axes before dispatch:

- **Sensitivity** decides *where* a prompt may go.
- **Complexity / difficulty** decides *how much model* it needs once it gets there.

A policy matrix, configured by a compliance officer (not hard-coded by an engineer), turns the two scores into a route:

|                   | Easy task                    | Hard task                     |
|-------------------|------------------------------|-------------------------------|
| **Not sensitive** | Cheap external API model     | Frontier external API model   |
| **Sensitive**     | Small local open-weight model | Large local open-weight model |

Sensitive prompts never leave the organisation's network. Every prompt is served by the smallest model that can handle it within its allowed locality. Compliance and cost are co-equal: each axis has its own component, threshold and metrics, so each half's contribution is measured separately.

### Related work

- **ComplianceGate** (arXiv 2026): one encoder assigns 6 joint labels (3 complexity × 2 sensitivity); 600 queries. *Closest prior work.* Its joint design is one of our evaluation baselines.
- **PRISM** (AAAI 2026): edge/cloud routing for personal devices, perturbs prompts with local differential privacy.
- **How we differ:** two separate components with their own thresholds and metrics, a deterministic identifier layer, a compliance-officer policy matrix, an enterprise model pool where sensitive prompts never go out at all, and evaluation against RouteLLM on large public benchmarks.
- RouteLLM, RouterBench and LLMRouterBench are used as **baselines and training data**, not competitors.

---

## Gateway requirements

These six drive every design choice:

1. **Drop-in for existing apps.** Accepts OpenAI Chat Completions requests unchanged, streaming included.
2. **Two checks per request, little added latency.** Sensitivity and complexity run **in parallel** before any model is called.
3. **Sensitive prompts never leave.** They go to a local model or get blocked, never to an external API. The gateway fails closed.
4. **Every decision is auditable without storing prompts.** Each request leaves a decision record with labels and costs, no raw text.
5. **Eight people working in parallel.** Clean seams between gateway, both classifiers and the UI.
6. **Runs on what we have.** No sponsor GPU server, so local models run on two team laptops. Storage is MongoDB Atlas on student credits. Everything ships as containers.

**Out of scope for v1:** image and audio inputs. Reject them with `400 unsupported_content`, never pass them through unscanned.

## Tech stack

Python for the gateway, both classifiers and eval code. TypeScript only for the web UI.

| Part | Pick | Notes |
|---|---|---|
| Gateway | Python 3.12, FastAPI, Uvicorn, Pydantic v2 | Async I/O for streaming; request models double as validation. (Considered: Go, Node/Express) |
| Provider calls | Own thin adapter on `httpx`: one OpenAI-compatible client + one adapter per non-compatible provider | We need a handful of providers, not 100. No LiteLLM in the gateway (see Supply chain) |
| Sensitivity classifier | Layered detector: L1 regex + dictionaries, L2 pre-trained NER, L3 fine-tuned multi-label classifier (mmBERT), L4 small LLM judge for unsure prompts. See **Sensitivity detection** | The Oct 21 doc listed Presidio + one encoder; this layered design is the current one |
| Complexity classifier | Fine-tuned small encoder → tier + score | Cheap on CPU, trained on our labels. RouteLLM as-is only handles strong-vs-weak, so it's the baseline to beat |
| Classifier serving | Each classifier is its own FastAPI service. PyTorch first, ONNX Runtime on CPU once latency matters | Sub-teams ship independently and can swap/A-B models. In-process serving is a later optimization |
| Local LLMs | Ollama on 2 team laptops turned GPU boxes (Ubuntu + NVIDIA driver), reachable **only** over a private Tailscale network. Small 4-bit quantized models sized to VRAM | Ollama speaks the OpenAI API, so "local" is just another provider. Two boxes = failover for sensitive traffic. vLLM needs compute capability 7.0+ and more VRAM |
| Storage | MongoDB Atlas (GitHub Student Pack) for decisions, policies and API keys, via **PyMongo's async API**. Redis for rate limits | Decision records are JSON docs; aggregation pipelines cover savings stats. **Motor is deprecated, don't use it.** (Switched from PostgreSQL for the credits) |
| Web UI | React + TypeScript + Vite + Tailwind; typed client generated from `openapi.yaml` | Playground, policy admin, maybe audit views. No Next.js |
| Audit dashboard | **Open:** Salesforce or a page in our web UI | Both read `GET /v1/decisions`, so this doesn't block the gateway |
| Observability | OpenTelemetry traces, Prometheus metrics, Grafana | Per-stage latency is a thesis result; measure from week one. (Considered: Langfuse) |
| Build & CI | Docker Compose; GitHub Actions running ruff, mypy, pytest and a spec-drift check; `uv` lockfile with hashes | Same stack on every laptop and the demo server |

### Supply chain

On 24 Mar 2026, LiteLLM 1.82.7 and 1.82.8 were published to PyPI with a payload that dumped env vars, cloud keys and secrets to an attacker. A router holds every provider key and sees every sensitive prompt, so:

- Keep the gateway's dependency list short. **Ask before adding any dependency.**
- Every package is pinned by hash (uv lock). CI tools are pinned by version.
- **No LiteLLM in the gateway image.** RouteLLM depends on LiteLLM, so it lives **only in the eval environment**.
- LiteLLM SDK (pinned with hashes) is only reconsidered if the provider list grows a lot.

---

## Architecture and request flow

```
Client app (OpenAI SDK, base_url → gateway)
   │
   ▼
┌──────────────── Gateway · Python + FastAPI ────────────────┐
│  Auth + rate limit (API key → tenant + policy)             │
│        │                                │   (in parallel)  │
│        ▼                                ▼                  │
│  Sensitivity service             Complexity service        │
│  L1 → L2‖L3 → aggregator → (L4)  small encoder             │
│  label + score, fails closed     tier + score + signals    │
│        └──────────────┬─────────────────┘                  │
│                       ▼                                    │
│  Policy router: cheapest model both checks allow           │
└────────┬───────────────────────────────┬───────────────────┘
 sensitive│                               │not sensitive
         ▼                               ▼
 Local model (Ollama)            External API model
 2 team laptops                  cheapest model for the tier
         │
         ▼  every decision is logged
 Decision log (MongoDB): labels, model, cost; never raw prompt text
         ▼
 Audit dashboard + web UI (reads GET /v1/decisions)
```

The router keeps the **strictest** sensitivity result, picks the cheapest model that fits the tier, and returns the answer with routing metadata attached. The routing engine also owns policy evaluation, model pool management, and ordered fallback/failover, which **always stays within the same locality**.

---

## Public gateway API

OpenAI Chat Completions unchanged, plus SentryRoute-only endpoints. All paths are under `/v1`.

### What `model` means

- **`sentryroute/auto`**: both checks run and the router picks. This is the default we tell apps to use.
- **`sentryroute/local`**: forces the local pool. Sensitivity still runs, for the audit log.
- **A concrete backend model id** (from `GET /v1/models`): the client pins it. Sensitivity still runs. If the request is sensitive and the pinned model is external, the policy reroutes to local (default) or blocks.

### Endpoints

| Method | Path | Called by | What it does | Scope |
|---|---|---|---|---|
| POST | `/v1/chat/completions` | Client apps | OpenAI-compatible chat, streaming or not; routes when `model` is `sentryroute/auto` | `chat` |
| POST | `/v1/route` | Eval harness, UI playground | Runs both classifiers + router, returns the decision, calls no model | `chat` |
| GET | `/v1/models` | Client apps, UI | `sentryroute/auto`, `sentryroute/local` and every backend model with locality, tier, price | `chat` |
| GET | `/v1/decisions` | Audit dashboard, UI | Decision records filtered by time, label, locality, model or tag; cursor paging | `audit:read` |
| GET | `/v1/decisions/{decision_id}` | Audit dashboard, UI | One decision record | `audit:read` |
| GET | `/v1/stats/savings` | Audit dashboard | Actual cost vs baseline-model cost, bucketed by day or week | `audit:read` |
| GET, PUT | `/v1/policies/{policy_id}` | Admins via UI | Read or replace a routing policy (`PUT` needs `If-Match`) | `admin` |
| GET | `/healthz`, `/readyz` | Docker, load balancer | Liveness; readiness also checks classifiers and the database | none |

### Request extension

Apps send an optional `sentryroute` object next to the normal fields (in `extra_body` with the OpenAI Python SDK):

| Field | Type | Meaning |
|---|---|---|
| `policy_id` | string | Which policy to apply; defaults to the API key's policy |
| `max_cost_usd` | number | Router skips models whose estimated cost is above this |
| `min_tier` | `simple` / `moderate` / `complex` | Floor on the complexity tier when the app knows the task is hard |
| `tags` | map of strings, max 10 | Stored on the decision record so the dashboard can filter by app or feature |

Everything else (`temperature`, `max_tokens`, `tools`, `response_format`, `stream`, `stream_options`) passes through to the chosen model untouched.

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8080/v1", api_key="sr_...")
resp = client.chat.completions.create(
    model="sentryroute/auto",
    messages=[{"role": "user", "content": "Summarise this clause for the sales team: ..."}],
    extra_body={"sentryroute": {"max_cost_usd": 0.02, "tags": {"app": "crm-assistant"}}},
)
resp.model                        # the model that actually answered
resp.model_extra["sentryroute"]   # routing metadata
```

### Routing metadata in every response

Sent twice. Headers are readable before a stream starts, and a `sentryroute` object goes in the body. OpenAI SDKs ignore unknown fields, so apps that don't care see nothing new.

- **Headers:** `X-SentryRoute-Decision-Id`, `X-SentryRoute-Model`, `X-SentryRoute-Locality` (`local` | `external`), `X-SentryRoute-Sensitivity` (the label)
- **Body `sentryroute`:** `decision_id`, `route {model, provider, locality, reason_codes}`, `sensitivity {label, score, categories, degraded}`, `complexity {tier, score, degraded}`, `cost {actual_usd, baseline_usd}`, `overhead_ms`

### Sensitivity labels

| Label | Meaning | Default policy |
|---|---|---|
| `public` | Nothing sensitive found | Any model |
| `internal` | Company-internal, not regulated | Any model (policy can tighten) |
| `confidential` | PII or business secrets | Local only |
| `restricted` | Credentials, card or ID numbers, **or the classifier failed** | Local only; policy can block |

Complexity tiers: `simple`, `moderate`, `complex`.

### Reason codes

`CHEAPEST_FOR_TIER`, `SENSITIVE_LOCAL_ONLY`, `CLASSIFIER_FAILED_CLOSED`, `PINNED_BY_CLIENT`, `PINNED_REROUTED_SENSITIVE`, `BUDGET_LIMIT`, `MIN_TIER_FLOOR`, `FALLBACK_AFTER_UPSTREAM_ERROR`

### Decision record

One MongoDB document per request, returned by `GET /v1/decisions`. It's the **only** data the audit dashboard reads, whichever dashboard we pick.

| Group | Fields |
|---|---|
| Identity | `decision_id`, `created_at`, `tenant_id`, `api_key_id`, `policy_id`, `policy_version`, `tags` |
| Request | `message_count`, `input_tokens_est`, `prompt_hmac` (keyed hash so short prompts can't be brute-forced back) |
| Sensitivity | `label`, `score`, `categories` with counts, `model_version`, `latency_ms`, `degraded` |
| Complexity | `tier`, `score`, `signals`, `model_version`, `latency_ms`, `degraded` |
| Route | `model`, `provider`, `locality`, `reason_codes`, `attempts` |
| Outcome | `status` (`ok`, `blocked`, `upstream_error`, `client_cancelled`), `http_status`, `input_tokens`, `output_tokens`, `ttft_ms`, `total_ms` |
| Cost | `actual_usd`, `baseline_usd`, `saved_usd` |

**Never in the record:** message or completion text, PII values, API keys.

---

## Internal classifier contract

Both classifier services expose the same endpoints, so the gateway treats them alike and either model can be swapped without a gateway change. They sit on the **private Docker network only**, never exposed publicly.

| Method | Path | What it does |
|---|---|---|
| POST | `/v1/classify` | Classify one request |
| GET | `/v1/info` | Model name, version, and the labels or tiers it can return |
| GET | `/healthz` | Liveness, and whether the model is loaded |

**Request (same for both):**
```json
{
  "request_id": "dec_01JB7Q2M4X9K3T6V8W0Y2Z4A6C",
  "messages": [
    { "role": "system", "content": "You are a sales assistant..." },
    { "role": "user", "content": "Summarise this clause for the sales team: ..." }
  ],
  "deadline_ms": 250
}
```

**Sensitivity response:**
```json
{
  "request_id": "dec_01JB7Q2M4X9K3T6V8W0Y2Z4A6C",
  "label": "confidential",
  "score": 0.91,
  "categories": [
    { "type": "PII.EMAIL_ADDRESS", "count": 2, "source": "presidio" },
    { "type": "BUSINESS.FINANCIAL", "count": 1, "source": "encoder" }
  ],
  "model_version": "sens-encoder-0.1+presidio",
  "latency_ms": 38
}
```

**Complexity response:**
```json
{
  "request_id": "dec_01JB7Q2M4X9K3T6V8W0Y2Z4A6C",
  "tier": "moderate",
  "score": 0.52,
  "signals": ["code", "multi_step"],
  "model_version": "cx-encoder-0.1",
  "latency_ms": 21
}
```

**Rules both teams build to:**

- **What each reads.** Sensitivity scans **every** message, including system and assistant turns, because the whole history goes to the provider. Complexity weights the last user turn and may truncate earlier turns.
- **No text out.** Responses carry entity types and counts, never matched values or offsets into the text.
- **Deadline.** If a service can't answer within `deadline_ms`, the gateway stops waiting and applies the fallback.
- **Fallbacks.** Sensitivity timeout/error → `restricted`, `degraded: true`. Complexity timeout/error → `complex`, `degraded: true` (costs more, never answers worse).
- **Mocks first.** Each team ships a mock that returns fixed labels by keyword in week one, so gateway work doesn't wait on trained models.

### Classifier design

**No frontier-model calls for routing.** Using a frontier model to pick a model would eat the savings and add ~1 s per request. The complexity classifier and sensitivity L1–L3 are rules and local encoders. The only LLM in the routing path is the sensitivity **L4 judge**, a small local model that runs **only** on prompts L3 is unsure about (see open questions on its latency). Otherwise LLM judges are used **offline only**, to label training data.

**Sensitivity detector:** layered and recall-biased. Full design in **Sensitivity detection** below.

**Difficulty classifier:**
- A small encoder that outputs the **minimum model tier** able to serve the request.
- *Labels:* offline, run each prompt through every tier and record the smallest tier whose output an LLM judge rates equivalent to the frontier output.
- Returns a **calibrated probability per tier**. A configurable threshold sets the org's point on the cost–quality curve, and low-confidence prompts **escalate one tier**.
- The same classifier drives both pools: cheap vs. frontier externally, small vs. large locally.
- Target classifier overhead: under 50 ms.

---

## Sensitivity detection

**Recall-biased.** A missed sensitive prompt is a data leak; a false positive only costs a bit more to serve. Covers English, Arabic and Franco (Arabizi).

### Pipeline

```
prompt ─► L1 regex ──restricted hit──► short-circuit → local model
              │
              ▼
      ┌── L2 NER ────────┐
      │                  │   (parallel, same prompt)
      └── L3 classifier ─┘
              │
              ▼
         Aggregator ──L3 unsure──► L4 LLM judge
              │                        │
              ▼◄───────────────────────┘
        Policy Engine ─► Router
```

- **L1 runs first.** A `restricted` hit short-circuits straight to the local model.
- **L2 and L3 run in parallel** on the same prompt.
- **Aggregator** merges spans and takes the **highest** sensitivity level across layers.
- **L4** runs only on prompts L3 is unsure about (roughly an L3 score of 40–70%; exact thresholds TBD).
- **Fail closed.** Any error or timeout in any layer → treat as sensitive → local model.

**How this fits the service contract:** L1 through L4 and the Aggregator live inside the sensitivity service, which still returns only `label`, `score` and `categories` (types + counts). L2's span positions stay inside the service, because the contract allows no text or offsets out. The Policy Engine is the gateway's policy router.

### Layers

| Layer | What it does | Model / method |
|---|---|---|
| **L1** Regex detector | Fixed patterns (emails, cards, Egyptian IDs, API keys) + per-company dictionaries | Rules, no training |
| **L2** NER transformer | Finds names, orgs, emails, etc. with exact positions (used for redaction) | Pre-trained, no training. `fastino/gliner2-privacy-filter-PII-multi` (GLiNER2-PII) vs `openai/privacy-filter`, compared head to head; the ~200 hand-marked prompts decide |
| **L3** Classifier | Judges whether the *meaning* of the prompt is sensitive. Multi-label | Fine-tuned `jhu-clsp/mmbert-base` (main). Baseline: `FacebookAI/xlm-roberta-base` or `microsoft/mdeberta-v3-base` |
| **L4** LLM judge | Second opinion, only for prompts L3 is unsure about | Small instruct LLM (~3–8B) on vLLM. TBD once the GPU budget is known |
| Aggregator | Merges spans, picks the final sensitivity level | Code |
| Policy Engine | Level → action: allow / redact and send / force local / block | Code (gateway policy router) |

**L3 labels (multi-label):** `strategic`, `financial`, `hr_personal`, `legal`, `credentials_code`, `customer_data`, `none`

TODO: how L1/L2 hits and L3 labels map to the four levels (`public` / `internal` / `confidential` / `restricted`).

### Datasets per layer

**L1** (rules, no training). Test only:
- Generated fake cards, Egyptian IDs, phones, IBANs, emails
- Fake secrets (patterns from gitleaks / detect-secrets)
- Tricky non-matches (order/invoice numbers)
- Fictional company dictionaries

**L2** (pre-trained, no training). Test only:
- ai4privacy PII-Masking-300k
- NVIDIA Nemotron-PII
- SPY benchmark
- ANERcorp + Wojood (Arabic)
- ~200 hand-marked prompts we write ourselves (**this set decides the L2 model**)

**L3** (trained). Training:
- Synthetic sensitive prompts per label (EN / AR / Franco)
- Synthetic hard negatives (same topic, not secret)
- WildChat / LMSYS-Chat-1M for the `none` class (personal info filtered)
- Enron emails wrapped in prompts
- Public company info (press releases, earnings calls) as hard negatives
- Fictional company prompts

**L3 test** (never trained on):
- Hand-labeled work prompts mined from WildChat / LMSYS, from **different conversations** than training
- Human-written prompts from the team + a form (made-up details only), written by people who **didn't build the generator**

**L4.** Test only:
- ~100 hand-labeled borderline prompts (L3 score ~40–70%)

**End-to-end.** Test only:
- ~300–500 prompts labeled with the correct final action

### Data rules

- **Test sets never leak into training.** Split WildChat / LMSYS by conversation, and keep generator output out of test sets.
- Human-written test prompts use made-up details only, never real personal data.
- Filter personal info out of WildChat / LMSYS before using it for training.
- Check each dataset's license and access terms. Don't commit gated or large datasets to the repo; fetch them with scripts and document them in `data/README.md`.

---

## Auth, errors, rate limits, streaming

**Auth.** Clients send `Authorization: Bearer sr_...`, which is what OpenAI SDKs do with `api_key`. Each key maps to one tenant, a default policy and scopes (`chat`, `audit:read`, `admin`). Keys are stored **hashed**. Provider keys live only in the gateway's secrets, never in client hands.

**Errors** use OpenAI's error shape so SDKs raise the right exception, plus `decision_id` when one exists:
```json
{ "error": { "message": "Request is confidential and the policy blocks it.",
  "type": "policy_error", "code": "sensitive_content_blocked", "param": null,
  "decision_id": "dec_01JB..." } }
```

| HTTP | Code | When |
|---|---|---|
| 400 | `invalid_request` | Malformed body or unknown model |
| 400 | `unsupported_content` | Image or audio parts (out of scope for v1) |
| 401 | `invalid_api_key` | Missing, unknown or revoked key |
| 403 | `scope_denied` | Key lacks the scope, e.g. a chat key on `/v1/policies` |
| 403 | `sensitive_content_blocked` | Policy blocks this sensitivity label |
| 404 | `not_found` | Unknown decision or policy id |
| 412 | `policy_version_conflict` | `PUT` policy with a stale `If-Match` |
| 422 | `no_eligible_model` | Nothing fits the label, tier and budget together |
| 429 | `rate_limited` | Over the key's limit; `Retry-After` says when |
| 502 | `upstream_error` | Provider failed after fallbacks |
| 503 | `local_model_unavailable` | Sensitive request but the local pool is down. **Never falls back to external** |
| 504 | `upstream_timeout` | Provider didn't answer in time |

**Rate limits.** Per key, requests/min and tokens/min, kept in Redis. Responses carry `x-ratelimit-remaining-requests` and `x-ratelimit-remaining-tokens` (same names as OpenAI).

**Streaming.** With `stream: true`, return SSE `chat.completion.chunk` objects ending with `data: [DONE]`.
- The decision is made **before** the upstream call, so routing headers arrive with the first byte.
- The last chunk before `[DONE]` carries `usage` (when `stream_options.include_usage` is set) and the `sentryroute` object.
- Fallback to another model only happens **before the first token**. An upstream failure mid-answer ends the stream with an error event; never silently switch models.

---

## Non-negotiables

These hold whatever else changes, and **tests must check each one.**

1. **Fail closed.** If the sensitivity service errors or times out, the request is `restricted` and goes local.
2. **No external fallback for sensitive traffic.** Fallback chains stay inside the same locality. Local pool down means a `503`, not a quiet hop to an external API.
3. **Pinned models don't bypass the check.** A client naming an external model still gets rerouted or blocked when the request is sensitive.
4. **No prompt text at rest.** Not in the decision log, app logs, trace attributes, exception messages or debug prints. Keep an HMAC of the prompt, entity types and counts, and token counts. Full capture is allowed only for tenants flagged as synthetic test data, and it's off by default.
5. **Classifiers are private.** They're only reachable from the gateway on the internal network.
6. **Measured overhead.** Both checks run in parallel with a 250 ms deadline each. Proposed target (to confirm once measured): routing adds under 100 ms at p95 on CPU for prompts under 2,000 tokens.

Also:
- **No secrets in the repo.** API keys, MongoDB URI, Tailscale/GPU box addresses go in `.env` (gitignored). Keep `.env.example` updated.

---

## Datasets

The sponsor won't provide datasets, so the core system is built on public and synthetic data only.

**Sensitivity:** per-layer training and test sets are in **Sensitivity detection → Datasets per layer**.

**Difficulty:**

| Dataset | Axis | Contents | Use |
|---|---|---|---|
| LLMRouterBench | Difficulty | Questions answered by many small and large models, with quality and cost | Train selection of the cheapest capable model |
| RouteLLM datasets | Difficulty | Human preferences between strong- and weak-model answers | When a stronger model is genuinely needed |
| RouterBench | Difficulty · eval | Prompts and recorded outcomes from multiple LLMs | Test that routing cuts cost without lowering quality |

For end-to-end evaluation, public prompts are mixed with **synthetically generated sensitive prompts** so the workload exercises both axes at once.

Document every dataset's source and license in `data/README.md`. Don't commit raw data containing real personal info.

## Evaluation

**Baselines:** always-frontier, always-cheap, random routing, RouteLLM, and a joint 6-class ComplianceGate-style classifier.
**Ablations:** sensitivity-only, difficulty-only, and joint routing.

| Metric | Axis | What it establishes |
|---|---|---|
| Cost–quality Pareto curve | Difficulty | Routing dominates baselines across a mixed workload, not just trading quality for price |
| Routing accuracy vs. oracle | Difficulty | How often we pick the cheapest adequate tier; under- and over-routing reported separately |
| Escalation rate | Difficulty | Guards against a cascade quietly escalating most traffic and costing more than no routing |
| **Leakage rate** | Sensitivity | % of sensitive prompts routed external. **Target: zero** |
| Detector precision & recall | Sensitivity | Recall bounds leakage; precision shows how much safe traffic is needlessly forced local |
| Quality retention on hard tasks | Both | Hard-subset quality vs always-frontier, on both external and local paths |
| End-to-end added latency | Both | Classifier overhead as a fraction of total response time |

## Risks and mitigations

- **Unstructured sensitive context is hard to detect.** The deterministic layer carries structured cases; the classifier handles the rest; uncertain prompts default local.
- **LLM-judge difficulty labels are noisy.** Human-verify a stratified sample and report agreement. Labels are based on output equivalence across tiers, not subjective "hard/easy."
- **Hard prompt misrouted to a small model.** Confidence-based escalation to the next tier; quality retention on the hard subset is tracked explicitly.
- **No sponsor traffic.** Public prompt datasets + synthetic sensitive prompts; weaker external validity claim, stated openly.
- **Insufficient hardware for local inference.** Evaluate with quantized small models (CPU if needed) and report the quality ceiling openly.

## Scope

**In v1:** gateway, sensitivity service, complexity service, policy router, decision log, web UI, audit dashboard (Phase 4).

**Not in v1, don't build unless asked:**
- Proposal add-on modules: A1 bilingual module as scoped in the proposal (Arabic for the complexity classifier, per-language reporting), A2 prompt injection detector, A3 adaptive routing (feedback loop). Note: the sensitivity detector itself does cover EN / AR / Franco.
- Semantic caching (mentioned in the proposal, not in the v1 contract)
- Redact mode (mask PII, then send external): the Oct 21 contract reserves it as `sensitive_action: redact` and keeps it out of v1, but the sensitivity design lists "redact and send" as a Policy Engine action. Don't build it until the open question below is settled.
- Image and audio inputs (rejected with `400 unsupported_content`)

## Open questions

| Question | Who decides | What it changes |
|---|---|---|
| Audit dashboard in Salesforce or our own web UI? | Prof. Mahmoud Khalil, with CloudzLab | Who builds the views; the API stays the same |
| Which GPUs / how much VRAM do the two laptops have? | Team | Which model size fits; below compute capability 7.0 also rules out vLLM |
| Which external models go in the pools? | Team, once AI subscriptions and credits are confirmed | Price table and tier mapping in the policy |
| Four sensitivity labels, or just sensitive / not sensitive? | Team | Dataset labelling; four is more work but a better thesis result |
| May `internal` requests go to external models by default? | Team, check with CloudzLab | Default policy |
| Is redact in v1? (Policy Engine lists "redact and send"; the Oct 21 contract says not in v1) | Team | Whether L2 spans ever leave the sensitivity service (contract says no offsets out), and who does the masking |
| How does L4 fit the 250 ms sensitivity deadline? A 3–8B judge on laptop GPUs likely won't | Sensitivity + gateway teams | A separate deadline for L4, or unsure prompts just go local without L4 |
| L4 on vLLM or Ollama? | Team, once laptop GPUs are known | Oct 21 doc picked Ollama for local models; vLLM needs compute capability 7.0+ |
| How do L1/L2 hits and L3 labels map to the four levels, and what goes in `categories[].type` / `source`? | Sensitivity team | Contract examples still say `presidio` / `encoder`; update `openapi.yaml` |

---

## Timeline

| Phase | Dates | Deliverables |
|---|---|---|
| 0 · Setup | late Sep 2026 (1 week) | Git repo, Jira board, sponsor kickoff, team roles, literature review |
| 1 · Research & design | early to mid Oct 2026 | Local and API model selection, datasets, system architecture |
| 2 · Core build (v1) | mid Oct to late Dec 2026 | Router gateway, first versions of sensitivity detection and complexity routing |
| 3 · Improvements | early Feb to mid Apr 2027 | Improvements, testing and tuning, comparison against existing approaches |
| 4 · Audit dashboard | mid Apr to mid May 2027 | Audit dashboard (Salesforce or custom) |
| 5 · Final delivery | mid May to end of June 2027 | Final fixes, thesis, presentation, live demo |

University midterms fall in mid November and mid April, so expect slower weeks then.

## Sponsor support (CloudzLab)

| Resource | Status |
|---|---|
| Technical mentor (biweekly) | Sponsor will try to provide |
| AI subscriptions | Sponsor will try to provide |
| Cloud / API credits (pays for external models) | Sponsor will try to provide |
| Salesforce org access (only if Salesforce dashboard is chosen) | Sponsor will try to provide |
| Cloud GPU servers | **Not provided.** Local models run on 2 team laptops |
| Sample data | **Not provided.** We build our own (see Datasets) |

What the sponsor gets: a working on-prem deployment with a measured cost-reduction figure and measured leakage rate, an audit trail suitable for compliance review, and early access to results and methodology.

---

## Repo layout

<!-- TODO: replace with the real structure once the repo is set up -->
- `api/openapi.yaml`: gateway contract (source of truth)
- `difficulty/`: complexity classifier Phase 1 on SPROUT (plan, notes, scripts; complexity only, no sensitivity code). Start at `difficulty/README.md`
- TODO: gateway service, sensitivity service, complexity service, web UI, eval harness, data

## Commands

<!-- Expected from the stack; confirm against the real scripts and update -->
```bash
uv sync                    # install Python deps from the hashed lockfile
docker compose up          # run the full stack locally
uv run pytest              # tests
uv run ruff check .        # lint
uv run mypy .              # type check
```
TODO: web UI commands, TS client generation from `openapi.yaml`, eval harness, spec-drift check.

## Workflow

- Agile sprints on Jira. Branch names: `<JIRA-KEY>-short-description` (project key: TODO).
- Reference the Jira ticket in commits and PRs.
- Changes go through PRs with at least one teammate's review. No direct pushes to `main`.
- CI (ruff, mypy, pytest, spec-drift) must pass before merging.
- Biweekly progress reviews with the sponsor's technical mentor.

## Notes for Claude

- **Spec first.** Contract changes start in `api/openapi.yaml`; code follows.
- **Use the mocks.** Build gateway features against the keyword mocks; don't wait on trained models.
- **Ask before adding dependencies**, especially anything that would end up in the gateway image.
- **Never let prompt text leak.** Watch logs, exception messages, trace attributes, test fixtures, and anything written to MongoDB.
- **Every non-negotiable needs a test.** When you touch routing, sensitivity handling or fallback, add or update the test that proves the rule still holds.
- **When unsure whether something is sensitive, treat it as sensitive.**
- **Never let test data into training.** Keep the sensitivity test sets out of any training or generator pipeline.
- **Keep router overhead low.** It's on the hot path of every request, and per-stage latency is a thesis result.
- Keep changes small and reviewable; this is an 8-person team working in parallel.
