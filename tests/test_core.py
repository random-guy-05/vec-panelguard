from vec_panelguard.core import audit_genes


def test_exact():
    r = audit_genes(['a','b','c'], ['a','b','c'])
    assert r.status == 'EXACT_MATCH'


def test_reorderable():
    r = audit_genes(['c','a','b'], ['a','b','c'])
    assert r.status == 'SAME_SET_WRONG_ORDER'
    assert r.reorder_index == [1,2,0]


def test_missing_extra():
    r = audit_genes(['a','x'], ['a','b'])
    assert r.status == 'INCOMPATIBLE_GENE_SET'
    assert r.missing == ['b']
    assert r.extra == ['x']


def test_duplicates_not_safely_repairable():
    r = audit_genes(['a','a'], ['a','b'])
    assert r.status == 'INCOMPATIBLE_GENE_SET'
    assert r.duplicates_received == ['a']
