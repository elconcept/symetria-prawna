import json
import re
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
SKILL=(ROOT/"skills/analiza-prawna/SKILL.md").read_text(encoding="utf-8")
AUDIT=(ROOT/"skills/analiza-prawna/references/audyt-dowodowy.md").read_text(encoding="utf-8")
FIXTURES=json.loads((ROOT.parent.parent/"fixtures/regression_symmetry.json").read_text(encoding="utf-8"))["cases"]

class RecentFailureProtocol(unittest.TestCase):
    def test_order_is_explicit(self):
        self.assertLess(SKILL.index("**NAJPIERW**"),SKILL.index("**POTEM**"))
        for phrase in ("podstawy twierdzeń obciążających","niezależne potwierdzenie","**ŁĄCZNIE**","A–K"):
            self.assertIn(phrase,SKILL)
    def test_failure_conditions_are_mandatory(self):
        for phrase in ("D=FAIL","H=FAIL","**O — obciążające twierdzenie:**","**P — porównanie:**","**S — synergia:**"):
            self.assertIn(phrase,AUDIT)
        self.assertIn("zawiadomienie o przestępstwie",AUDIT)
    def test_cases_have_grounded_corrective_actions(self):
        self.assertGreaterEqual(len(FIXTURES),7)
        ids={i["id"] for i in FIXTURES}
        for name in ("TK_ACCUSATION_FIRST","CUMULATIVE_MATERIAL","INVENTED_BENIGN_EXCUSE","NOTIFICATION_IS_NOT_CONVICTION"):
            self.assertIn(name,ids)
        for case in FIXTURES:
            self.assertTrue(case["prompt"] and case["bad_answer"] and case["required_action"])
            self.assertTrue(set(case["expected_codes"])<=set("ABCDEFGHIJK"))
    def test_review_flag_for_isolated_intent(self):
        from symetria_dowodowa.core import risks
        flags=risks("Zmodyfikowany plik sam w sobie nie dowodzi zamiaru.")
        self.assertIn("isolated_intent_dismissal",{f["code"] for f in flags})
        self.assertNotIn("isolated_intent_dismissal",{f["code"] for f in risks("Zbadano łączną moc świadectw i chronologię.")})

if __name__=="__main__": unittest.main()
