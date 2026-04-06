# NOUZ Guide

A comprehensive guide to semantic knowledge management with NOUZ.

## What is NOUZ?

NOUZ is an MCP server that brings semantic structure to your Obsidian vault. It analyzes your notes via embeddings and builds a knowledge graph based on meaning, not folders.

## Architecture & Modes

### LUCA — Pure Graph (Default)
Simple graph mode. Level and type are for display only, no semantic classification. Good for general note-taking.

### PRIZMA — Graph + Semantics
Graph-based with semantic bridges and core_mix. Calculates how close your notes are to defined categories. Recommended for most use cases.

### SLOI — Strict Hierarchy
Strict 5-level hierarchy with validation. Use when you need an enforced DAG (Directed Acyclic Graph) structure.

## Five Levels

| Level | Type | Description |
|-------|------|-------------|
| 1 | Core | Top-level domain (e.g., "Mathematics") |
| 2 | Pattern | Knowledge area within domain |
| 3 | Module | Grouping within field |
| 4 | Quant | Concrete entity |
| 5 | Artifact | Leaf note/reference |

## YAML Format

Each note should have YAML frontmatter:

```yaml
---
type: module
level: 3
sign: T
status: active
tags:
  - research
parents:
  - Core Name
parents_meta:
  - entity: Core Name
    link_type: hierarchy
---
```

## Semantic Etalons (Optional)

Etalons are reference texts that define the "axes" of your semantic space. By default, NOUZ starts in **LUCA** mode without them.

If you activate **PRIZMA** or **SLOI** by defining etalons in `config.yaml`, NOUZ can:
- Automatically classify notes by semantic similarity (auto-signs)
- Calculate `core_mix` (percentage blend of domains)
- Suggest related notes via embeddings

### How to Configure

Copy `config.template.yaml` to `config.yaml` and define your domains. Here is an interdisciplinary example:

```yaml
mode: prizma

etalons:
  - sign: T
    name: Technology
    text: "programming software architecture infrastructure machine learning neural networks algorithms"
  - sign: S
    name: Science
    text: "physics chemistry biology mathematics formal logic theorems cosmology quantum mechanics"
  - sign: H
    name: Humanities
    text: "philosophy psychology sociology history literature art culture ethics cognitive science"
```

### Best Practices

**For best results, use 3-5 distinct domains with cosine similarity < 0.55 between them:**

1. **Different fields** — Use distinct knowledge domains
2. **Keyword-dense text** — Each etalon should be a dense list of keywords, not a story
3. **Test with embeddings** — Run `calibrate_cores` and check the pairwise cosine similarity

Example of well-separated etalons:

| Sign | Domain     | Keywords                                        |
| ---- | ---------- | ----------------------------------------------- |
| T    | Technology | programming, software, machine learning, code   |
| S    | Science    | physics, mathematics, theorem, biology, atoms   |
| H    | Humanities | philosophy, history, sociology, ethics, culture |

**Recommendation:** If your domain similarity is > 0.55, the semantic classification will be less accurate but still functional.

## Tools

### Basic (all modes)
- `read_file(path)` — Read note with YAML
- `write_file(path, content, metadata)` — Write note
- `list_files(level, sign, tags)` — Filter files
- `index_all(with_embeddings)` — Index to SQLite DB
- `embed(text)` — Get embedding from configured provider

### Navigation
- `get_parents(path)` — Files linking to this file
- `get_children(path)` — Files this file links to

### Semantics (Prizma / Sloi only)
- `calibrate_cores()` — Recalculate etalon embeddings
- `recalc_signs()` — Auto-assign signs based on content
- `recalc_core_mix()` — Calculate core_mix bottom-up
- `suggest_metadata(path)` — Suggest level/sign/tags
- `suggest_parents(path)` — Suggest links by embeddings
- `format_entity_compact(path)` — Entity formula

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OBSIDIAN_ROOT` | ./obsidian | Vault path |
| `MODE` | luca | luca / prizma / sloi (Overridden by config.yaml) |
| `EMBED_PROVIDER` | openai | openai / gigachat / ollama |
| `EMBED_API_URL` | http://127.0.0.1:1234/v1 | API endpoint |
| `EMBED_MODEL` | — | Model name |
| `EMBED_API_KEY` | — | API key |

## Example Workflow

1. **Start server** — `python server.py`
2. **Add YAML** to your notes (level, type, sign)
3. **Index** — `index_all(with_embeddings=true)`
4. **Calibrate etalons** (optional) — `calibrate_cores()`
5. **Recalc signs** (optional) — `recalc_signs()`
6. **Query** — Use `suggest_parents`, `list_files`, etc.

## Learn More

- Website: https://kvantra-dev.github.io/nouz/
- GitHub: https://github.com/KVANTRA-dev/NOUZ-MCP

---

> _Косинусы считаются, синтаксис меняется, семантика остаётся._
