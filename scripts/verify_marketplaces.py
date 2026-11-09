#!/usr/bin/env python3
"""Check the single ChatGPT/Codex marketplace and supported plugin manifests."""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
p = root / "plugins" / "symetria-dowodowa-tknc"

def read(path):
    return json.loads((root / path).read_text(encoding="utf8"))

market = read(".agents/plugins/marketplace.json")
plugin = read("plugins/symetria-dowodowa-tknc/plugin.json")
legacy = read("plugins/symetria-dowodowa-tknc/.codex-plugin/plugin.json")
mcp = read("plugins/symetria-dowodowa-tknc/mcp.json")

assert len(market["plugins"]) == 1
assert market["plugins"][0]["name"] == plugin["name"] == legacy["name"] == "symetria-dowodowa-tknc"
assert market["plugins"][0]["source"]["path"] == "./plugins/symetria-dowodowa-tknc"
assert plugin["version"] == legacy["version"] == "0.4.0"
assert plugin["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
assert mcp["$schema"] == "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
assert mcp["mcpServers"]["symetria-dowodowa"]["type"] == "stdio"
assert (p / "skills" / "analiza-dowodowa" / "references" / "prawo-polskie.md").exists()
assert (p / "skills" / "audyt-dowodowy" / "references" / "rzecznik-obywatela.md").exists()
assert (p / "pyproject.toml").is_file()
for deleted in [root / ".claude-plugin", p / ".claude-plugin", p / "hooks", p / "commands", p / "agents", p / ".mcp.json"]:
    assert not deleted.exists(), deleted
for item in (p / "skills").iterdir():
    if item.is_dir():
        assert (item / "SKILL.md").is_file(), item
print("OK: 1 ChatGPT/Codex marketplace, 1 plugin, Polish procedure, no Claude artifacts")
