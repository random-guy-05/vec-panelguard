from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PanelAudit:
    status: str
    expected_count: int
    received_count: int
    missing: list[str]
    extra: list[str]
    duplicates_expected: list[str]
    duplicates_received: list[str]
    reorder_index: list[int] | None

    def to_dict(self):
        return asdict(self)


def duplicates(values):
    return sorted(k for k, n in Counter(values).items() if n > 1)


def audit_genes(received, expected) -> PanelAudit:
    rec = [str(x) for x in received]
    exp = [str(x) for x in expected]
    de = duplicates(exp)
    dr = duplicates(rec)
    missing = sorted(set(exp) - set(rec))
    extra = sorted(set(rec) - set(exp))
    reorder = None
    if rec == exp and not de and not dr:
        status = 'EXACT_MATCH'
        reorder = list(range(len(exp)))
    elif len(rec) == len(exp) and not missing and not extra and not de and not dr:
        status = 'SAME_SET_WRONG_ORDER'
        pos = {g: i for i, g in enumerate(rec)}
        reorder = [pos[g] for g in exp]
    else:
        status = 'INCOMPATIBLE_GENE_SET'
    return PanelAudit(status, len(exp), len(rec), missing, extra, de, dr, reorder)


def read_panel(path):
    lines = [line.strip() for line in open(path, encoding='utf-8') if line.strip()]
    if not lines:
        raise ValueEror('panel file is empty')
    return lines
