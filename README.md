# Nouz — Semantic Knowledge Engine for Obsidian

> *Structure emerges from content. Not from folders.*

Nouz is an MCP server that builds a semantic graph over your Obsidian vault. Notes are classified by meaning — not by where you put them.

**Designed for:**
- Researchers and academics managing large knowledge bases
- Scientists who think in cross-domain connections and systems
- Developers building AI-augmented personal knowledge workflows

---

## How it works

Nouz reads your vault, computes embeddings, and organizes notes into a directed acyclic graph (DAG) based on semantic similarity and explicit hierarchy links.

Three modes depending on how deep you want to go:

| Mode | What it does |
|------|-------------|
| `luca` | Graph traversal — navigate parent/child relationships |
| `prizma` | Semantic cores — classify notes into knowledge domains |
| `sloi` | Hierarchy levels — enforce structure (core → pattern → module → quant → artifact) |

---

## Installation

```bash
pip install nouz-mcp
```

## Quick start

```bash
# Point at your vault
OBSIDIAN_ROOT=/path/to/vault nouz-mcp

# With semantic classification
MODE=prizma EMBED_ENABLED=true nouz-mcp
```

Add to your MCP client config (Claude Desktop, etc.):

```json
{
  "mcpServers": {
    "nouz": {
      "command": "nouz-mcp",
      "env": {
        "OBSIDIAN_ROOT": "/path/to/your/vault"
      }
    }
  }
}
```

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OBSIDIAN_ROOT` | `./obsidian` | Path to Obsidian vault |
| `MODE` | `prizma` | Server mode: `luca`, `prizma`, `sloi` |
| `EMBED_ENABLED` | `true` | Enable semantic features |
| `EMBED_PROVIDER` | `openai` | Provider: `openai`, `lmstudio`, `gigachat` |
| `EMBED_API_URL` | `http://127.0.0.1:1234/v1` | Embedding endpoint |

---

## MCP Tools

- `read_file` — Read note with YAML metadata
- `write_file` — Create/update note with hierarchy
- `list_files` — Filter by level, sign, subfolder
- `get_children` — Traverse DAG downward
- `get_parents` — Traverse DAG upward
- `suggest_metadata` — Auto-classify a note
- `suggest_parents` — Find semantic parent candidates
- `index_all` — Reindex the vault
- `embed` — Get text embedding
- `format_entity_compact` — Compact graph formula for a node

---

## Development

```bash
pip install -e .
pytest
```

---

## Links

- [Glama registry](https://glama.ai/mcp/servers/KVANTRA-dev/NOUZ-MCP)
- [GitHub](https://github.com/KVANTRA-dev/NOUZ-MCP)
- [Website](https://kvantra-dev.github.io/nouz/)

---

*Built by [Maria Belkina](https://github.com/KVANTRA-dev) · KVANTRA*

<!-- mcp-name: io.github.KVANTRA-dev/NOUZ-MCP -->
