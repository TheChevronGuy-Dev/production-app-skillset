# Contributing

Keep the catalog useful to both humans and coding assistants. Propose a concrete behavior change, applicability condition and verification method. Preserve R001–R100 IDs; record broader additions separately until a deliberate catalog version change.

1. Edit the canonical JSON and relevant playbooks or skill instructions.
2. Regenerate: `python3 scripts/render_references.py`.
3. Run `python3 scripts/rules.py validate`, `python3 scripts/render_references.py --check` and `python3 -m unittest discover -s tests -v`.
4. Explain changes and test results in the pull request. Link primary documentation for technical corrections.

Never add real credentials, production data, completed private assessments, copied proprietary guides or claims that passing this toolkit certifies a product. Keep the CLI offline and dependency-free. Review public instructions for platform-specific assumptions. Add regression tests when changing CLI behavior.
