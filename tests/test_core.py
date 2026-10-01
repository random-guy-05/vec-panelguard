from vec_panelguard.core import audit_genes


def test_exact():
    report = audit_genes(["a", "b", "c"], ["a", "b", "c"])
    assert report.status == "EXACT_MATCH"


def test_reorderable():
    report = audit_genes(["c", "a", "b"], ["a", "b", "c"])
    assert report.status == "SAME_SET_WRONG_ORDER"
    assert report.reorder_index == [1, 2, 0]


def test_missing_extra():
    report = audit_genes(["a", "x"], ["a", "b"])
    assert report.status == "INCOMPATIBLE_GENE_SET"
    assert report.missing == ["b"]
    assert report.extra == ["x"]


def test_duplicates_not_safely_repairable():
    report = audit_genes(["a", "a"], ["a", "b"])
    assert report.status == "INCOMPATIBLE_GENE_SET"
    assert report.duplicates_received == ["a"]
