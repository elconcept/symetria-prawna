#!/usr/bin/env python3
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/"plugins/symetria-dowodowa-tknc"
def read(f):return json.loads((root/f).read_text(encoding="utf-8"))
o=read("plugins/symetria-dowodowa-tknc/plugin.json")
c=read("plugins/symetria-dowodowa-tknc/.codex-plugin/plugin.json")
a=read(".agents/plugins/marketplace.json")
d=read("plugins/symetria-dowodowa-tknc/.claude-plugin/plugin.json")
m=read(".claude-plugin/marketplace.json")
assert o["version"]==c["version"]==d["version"]=="0.6.0"
assert o["name"]==c["name"]==a["plugins"][0]["name"]=="symetria-dowodowa-tknc"
assert d["name"]==m["plugins"][0]["name"]=="symetria-prawna"
assert len(a["plugins"])==len(m["plugins"])==1
assert a["plugins"][0]["source"]["path"]==m["plugins"][0]["source"]=="./plugins/symetria-dowodowa-tknc"
assert o["extensions"]["com.openai"]["interface"]["displayName"]=="Symetria Prawna"
assert a["interface"]["displayName"]=="Symetria Prawna"
assert "requires_local_executor" not in c and "mcpServers" not in c
assert not (p/"mcp.json").exists() and not (p/".mcp.json").exists()
assert sorted(x.parent.name for x in (p/"skills").glob("*/SKILL.md"))==["analiza-prawna"]
skill=p/"skills/analiza-prawna/SKILL.md"
text=skill.read_text(encoding="utf-8")
assert len(text.split())<=350
assert (p/"skills/analiza-prawna/agents/openai.yaml").read_text(encoding="utf-8").find("allow_implicit_invocation: true")>=0
for f in ["audyt-dowodowy.md","kanon-tk-nc.md","prawo-polskie.md"]:
 assert (p/"skills/analiza-prawna/references"/f).exists()
assert (p/"agents/audytor-prawny.md").is_file()
assert (p/".claude-plugin/plugin.json").is_file()
assert not (p/"hooks").exists()
print(f"OK: OpenAI skills-only and Claude Code manifests, one skill, private case reference on demand, {len(text.split())} words")
