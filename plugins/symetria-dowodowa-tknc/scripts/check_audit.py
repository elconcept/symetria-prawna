#!/usr/bin/env python3
"""Weryfikacja mechaniczna kontraktu audytu 1.1; NIE ocena semantyczna ani hook."""
import json
import sys
from pathlib import Path

CODES = set("ABCDEFGHIJK")
STATUSES = {"PASS", "FAIL", "NOT_CHECKED"}
REQUIRED_FLAGS = ("performed", "counterbias_applied", "reviewed_final_draft",
                  "institutional_authority_not_presumed", "hypothetical_defenses_removed", "visible_footer")

def validate_audit(data):
    if not isinstance(data, dict):
        raise ValueError("Audit must be a JSON object")
    if data.get("schema_version") != "1.1":
        raise ValueError("Unsupported schema_version; use 1.1")
    items = data.get("audit_items")
    if not isinstance(items, list) or len(items) != 11:
        raise ValueError("Must supply eleven audit_items (A-K)")
    seen = set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Audit item must be an object")
        code, status = item.get("code"), item.get("status")
        if code not in CODES or code in seen:
            raise ValueError("Invalid/duplicate code")
        seen.add(code)
        if status not in STATUSES:
            raise ValueError("Invalid status")
        if status == "FAIL":
            for key in ("draft_excerpt", "reason", "repair"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    raise ValueError(f"FAIL {code} lacks {key}")
        if status == "PASS" and item.get("source_available") is False:
            raise ValueError(f"PASS {code} without source verification")
        if status == "NOT_CHECKED" and not item.get("reason"):
            raise ValueError(f"NOT_CHECKED {code} lacks reason")
    if seen != CODES:
        raise ValueError("Some codes missing")
    audit = data.get("self_evaluation")
    if not isinstance(audit, dict):
        raise ValueError("self_evaluation is mandatory")
    for key in REQUIRED_FLAGS:
        if audit.get(key) is not True:
            raise ValueError(f"Missing or false self_evaluation.{key}")
    iterations = audit.get("iterations")
    if not isinstance(iterations, int) or isinstance(iterations, bool) or iterations < 1:
        raise ValueError("self_evaluation.iterations must be positive integer")
    fails = [i["code"] for i in items if i["status"] == "FAIL"]
    unchecked = [i["code"] for i in items if i["status"] == "NOT_CHECKED"]
    verdict = "FAIL" if fails else "NOT_CHECKED" if unchecked else "PASS"
    if audit.get("final_verdict") != verdict:
        raise ValueError("self_evaluation.final_verdict inconsistent with audit items")
    return {"passed": verdict == "PASS", "verdict": verdict,
            "failed_codes": fails, "not_checked_codes": unchecked,
            "self_evaluation_declared": True}

def main():
    obj = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(validate_audit(obj), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
