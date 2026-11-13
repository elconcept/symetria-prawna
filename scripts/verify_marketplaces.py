#!/usr/bin/env python3
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/"plugins/symetria-dowodowa-tknc"
h=root/"plugins/symetria-prawna-hooki"
def read(f):return json.loads((root/f).read_text(encoding="utf-8"))
o=read("plugins/symetria-dowodowa-tknc/plugin.json")
c=read("plugins/symetria-dowodowa-tknc/.codex-plugin/plugin.json")
a=read(".agents/plugins/marketplace.json")
d=read("plugins/symetria-dowodowa-tknc/.claude-plugin/plugin.json")
m=read(".claude-plugin/marketplace.json")
hc=read("plugins/symetria-prawna-hooki/.claude-plugin/plugin.json")
hx=read("plugins/symetria-prawna-hooki/.codex-plugin/plugin.json")
VERSION="0.7.0"
assert o["version"]==c["version"]==d["version"]==hc["version"]==hx["version"]==VERSION
assert o["name"]==c["name"]==a["plugins"][0]["name"]=="symetria-dowodowa-tknc"
assert d["name"]==m["plugins"][0]["name"]=="symetria-prawna"
assert hc["name"]==hx["name"]==m["plugins"][1]["name"]==a["plugins"][1]["name"]=="symetria-prawna-hooki"
assert len(a["plugins"])==len(m["plugins"])==2
assert a["plugins"][0]["source"]["path"]==m["plugins"][0]["source"]=="./plugins/symetria-dowodowa-tknc"
assert a["plugins"][1]["source"]["path"]==m["plugins"][1]["source"]=="./plugins/symetria-prawna-hooki"
assert o["extensions"]["com.openai"]["interface"]["displayName"]=="Symetria Prawna"
assert a["interface"]["displayName"]=="Symetria Prawna"
# Regresja ochronna ChatGPT web: plugin ze skillem bez lokalnego wykonawcy (MCP, hooki).
for man in (o,c,d):
    assert "requires_local_executor" not in man and "mcpServers" not in man and "hooks" not in man
assert not (p/"mcp.json").exists() and not (p/".mcp.json").exists() and not (p/"hooks").exists()
assert sorted(x.parent.name for x in (p/"skills").glob("*/SKILL.md"))==["analiza-prawna"]
skill=p/"skills/analiza-prawna/SKILL.md"
text=skill.read_text(encoding="utf-8")
assert len(text.split())<=350
assert (p/"skills/analiza-prawna/agents/openai.yaml").read_text(encoding="utf-8").find("allow_implicit_invocation: true")>=0
for f in ["audyt-dowodowy.md","kanon-tk-nc.md","prawo-polskie.md"]:
 assert (p/"skills/analiza-prawna/references"/f).exists()
assert (p/"agents/audytor-prawny.md").is_file()
assert (p/".claude-plugin/plugin.json").is_file()
# Plugin hooków: domyślna ścieżka hooks/hooks.json (Claude Code i Codex), bez pola hooks w manifestach.
assert "hooks" not in hc and "hooks" not in hx
hooks=json.loads((h/"hooks/hooks.json").read_text(encoding="utf-8"))["hooks"]
assert set(hooks)=={"SessionStart","UserPromptSubmit","PostToolUse","Stop"}
assert (h/"hooks/symetria_hook.py").is_file()
assert (h/"hooks/symetria_core.py").read_bytes()==(p/"src/symetria_dowodowa/core.py").read_bytes(), "uruchom scripts/sync_hooks_core.py"
assert not (h/"skills").exists() and not (h/".mcp.json").exists()
print(f"OK: skill bez lokalnego wykonawcy ({len(text.split())} słów) + plugin hooków {VERSION} (Claude Code, Codex)")
