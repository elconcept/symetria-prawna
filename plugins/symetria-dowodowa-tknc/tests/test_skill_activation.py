from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/analiza-dowodowa"
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")


class LightweightSkillContract(unittest.TestCase):
    def test_only_one_skill(self):
        self.assertEqual([p.parent.name for p in ROOT.glob("skills/*/SKILL.md")], ["analiza-dowodowa"])

    def test_frontmatter_and_trigger_coverage(self):
        self.assertTrue(TEXT.startswith("---\n"))
        header = TEXT.split("---", 2)[1]
        self.assertIn("name: analiza-dowodowa", header)
        for keyword in ("KAŻDYM", "prawnym", "dokumentacji", "przepisów", "orzecznictwa", "terminów", "zażaleń", "kontynuacje"):
            self.assertIn(keyword, header)

    def test_single_skill_token_budget(self):
        self.assertLessEqual(len(TEXT.split()), 350)

    def test_required_contract(self):
        for token in ("TK/NC", "Kontrbias", "Rzecznik", "samoocenę A–K", "NOT_CHECKED", "PASS"):
            self.assertIn(token, TEXT)

    def test_opt_in_implicit_activation(self):
        agent = (SKILL / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: true", agent)

    def test_selective_reference_links(self):
        for ref in re.findall(r"\]\(references/([^)]*)\)", TEXT):
            self.assertTrue((SKILL / "references" / ref).is_file(), ref)
        self.assertEqual(sorted(x.name for x in (SKILL/"references").glob("*.md")),
                         ["audyt.md", "kanon.md", "prawo-polskie.md"])

    def test_web_compatibility(self):
        manifest=json.loads((ROOT/"plugin.json").read_text(encoding="utf-8"))
        compat=json.loads((ROOT/".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], compat["version"])
        self.assertFalse((ROOT/"mcp.json").exists())
        self.assertFalse((ROOT/".mcp.json").exists())
        self.assertFalse(compat.get("requires_local_executor",False))
        self.assertNotIn("mcpServers",compat)


if __name__ == "__main__":
    unittest.main()
