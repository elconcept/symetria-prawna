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


assert len(market["plugins"]) == 1
assert market["plugins"][0]["name"] == plugin["name"] == legacy["name"] == "symetria-dowodowa-tknc"
assert market["plugins"][0]["source"]["path"] == "./plugins/symetria-dowodowa-tknc"
assert plugin["version"] == legacy["version"] == "0.5.0"
assert plugin["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
assert not (p / "mcp.json").exists(), "stdio MCP makes ChatGPT plugin desktop-only"
assert not (p / ".mcp.json").exists(), "legacy MCP must not be bundled"
assert "mcpServers" not in plugin and "mcpServers" not in legacy
assert not legacy.get("requires_local_executor", False)
assert not plugin.get("extensions", {}).get("com.openai", {}).get("requires_local_executor", False)
assert (p / "skills" / "analiza-dowodowa" / "references" / "prawo-polskie.md").exists()
assert (p / "skills" / "analiza-dowodowa" / "references" / "audyt.md").exists()
assert (p / "pyproject.toml").is_file()
for deleted in [root / ".claude-plugin", p / ".claude-plugin", p / "hooks", p / "commands", p / "agents", p / ".mcp.json"]:
    assert not deleted.exists(), deleted
assert sorted(x.parent.name for x in (p / "skills").glob("*/SKILL.md")) == ["analiza-dowodowa"], "must have one skill"
assert (p / "skills/analiza-dowodowa/agents/openai.yaml").is_file()
assert "allow_implicit_invocation: true" in (p / "skills/analiza-dowodowa/agents/openai.yaml").read_text(encoding="utf-8")
skill = (p / "skills/analiza-dowodowa/SKILL.md").read_text(encoding="utf-8")
assert len(skill.split()) <= 350, "SKILL.md too long"
for item in (p / "skills").iterdir():
    if item.is_dir():
        assert (item / "SKILL.md").is_file(), item
print(f"OK: ChatGPT skills-only, 1 marketplace, 1 skill, implicit invocation enabled, {len(skill.split())} words")
