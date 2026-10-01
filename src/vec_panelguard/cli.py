from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import audit_genes, read_panel


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description='Audit/repair VEC gene-panel order.')
    p.add_argument('file', type=Path)
    p.add_argument('--panel', required=True, type=Path)
    p.add_argument('--fix', type=Path)
    p.add_argument('--json', type=Path, dest='json_path')
    args = p.parse_args(argv)
    import anndata as ad
    expected = read_panel(args.panel)
    a = ad.read_h5ad(args.file)
    report = audit_genes(a.var_names, expected)
    print(report.status)
    print(f'expected={report.expected_count} received={report.received_count}')
    if report.missing:
        print('missing:', ', '.join(report.missing[:20]))
    if report.extra:
        print('extra:', ', '.join(report.extra[:20]))
    if args.json_path:
        args.json_path.write_text(json.dumps(report.to_dict(), indent=2) + '\n')
    if args.fix:
        if report.status == 'EXACT_MATCH':
            args.fix.parent.mkdir(parents=True, exist_ok=True)
            a.write_h5ad(args.fix)
        elif report.status == 'SAME_SET_WRONG_ORDER':
            fixed = a[:, report.reorder_index].copy()
            fixed.var_names = expected
            args.fix.parent.mkdir(parents=True, exist_ok=True)
            fixed.write_h5ad(args.fix)
            check = audit_genes(fixed.var_names, expected)
            if check.status != 'EXACT_MATCH':
                args.fix.unlink(missing_ok=True)
                print('ERROR: post-write audit failed')
                return 2
        else:
            print('ERROR: incompatible set; refusing to invent/drop genes')
            return 2
        print(f'wrote {args.fix}')
    return 0 if report.status == 'EXACT_MATCH' else 3 if report.status == 'SAME_SET_WRONG_ORDER' else 4
