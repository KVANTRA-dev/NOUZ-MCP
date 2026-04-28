# NOUZ — Semantic MCP Server for Your Knowledge Base

Works with Obsidian, Logseq, and any directory of Markdown files.

> *Structure emerges from content.*

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![MCP](https://img.shields.io/badge/protocol-MCP_stdio-lightgrey.svg)](https://modelcontextprotocol.io)
[![PyPI](https://img.shields.io/badge/pypi-nouz--mcp-orange.svg)](https://pypi.org/project/nouz-mcp/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19595850.svg)](https://doi.org/10.5281/zenodo.19595850)

🇷🇺 [Русская версия](README_RU.md)

---

## Why NOUZ

When your knowledge base grows — organizing documents into folders stops working. Your AI agent sees files, but doesn't understand how your ideas and documents connect.

NOUZ gives your agent semantic coordinates. Each note gets a domain sign, a hierarchy level, and connections to other notes. The domain is assigned from the file's content — or manually by you, if you prefer strict hierarchy.

---

## What It Does

NOUZ sits between your note base and your AI agent. It handles all the chaos-structuring:

1. **Automatic Classification (Semantics)**  
   You define "Cores" — base domains of your interests (e.g., 🧠 Systems Thinking, 🧬 Science, 💻 Code). When you add a new note, NOUZ reads its text, compares vectors, and automatically assigns the correct domain (Sign) or a combination of domains.

2. **Hidden Connection Discovery (Bridges)**  
   The server doesn't just build a directed graph (DAG). It finds non-obvious intersections between disciplines:
   - *Semantic bridges:* two notes from different domains talk about the same thing.
   - *Tag bridges:* notes share hidden concepts at the tag level.
   - *Analogies:* notes play the same structural role in different sciences (e.g., "framework" in IT and "taxonomy" in biology).

3. **Base Evolution Tracking (Drift)**  
   NOUZ aggregates data bottom-up. If your "Philosophy" folder started accumulating too many notes about algorithms, the system notices and shows the divergence (core drift) — your folder evolved.

Depending on your needs, NOUZ works in three modes: from a simple visual graph (**LUCA**) to a strict 5-level self-organizing hierarchy (**SLOI**).

---

## How It Works

1. You describe domains in `config.yaml` — what each does, what language it speaks.
2. The server turns descriptions into vector etalons (locally, via LM Studio or Ollama).
3. Each new note is projected onto these axes. Sign is determined by content, or by you.
4. Modules automatically receive `core_mix` — aggregated core composition from all their quants. If a module's `sign` diverges from `core_mix` — the server reports `core_drift`.

**Three types of bridges** find connections between notes from different domains: semantic (texts are close), tag (concepts overlap), analogy (similar role in the graph).

---

## Quick Start

```bash
pip install nouz-mcp
OBSIDIAN_ROOT=/path/to/vault nouz-mcp
```

Without `config.yaml`, the server starts in **LUCA** mode — graph without semantics, works immediately.

Or from source:

```bash
git clone https://github.com/KVANTRA-dev/NOUZ-MCP
cd NOUZ-MCP
pip install -r requirements.txt
OBSIDIAN_ROOT=./vault python server.py
```

Connect to Claude Desktop, Cursor, OpenCode, or any MCP client:

```json
{
  "mcpServers": {
    "nouz": {
      "command": "nouz-mcp",
      "env": {
        "OBSIDIAN_ROOT": "/path/to/vault",
        "MODE": "prizma",
        "EMBED_API_URL": "http://127.0.0.1:1234/v1"
      }
    }
  }
}
```

---

## MCP Tools

| Tool | Purpose |
|------------|-------|
| `suggest_metadata` | Sign, level, bridges, drift warnings |
| `write_file` | Write a note with YAML frontmatter |
| `read_file` | Read a note + metadata |
| `calibrate_cores` | Update core reference vectors |
| `recalc_signs` | Recalculate signs for all notes |
| `recalc_core_mix` | Recalculate bottom-up aggregation |
| `index_all` | Re-index the entire base |
| `format_entity_compact` | Formula `(children)[sign]{parents}` |
| `embed` | Get a vector for text |
| `list_files` | List with filters by level, sign |
| `get_children` / `get_parents` | Graph traversal |
| `suggest_parents` | Find parents for an orphan |
| `add_entity` | Create an entity in one step (auto sign, tags, parents) |
| `process_orphans` | Auto-fill files without markup |

---

## Configuration

Minimal `config.yaml`:

```yaml
mode: prizma

etalons:
  - sign: S
    name: Systems Thinking
    text: >
      Methodology for analysing complex objects: feedback loops,
      emergent properties, self-regulation, bifurcation points.
      Cybernetics, synergetics, dissipative structures — tools for
      understanding how the whole exceeds the sum of its parts.
      Not data and not code — a way of thinking about complexity.
  - sign: D
    name: Data & Science
    text: >
      Physics and cosmology: Lagrangians, curvature tensors, quarks,
      fermions, plasma, vacuum fluctuations, cosmic microwave background.
      Pure science about the nature of matter, energy and spacetime.
  - sign: E
    name: Engineering
    text: >
      Software engineering, ML, infrastructure: writing and debugging
      code, deployment, containerisation, neural networks, inference,
      microservices, CI/CD, refactoring, APIs. The practical discipline
      of building computational systems from architecture to production.

thresholds:
  sign_spread: 0.05
  confident_spread: 60.0
  pattern_second_sign_threshold: 30.0
  semantic_bridge_threshold: 0.55
  structural_bridge_threshold: 0.55
  parent_link_threshold: 0.55
```

After setup, run `calibrate_cores` — the server creates reference vectors.
Check pairwise cosines: mean-centered between different domains should be
noticeably lower than raw. If all pairs are roughly equal — strengthen the differences in texts.

### Real Calculation Example

Here are actual results for the S/D/E etalons using the `text-embedding-granite-embedding-278m-multilingual` model:

```
=== Pairwise Cosine (raw) ===
S↔D: 0.5890    S↔E: 0.5853    D↔E: 0.6011

=== Pairwise Cosine (mean-centered) ===
S↔D: -0.5051   S↔E: -0.5120   D↔E: -0.4827
```

Negative mean-centered values are an excellent result: cores are semantically well-separated. Self-classification: S→99.2%, D→97.6%, E→96.9%.

| Variable | Default | Description |
| --- | --- | --- |
| `OBSIDIAN_ROOT` | `./obsidian` | Path to vault |
| `MODE` | `luca` | `luca`, `prizma`, or `sloi` |
| `EMBED_PROVIDER` | `openai` | `openai`, `lmstudio`, `ollama` |
| `EMBED_API_URL` | `http://127.0.0.1:1234/v1` | Embedding endpoint |
| `EMBED_API_KEY` | *(empty)* | API key, if needed |
| `EMBED_MODEL` | *(empty)* | Model name |

---

## Privacy

| Component | Local? |
|-----------|-----------|
| Embeddings (LM Studio / Ollama) | ✅ Yes |
| Your notes | ✅ Yes |
| NOUZ server | ✅ Yes |
| AI agent context (Claude, ChatGPT) | ❌ Goes to cloud |

Everything critical stays on your machine.

---

## Development

```bash
git clone https://github.com/KVANTRA-dev/NOUZ-MCP
cd NOUZ-MCP
pip install -e .
python -m pytest test_server.py
```

---

## Links

- 🌐 [kvantra.tech](https://kvantra.tech)
- 📦 [PyPI](https://pypi.org/project/nouz-mcp/)
- 🗂️ [Glama Registry](https://glama.ai/mcp/servers/KVANTRA-dev/NOUZ-MCP)
- 💬 [Telegram](https://t.me/volnaya_sreda)
- 🐙 [GitHub](https://github.com/KVANTRA-dev/NOUZ-MCP)
- 📄 [Paper "Recursive Self-Organization as a Universal Principle"](https://doi.org/10.5281/zenodo.19595850)

---

MIT License © 2026 KVANTRA

*Cosines are computed. Syntax changes. Semantics remains.*

<!-- mcp-name: io.github.KVANTRA-dev/NOUZ-MCP -->
