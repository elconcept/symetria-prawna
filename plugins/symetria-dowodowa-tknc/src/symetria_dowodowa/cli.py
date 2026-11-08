"""CLI for local draft audits without MCP client or remote services."""
import argparse,json,sys
from pathlib import Path
from .core import advocate_review,validate_audit,risks,digest

def main():
    p=argparse.ArgumentParser(description='Offline TK/NC draft audit checks')
    sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('screen');a.add_argument('draft',help='UTF-8 text file')
    a=sub.add_parser('rzecznik');a.add_argument('draft')
    a=sub.add_parser('gate');a.add_argument('draft');a.add_argument('audit');a.add_argument('receipt')
    x=p.parse_args();draft=Path(x.draft).read_text(encoding='utf-8')
    if x.cmd=='screen':result={'draft_sha256':digest(draft),'risk_flags':risks(draft)}
    elif x.cmd=='rzecznik':result=advocate_review(draft)
    else:
        result=validate_audit(json.loads(Path(x.audit).read_text(encoding='utf-8')),draft,json.loads(Path(x.receipt).read_text(encoding='utf-8')))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if x.cmd=='gate' and result['status']!='PASS':sys.exit(2)
if __name__=='__main__':main()
