from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/analiza-prawna"
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")

class LightweightSkillContract(unittest.TestCase):
    def test_exactly_one_skill(self):
        self.assertEqual([p.parent.name for p in ROOT.glob("skills/*/SKILL.md")], ["analiza-prawna"])

    def test_frontmatter_and_broad_triggers(self):
        self.assertTrue(TEXT.startswith("---\n"))
        header = TEXT.split("---", 2)[1]
        self.assertIn("name: analiza-prawna", header)
        for word in ("KAŻDYM", "zadaniu prawnym", "przepisów", "orzecznictwa", "terminów", "zażaleń", "kontynuacje"):
            self.assertIn(word,header)

    def test_lean_instruction(self):
        self.assertLessEqual(len(TEXT.split()),350)

    def test_obligatory_process(self):
        for word in ("NAJPIERW", "POTEM", "ŁĄCZNIE", "Kontrola", "PASS/FAIL/NOT_CHECKED"):
            self.assertIn(word,TEXT)

    def test_case_reference_is_conditional(self):
        self.assertIn("wyłącznie gdy analiza dotyczy TK lub NC",TEXT)
        self.assertIn("Nie przenoś tego kanonu na niepowiązane sprawy",TEXT)

    def test_implicit_activation(self):
        yaml=(SKILL/"agents/openai.yaml").read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: true",yaml)

    def test_reference_paths(self):
        for file in re.findall(r"\]\(references/([^)]*)\)",TEXT):
            self.assertTrue((SKILL/"references"/file).exists(),file)
        self.assertEqual(sorted(p.name for p in (SKILL/"references").glob("*.md")),
                         ["audyt-dowodowy.md","kanon-tk-nc.md","prawo-polskie.md"])

    def test_chatgpt_no_local_executor(self):
        manifest=json.loads((ROOT/"plugin.json").read_text(encoding="utf-8"))
        compat=json.loads((ROOT/".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"],compat["version"])
        self.assertFalse((ROOT/"mcp.json").exists())
        self.assertFalse((ROOT/".mcp.json").exists())
        self.assertFalse(compat.get("requires_local_executor",False))
        self.assertNotIn("mcpServers",compat)
        self.assertEqual(manifest["extensions"]["com.openai"]["interface"]["displayName"],"Symetria Prawna")

if __name__=="__main__":unittest.main()
