"""Private local stdio MCP server, launched on demand by uvx.

No network access, storage or telemetry from this server. An LLM is not launched
by this implementation: the citizen advocate is a deterministic challenge tool.
"""
from __future__ import annotations
from mcp.server.fastmcp import FastMCP
from .core import as_list, quote_check, risks, advocate_review, validate_audit, digest
import json

server=FastMCP('symetria-dowodowa-tknc')

def decode_object(s:str) -> dict:
    x=json.loads(s)
    if not isinstance(x,dict):raise ValueError('Expected object')
    return x

@server.tool()
def flag_asymmetry(draft:str)->dict:
    """Find *possible* invented official defenses, official-document privilege and disproportionate discrepancies. Risk flags are NOT verdicts."""
    return {'draft_sha256':digest(draft), 'risk_flags':risks(draft), 'semantic_verified':False}

@server.tool()
def verify_quote(quote:str, source_id:str, sources_json:str)->dict:
    """Check whether the quoted text literally occurs in a supplied source; no external access."""
    return quote_check(quote,source_id,as_list(sources_json))

@server.tool()
def rzecznik_obywatela(draft:str, claims_json:str='[]')->dict:
    """Adversarial citizen-rights challenge, checks for speculative official defenses. A rules-based consult, NOT an independent LLM."""
    return advocate_review(draft,as_list(claims_json))

@server.tool()
def gate_response(draft:str,audit_json:str,rzecznik_receipt_json:str)->dict:
    """Fail-closed structural gate for draft-bound A-K self-evaluation and Rzecznik receipt; does not certify semantic truth."""
    return validate_audit(decode_object(audit_json),draft,decode_object(rzecznik_receipt_json))

def main():
    server.run(transport='stdio')

if __name__=='__main__':main()
