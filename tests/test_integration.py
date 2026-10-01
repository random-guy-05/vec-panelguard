import subprocess
import sys

import anndata as ad
import numpy as np
import pandas as pd


def test_cli_repairs_gene_order_and_expression_columns(tmp_path):
    source = tmp_path / "source.h5ad"
    repaired = tmp_path / "repaired.h5ad"
    panel = tmp_path / "panel.txt"

    # Received genes are c,a,b and expression columns encode that order.
    matrix = np.array(
        [
            [30.0, 10.0, 20.0],
            [300.0, 100.0, 200.0],
        ],
        dtype=np.float32,
    )
    data = ad.AnnData(
        X=matrix,
        var=pd.DataFrame(index=["c", "a", "b"]),
    )
    data.write_h5ad(source)
    panel.write_text("a\nb\nc\n")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "vec_panelguard.cli",
            str(source),
            "--panel",
            str(panel),
            "--fix",
            str(repaired),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    fixed = ad.read_h5ad(repaired)
    assert list(fixed.var_names) == ["a", "b", "c"]
    np.testing.assert_allclose(
        np.asarray(fixed.X),
        np.array(
            [
                [10.0, 20.0, 30.0],
                [100.0, 200.0, 300.0],
            ],
            dtype=np.float32,
        ),
    )


def test_incompatible_set_refuses_fix(tmp_path):
    source = tmp_path / "source.h5ad"
    repaired = tmp_path / "repaired.h5ad"
    panel = tmp_path / "panel.txt"

    ad.AnnData(
        X=np.ones((2, 2), dtype=np.float32),
        var=pd.DataFrame(index=["a", "x"]),
    ).write_h5ad(source)
    panel.write_text("a\nb\n")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "vec_panelguard.cli",
            str(source),
            "--panel",
            str(panel),
            "--fix",
            str(repaired),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 4
    assert not repaired.exists()
