from pathlib import Path
import unittest
import json

REPO=Path(__file__).resolve().parents[3]
PLUGIN=REPO/"plugins/symetria-dowodowa-tknc"

class ClaudeCodePackage(unittest.TestCase):
    def test_marketplace_skill_plugin_and_hooks_plugin(self):
        market=json.loads((REPO/".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual([x["name"] for x in market["plugins"]],["symetria-prawna","symetria-prawna-hooki"])
        self.assertEqual(market["plugins"][1]["source"],"./plugins/symetria-prawna-hooki")
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

    def test_skill_plugin_has_no_local_executor(self):
        # Hooki są w osobnym pluginie symetria-prawna-hooki; ten katalog instaluje też ChatGPT web.
        self.assertFalse((PLUGIN/".mcp.json").exists())
        self.assertFalse((PLUGIN/"mcp.json").exists())
        self.assertFalse((PLUGIN/"hooks").exists())
        self.assertNotIn("hooks",json.loads((PLUGIN/".claude-plugin/plugin.json").read_text(encoding="utf-8")))

if __name__=="__main__":unittest.main()
