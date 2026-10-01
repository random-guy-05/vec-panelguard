# VEC PanelGuard

A focused tool for one of the easiest VEC mistakes to make: **the right genes in the wrong order are still a rejected submission**.

PanelGuard compares an H5AD's `var_names` to an official board panel text file downloaded from the Challenge Data page. If the set is identical but the order differs, it can create a repaired copy by reindexing expression columns. It never invents missing genes or silently drops extras.

## Usage

```bash
vec-panelguard prediction.h5ad --panel T2__heart__val_interp.genes.txt

# Same set, wrong order? Write a repaired copy:
vec-panelguard prediction.h5ad \
  --panel T2__heart__val_interp.genes.txt \
  --fix prediction_ordered.h5ad
```

Output distinguishes:

- `EXACT_MATCH`
- `SAME_SET_WRONG_ORDER`
- `INCOMPATIBLE_GENE_SET`
- duplicate gene names

The repair preserves all rows and AnnData metadata while reordering the gene axis. Run the official validator after repair.

## Why separate from a general validator?

This tool is intentionally narrow and **actionable**: not only "gene order is wrong", but "the set is exactly repairable" and a safe repaired file. It uses the official panel file you downloaded, so it does not ship a stale private copy of gene names.
