# Community Contribution submission text

## Title
VEC PanelGuard — safely audit and repair gene-panel order

## Description
PanelGuard compares a prediction H5AD's `var_names` against an official VEC panel text file. It distinguishes an exact match from the common "same genes, wrong order" case and from genuinely incompatible missing/extra/duplicate genes. When the set is exactly repairable it can write a new H5AD with expression columns reindexed to the official order, without inventing or dropping genes. This turns a common portal rejection into a one-command deterministic repair while keeping the official Data-page panel file as the source of truth.
