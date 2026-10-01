from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import audit_genes, read_panel


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit/repair VEC gene-panel order."
    )
    parser.add_argument("file", type=Path)
    parser.add_argument("--panel", required=True, type=Path)
    parser.add_argument("--fix", type=Path)
    parser.add_argument("--json", type=Path, dest="json_path")
    args = parser.parse_args(argv)

    import anndata as ad

    expected = read_panel(args.panel)
    data = ad.read_h5ad(args.file)
    report = audit_genes(data.var_names, expected)

    print(report.status)
    print(
        f"expected={report.expected_count} "
        f"received={report.received_count}"
    )
    if report.missing:
        print("missing:", ", ".join(report.missing[:20]))
    if report.extra:
        print("extra:", ", ".join(report.extra[:20]))

    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(
            json.dumps(report.to_dict(), indent=2) + "\n",
            encoding="utf-8",
        )

    if args.fix:
        if report.status == "EXACT_MATCH":
            fixed = data.copy()
        elif report.status == "SAME_SET_WRONG_ORDER":
            fixed = data[:, report.reorder_index].copy()
            fixed.var_names = expected
        else:
            print("ERROR: incompatible set; refusing to invent/drop genes")
            return 4

        args.fix.parent.mkdir(parents=True, exist_ok=True)
        fixed.write_h5ad(args.fix)
        check = ad.read_h5ad(args.fix)
        post = audit_genes(check.var_names, expected)
        if post.status != "EXACT_MATCH":
            args.fix.unlink(missing_ok=True)
            print("ERROR: post-write audit failed")
            return 2
        print(f"wrote {args.fix}")
        return 0

    if report.status == "EXACT_MATCH":
        return 0
    if report.status == "SAME_SET_WRONG_ORDER":
        return 3
    return 4


if __name__ == "__main__":
    raise SystemExit(main())
