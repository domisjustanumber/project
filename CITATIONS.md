# Workspace source provenance

The outer workspace owns citations for workspace tooling and agent guidance.
Independent checkouts own their own bibliographies; the workspace checker skips
`repos/`, legacy checkouts, local agent configuration, and generated artifacts.

Use braced Better BibTeX-compatible entries in root `references.bib`, with stable
keys, title, author/editor, URL, access date (`urldate`), `review`, and `claim`.
Allowed review scopes are metadata, abstract, excerpt, full-text and source-code.
For limited review include a `note` explaining exactly what was inspected. Omit
unknown publication metadata. Cite keys beside supported claims with bracketed
`@key` markers; these are provenance markers, not a rendering integration.

Run `python -B tools/check_references.py` and
`python -B -m unittest discover -s tools -p test_references.py -v`.
The validator and in-memory tests are adapted from Core's existing validator;
they check syntax and attribution consistency, not whether a claim is true.
