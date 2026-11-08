import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_audit import validate_audit

FLAGS = ("performed", "counterbias_applied", "reviewed_final_draft",
         "institutional_authority_not_presumed", "hypothetical_defenses_removed", "visible_footer")

def sample(status="PASS"):
    return {"schema_version": "1.1", "audit_items": [
        {"code": c, "status": status, "source_available": True,
         "draft_excerpt": "fragment", "reason": "uzasadnienie", "repair": "korekta"}
        for c in "ABCDEFGHIJK"],
        "self_evaluation": {**{key: True for key in FLAGS}, "iterations": 1,
                            "final_verdict": status}}

class TestAuditContract(unittest.TestCase):
    def test_all_pass(self):
        self.assertTrue(validate_audit(sample())["passed"])
    def test_fail_blocks(self):
        a = sample(); a["audit_items"][2]["status"] = "FAIL"
        a["self_evaluation"]["final_verdict"] = "FAIL"
        self.assertFalse(validate_audit(a)["passed"])
        self.assertEqual(validate_audit(a)["failed_codes"], ["C"])
    def test_no_unchecked_as_pass(self):
        a = sample(); a["audit_items"][1]["source_available"] = False
        with self.assertRaises(ValueError): validate_audit(a)
    def test_no_empty_fail(self):
        a = sample(); a["audit_items"][0]["status"] = "FAIL"
        a["audit_items"][0]["repair"] = ""
        with self.assertRaises(ValueError): validate_audit(a)
    def test_no_missing_tests(self):
        a = sample(); a["audit_items"].pop()
        with self.assertRaises(ValueError): validate_audit(a)
    def test_counterbias_required(self):
        a = sample(); a["self_evaluation"]["counterbias_applied"] = False
        with self.assertRaises(ValueError): validate_audit(a)
    def test_footer_required(self):
        a = sample(); a["self_evaluation"]["visible_footer"] = False
        with self.assertRaises(ValueError): validate_audit(a)
    def test_not_checked_cannot_pass(self):
        a = sample(); a["audit_items"][1]["status"] = "NOT_CHECKED"
        a["self_evaluation"]["final_verdict"] = "NOT_CHECKED"
        self.assertEqual(validate_audit(a)["verdict"], "NOT_CHECKED")
        self.assertFalse(validate_audit(a)["passed"])
    def test_unchecked_false_pass_rejected(self):
        a = sample(); a["audit_items"][1]["status"] = "NOT_CHECKED"
        with self.assertRaises(ValueError): validate_audit(a)
    def test_missing_self_eval_rejected(self):
        a = sample(); del a["self_evaluation"]
        with self.assertRaises(ValueError): validate_audit(a)
    def test_iteration_nonpositive_rejected(self):
        a = sample(); a["self_evaluation"]["iterations"] = 0
        with self.assertRaises(ValueError): validate_audit(a)

if __name__ == "__main__": unittest.main()
