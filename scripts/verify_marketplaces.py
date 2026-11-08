#!/usr/bin/env python3
"""Strict structural checks for two one-plugin marketplaces and three manifests."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/'plugins'/'symetria-dowodowa-tknc'
read=lambda f:json.loads((root/f).read_text(encoding='utf8'))
o=read('.agents/plugins/marketplace.json');c=read('.claude-plugin/marketplace.json')
a=read('plugins/symetria-dowodowa-tknc/plugin.json')
b=read('plugins/symetria-dowodowa-tknc/.claude-plugin/plugin.json')
l=read('plugins/symetria-dowodowa-tknc/.codex-plugin/plugin.json')
m=read('plugins/symetria-dowodowa-tknc/mcp.json')
assert len(o['plugins'])==len(c['plugins'])==1
assert a['name']==b['name']==l['name']==o['plugins'][0]['name']==c['plugins'][0]['name']=='symetria-dowodowa-tknc'
assert a['version']==b['version']==l['version']=='0.3.0'
assert o['plugins'][0]['source']['path']=='./plugins/symetria-dowodowa-tknc'
assert c['plugins'][0]['source']=='./plugins/symetria-dowodowa-tknc'
assert a['$schema']=='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
assert m['$schema']=='https://agent-plugins.org/schemas/1.0.0/mcp.schema.json'
assert m['mcpServers']['symetria-dowodowa']['type']=='stdio'
assert (p/'pyproject.toml').exists()
assert (p/'agents/rzecznik-obywatela.md').exists()
assert (p/'hooks/hooks.json').exists()
for x in (p/'skills').iterdir():
    if x.is_dir(): assert (x/'SKILL.md').is_file()
print('OK: OpenAI + Claude marketplace/manifests, one plugin, portable stdio MCP')
