# Composio App-Research Agent & Case Study

[![GitHub Repository](https://img.shields.io/badge/GitHub-krbok%2FComposio-blue?logo=github)](https://github.com/krbok/Composio)
[![Dataset](https://img.shields.io/badge/Dataset-100%20Apps%20Evaluated-emerald)](out/all_100.json)
[![Interactive Dashboard](https://img.shields.io/badge/Case%20Study-index.html-indigo)](index.html)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](pyproject.toml)

An autonomous research pipeline evaluating **100 enterprise SaaS and developer platforms** across 10 categories for Composio agent toolkit buildability (auth method, multi-tenant gating, API surface, Model Context Protocol support, and buildability verdicts).

Built using the **Claude Agent SDK** backed by Composio's free Exa-powered search tools (`COMPOSIO_SEARCH_WEB`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`) with a dual-signal verification loop (deterministic Composio catalog cross-checks + secondary independent passes).

---

## 📑 Table of Contents
1. [Headline Findings & Macro Patterns](#-headline-findings--macro-patterns)
2. [Interactive Case Study Dashboard](#-interactive-case-study-dashboard)
3. [Architecture & Technical Design](#-architecture--technical-design)
4. [Where Human Was Needed vs. Agent Autonomy](#-where-human-was-needed-vs-agent-autonomy)
5. [Verification Honesty & Catalog Discrepancies](#-verification-honesty--catalog-discrepancies)
6. [Quickstart & Reproducibility](#-quickstart--reproducibility)
7. [Repository Structure](#-repository-structure)

---

## 📊 Headline Findings & Macro Patterns

Across the 100 evaluated applications (spanning CRM, Helpdesk, Messaging, Marketing, Ecommerce, Scraping/SEO, Developer Infra, Productivity, Fintech, and AI/Media), the agent identified several key macro patterns:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             HEADLINE METRICS                                │
├────────────────────────┬─────────────────────────┬──────────────────────────┤
│   BUILDABILITY         │    AUTH PROTOCOLS       │     MCP ECOSYSTEM        │
│   • 65% Buildable Now  │    • 66% OAuth 2.0      │     • 73% Official MCP   │
│   • 32% With Friction  │    • 28% API Key        │     • 24% Community MCP  │
│   •  3% Blocked        │    •  4% Basic / 2% CLI │     •  3% None           │
└────────────────────────┴─────────────────────────┴──────────────────────────┘
```

### 1. The "Personal App" Illusion (Multi-Tenant Gating)
A critical insight discovered during research: **single-developer access is often frictionless, but multi-tenant access is gated.**
* Many platforms (e.g., Zendesk, Close, Copper, Pipedrive) allow individual developers to generate private API keys or single-workspace OAuth apps immediately.
* However, a Composio toolkit requires a **multi-tenant path** where *other* users authorize their own accounts.
* **35% of platforms** enforce human gating for this multi-tenant path:
  * **Admin Review (16%):** e.g., Zendesk requires converting local clients to "Global OAuth Clients" via marketplace ops; Close requires human review to make an OAuth app public.
  * **Partner / Marketplace Gating (14%):** e.g., Amazon SP-API requires becoming an approved Solution Provider; Front requires App Store listing.
  * **Paid Plan Requirements (5%):** e.g., Smartsheet requires Business+ licensing for developer tools; Devin and Grain require paid subscriptions.

### 2. Explosive MCP Adoption (73% Official First-Party)
* **73 out of 100 apps** now publish or host an official Model Context Protocol server (e.g., HubSpot, Stripe, Brex, Ramp, Xero, Smartsheet, QuickBooks, Consensus, Devin, Otter AI, Grain).
* MCP is rapidly becoming the standard interface for AI agent integration alongside traditional REST endpoints.
* **24% have active open-source community MCP wrappers**, leaving only 3% with no MCP footprint.

### 3. Category Polarization
* **Developer & Infra (80% instant)** and **Productivity (90% instant)** are heavily self-serve with instant API key / OAuth provisioning (Vercel, Supabase, Cloudflare, Linear, Notion, Harvest).
* **Marketing & Ads (60% gated)** and **Enterprise ERP/CRM** strictly enforce partner verification and business compliance checks (Meta Ads, Google Ads, LinkedIn Ads, DealCloud, Salesforce Commerce Cloud).

### 4. The 3 Strictly Blocked Outliers
Only 3 apps out of 100 are strictly blocked for automated toolkit buildability today:
1. **Salesforce Commerce Cloud (B2C):** No public developer sandbox or self-serve signup; sandboxes require an active commercial contract and purchasing credits through an Account Executive.
2. **Ahrefs Connect:** API v3 multi-tenant OAuth strictly mandates an active Enterprise subscription + manual sales application review.
3. **Sherlock:** Local open-source Python CLI tool with no hosted public API or authentication infrastructure.

---

## 🖥️ Interactive Case Study Dashboard

The complete findings are published as a standalone, zero-dependency interactive dashboard in [`index.html`](index.html).

- **Interactive 100-App Matrix:** Live search, multi-criteria filtering (Category, Buildability, Auth Protocol, MCP Status), and column sorting.
- **Deep-Dive Drawer/Modals:** Click "Inspect" on any row to view full blocker details, API breadth, and verified official doc evidence URLs.
- **Visual Pattern Cards:** Visual breakdown of authentication distributions, gating tiers, and MCP readiness.
- **Honesty Log:** Direct comparison of agent findings vs. Composio's live catalog.
- **Instant JSON Export:** Export filtered rows directly from the browser for offline analysis.

To view locally:
```bash
# Serve locally
python3 -m http.server 8000
# Open http://localhost:8000 in your browser
```

---

## 🏗️ Architecture & Technical Design

The pipeline was built using a clean, resilient agentic loop:

```
┌─────────────────────────────────────────────────────────────┐
│                      APPS_100 Dataset                       │
│           (100 Apps across 10 distinct categories)          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Stage 1: Claude Agent SDK Loop                │
│  - Composio Exa Search & URL Fetch (No-Auth)                │
│  - Dedicated "<app> MCP server" search pass                 │
│  - Multi-tenant gating evaluation (RFC / public apps)       │
│  - Pydantic schema validation at tool-call boundary         │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│               Stage 2: Verification Engine                  │
│  Signal A: Deterministic Composio Catalog Cross-Check       │
│  Signal B: Independent Secondary Browser/Search Pass        │
│  Flags discrepancies & calculates final confidence          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Validated Output Artifacts                │
│  - out/all_100.json (Full 100-row structured dataset)       │
│  - index.html (Interactive Standalone Case Study)           │
└─────────────────────────────────────────────────────────────┘
```

1. **Strict Pydantic Schema (`research/schema.py`):**
   Enforces exact enums for `AuthMethod`, `SelfServeStatus`, `ApiSurface`, `ApiBreadth`, `HasMcp`, and `Buildability`. The model ends its turn by invoking `submit_finding`. Hallucinated enum values or invalid URLs fail validation at the boundary, preventing malformed data from ever entering `out/all_100.json`.

2. **Agent Isolation & Tool Sandboxing (`research/agent.py`):**
   - Directs `claude-agent-sdk` to a local `node_modules/.bin/claude` binary for complete portability.
   - Clears ambient environment variables (`ANTHROPIC_API_KEY`) to prevent unintended metered billing while leveraging Claude Code CLI login.
   - Uses `bypassPermissions` with strictly isolated toolsets (`COMPOSIO_SEARCH_WEB`, `COMPOSIO_SEARCH_FETCH_URL_CONTENT`, `submit_finding`) to block unwanted local command execution or ambient tool leakage during unattended batch runs.

3. **Dual-Signal Verification Loop (`research/verify.py`):**
   - **Signal A (Catalog Truth):** Deterministic query against Composio's real catalog (`composio.toolkits.get`).
   - **Signal B (Independent Second Pass):** A secondary pass using native WebSearch/WebFetch without seeing first-pass answers to prevent anchoring bias.
   - Discrepancies are flagged for human review with exact field diffs.

4. **Resumable Incremental Storage (`research/run_all.py`):**
   Every completed row is written to disk immediately with mutex locking, enabling the pipeline to resume seamlessly from rate limits or interruptions without losing progress.

---

## 🤖 Where Human Was Needed vs. Agent Autonomy

| Dimension | Handled Autonomously by Agent | Required Human Engineering / Oversight |
| :--- | :--- | :--- |
| **Documentation Ingestion** | Fetched and parsed 100+ developer portals, OpenAPI specs, and auth guides. | Built search query strategies and Exa fetch pipelines. |
| **Gating Evaluation** | Identified subtle multi-tenant friction points (e.g., Zendesk Global OAuth client review). | Defined strict multi-tenant definitions to stop agents from defaulting to private API keys. |
| **MCP Discovery** | Discovered newly released (2024-2026) first-party and community MCP servers. | Mandated dedicated MCP search steps in the system prompt. |
| **Process Isolation** | Extracted exact schema outputs adhering to Pydantic constraints. | Sandboxed CLI subprocesses and isolated environment tokens. |
| **Catalog Reconciliation** | Accurately flagged discrepancies against Composio catalog. | Analyzed and explained root causes for catalog differences. |

---

## 🔍 Verification Honesty & Catalog Discrepancies

Comparing the agent's findings against Composio's live catalog (`composio.toolkits.get`) matched **50 toolkits**, with **44 agreeing immediately**.

The **6 discrepancies** highlighted key architectural nuances where the agent's multi-tenant evaluation was more accurate for production integrations than legacy catalog entries:

| App | Agent Finding | Composio Catalog | Technical Explanation & Verdict |
| :--- | :--- | :--- | :--- |
| **Close CRM** | `OAuth2` (*admin-approval*) | `API_KEY` | **Agent is more accurate for multi-tenancy.** Composio uses single-user API keys. True multi-tenant Close apps require Close approval to become public OAuth apps. |
| **Front** | `OAuth2` (*partner-gated*) | `API_KEY` | **Agent is more accurate for multi-tenancy.** Front supports API keys for internal scripts, but multi-tenant apps require official App Store partner review. |
| **Ahrefs** | `OAuth2` (*partner-gated*) | `API_KEY` | **Agent is correct.** Ahrefs API v3 supports OAuth2 via "Ahrefs Connect", strictly requiring Enterprise plan + sales approval. API key is personal single-account only. |
| **Vercel** | `OAuth2` (*self-serve-free*) | `API_KEY` | **Both valid.** Composio uses personal access tokens; Vercel Integrations platform supports self-serve multi-tenant OAuth2 apps. |
| **Cloudflare** | `OAuth2` (*self-serve-free*) | `API_KEY` | **Both valid.** Cloudflare supports both scoped API Tokens and OAuth 2.0 applications for third-party integrations. |
| **Consensus** | `OAuth2` (*self-serve-free*) | `API_KEY` | **Agent caught the latest 2025/2026 update.** Consensus released an official OAuth2 PKCE MCP server (`mcp.consensus.app/mcp`) alongside its legacy REST API key. |

---

## 🚀 Quickstart & Reproducibility

### 1. Prerequisites & Setup

```bash
# Clone repository
git clone https://github.com/krbok/Composio.git
cd Composio

# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Install local Claude Code CLI
npm install

# Configure Composio API Key
cp .env.example .env
# Edit .env and add: COMPOSIO_API_KEY=your_composio_key
```

### 2. Run the 5-App Stress Test Benchmark

```bash
python -m research.stress_test
```
*Executes research on 5 contrasting apps and outputs to `out/stress_test.json`.*

### 3. Run Stage-2 Verification on the Stress Test

```bash
python -m research.verify_stress_test
```
*Cross-checks results against Composio catalog and writes `out/verified_stress_test.json`.*

### 4. Run the Full 100-App Pipeline

```bash
python -m research.run_all --concurrency 3
```
*Resumable execution that saves incrementally to `out/all_100.json`.*

### 5. Rebuild the HTML Case Study

```bash
python build_case_study.py
```
*Generates the standalone `index.html` case study dashboard.*

---

## 📂 Repository Structure

```
.
├── index.html                   # Standalone Interactive Case Study Dashboard
├── build_case_study.py          # HTML Case Study compilation script
├── pyproject.toml               # Python package configuration
├── package.json                 # Node dependencies (@anthropic-ai/claude-code)
├── .gitignore                   # Git ignore rules (tracks JSON datasets)
├── out/
│   ├── all_100.json             # Complete 100-app validated research dataset
│   ├── all_100_failures.json    # Failure log (0 failures remaining)
│   ├── stress_test.json         # 5-app stress test benchmark
│   └── verified_stress_test.json# Dual-pass verification output
└── research/
    ├── __init__.py
    ├── apps_100.py              # The 100-app dataset definitions & hints
    ├── schema.py                # Pydantic row & enum models
    ├── agent.py                 # Claude Agent SDK runner with Composio tools
    ├── verify.py                # Stage-2 verification & catalog cross-check
    ├── run_all.py               # Resumable 100-app batch runner
    ├── stress_test.py           # 5-app stress test runner
    └── verify_stress_test.py    # Stress test verification runner
```

---

## 📜 License

MIT License. Built for the Composio App Research Case Study.