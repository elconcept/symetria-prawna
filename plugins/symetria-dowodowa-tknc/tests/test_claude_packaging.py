from pathlib import Path
import unittest
import json

REPO=Path(__file__).resolve().parents[3]
PLUGIN=REPO/"plugins/symetria-dowodowa-tknc"

class ClaudeCodePackage(unittest.TestCase):
    def test_single_plugin_marketplace(self):
        market=json.loads((REPO/".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(len(market["plugins"]),1)
        self.assertEqual(market["plugins"][0]["name"],"symetria-prawna")
        self.assertEqual(market["plugins"][0]["source"],"./plugins/symetria-dowodowa-tknc")
        self.assertTrue(market["owner"]["name"])

    def test_manifest_identity_and_version(self):
        m=json.loads((PLUGIN/".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        o=json.loads((PLUGIN/"plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(m["name"],"symetria-prawna")
        self.assertEqual(m["version"],o["version"])
        self.assertTrue(m["description"])
        self.assertEqual(o["name"],"symetria-dowodowa-tknc")  # account-safe legacy internal ID

    def test_agent_references_and_one_skill(self):
        agent=(PLUGIN/"agents/audytor-prawny.md").read_text(encoding="utf-8")
        self.assertTrue(agent.startswith("---\n"))
        self.assertIn("name: audytor-prawny",agent)
        self.assertIn("nie",agent.lower())
        self.assertEqual(len(list((PLUGIN/"skills").glob("*/SKILL.md"))),1)

    def test_claude_no_surprise_mcp_or_hooks(self):
        self.assertFalse((PLUGIN/".mcp.json").exists())
        self.assertFalse((PLUGIN/"mcp.json").exists())
        self.assertFalse((PLUGIN/"hooks").exists())

if __name__=="__main__":unittest.main()
