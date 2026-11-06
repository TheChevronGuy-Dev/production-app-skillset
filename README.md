# Production App Skillset

A reusable AI coding skill built from 100 app-development rules, organized into ten pillars. Use it to scope, implement and review web/mobile applications without treating every technology as mandatory.

**Version:** 1.0.0 · **License:** MIT · **CLI:** Python 3.10+ standard library only

This is a skill and reference toolkit, not an application framework, automatic security scanner or compliance certification. It does not implement all controls for you. Its CLI generates checklists and validates recorded assessments; the coding assistant and developer perform the actual implementation and verification.

## Start here

1. Download and extract this repository.
2. Give your coding assistant `SKILL.md` and access to its referenced files.
3. Ask: **“Use this skill to review my app. Identify applicable rules, implement the authorized changes, and record verification evidence by rule ID.”**

For an assistant supporting folder-based skills, place the **complete repository contents** inside a folder named `build-production-apps` in that assistant's documented skill directory. `SKILL.md`, `data`, `references`, `scripts` and `agents` must remain together. Check the assistant's current installation instructions; discovery paths and invocation syntax vary. If no skills loader is available, point the assistant directly to `SKILL.md` as project context. No MCP server or API key is required for this package.

Do not install the whole package as a new application dependency. Keep it in a tools/documentation area or the assistant's skills folder. Avoid overwriting an existing `AGENTS.md`; see `examples/AGENTS.fragment.md` for an optional integration fragment.

## What is included

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Assistant workflow and module routing |
| `agents/openai.yaml` | Optional assistant UI metadata |
| `data/rules.json` | All 100 rules in machine-readable form |
| `references/` | Ten pillar guides, corrections, playbooks, extra safeguards and sources |
| `scripts/rules.py` | Offline search, checklist and assessment CLI |
| `tests/` | Behavioral tests for the toolkit |
| `.github/workflows/ci.yml` | GitHub Actions package checks |
| `examples/` | Sample prompts, assessment and agent integration |

Each rule has a stable ID (`R001`–`R100`), original number, pillar, type, applicability, implementation guidance and verification step. `control` means required **when applicable**. `decision` means a feature or architecture choice needs justification; omission can be correct.

## Run the tools

Run commands from the extracted repository root. On Windows, substitute `py -3` for `python3` if needed.

```bash
python3 scripts/rules.py validate
python3 scripts/rules.py list --query webhook
python3 scripts/rules.py checklist --profile ecommerce
python3 scripts/rules.py checklist --pillar security > security-checklist.md
python3 scripts/rules.py init --profile all > assessment.json
python3 scripts/rules.py review assessment.json
python3 scripts/rules.py review assessment.json --gate
python3 -m unittest discover -s tests -v
```

Redirection creates or replaces a file; choose a new filename to preserve existing work. `rules.py` only reads files and writes stdout/stderr. The maintenance command `render_references.py` rewrites the ten bundled pillar guides unless `--check` is used. They do not contact the network, modify the target app, install dependencies or read environment secrets.

Profiles: `all`, `web`, `saas`, `ecommerce`, `api`, `mobile`. They select broad groups, not exact applicability. `ecommerce` includes all ten pillars. Use `all` when completeness matters. A SaaS app with billing must add payment rules; a mobile app may also need checkout. Native mobile guidance is in `references/additional-safeguards.md` and is outside the numbered CLI gate.

## Record evidence honestly

Edit the generated assessment's `scope` to name the repository/revision/environment and reviewed features. For each rule choose:

| Status | Required supporting fields |
| --- | --- |
| `todo` | Work not assessed yet |
| `pass` | `evidence`: test command/result, reviewed path or manual observation |
| `fail` | Record finding and next action in `reason` |
| `not-applicable` | `reason`: why the condition does not apply |
| `deferred` | `reason`, `owner`, `review_by` |

`review` checks structure and supporting-field presence. `--gate` also rejects `todo`, `fail`, `deferred`, missing selected rules and unchanged scope placeholders. Exit codes: **0** validation succeeded, **1** assessment findings, **2** input/catalog error. A passing gate validates declarations, not their truth. It cannot verify application behavior, evidence quality, excluded modules or the additional safeguards. Review exceptions and evidence manually.

Do not publish filled assessments containing private vulnerabilities, secrets or customer data.

## Put this on GitHub

1. Create an empty GitHub repository, for example `production-app-skillset`.
2. Extract the ZIP and upload the **contents** of its top-level folder to the repository root. Include `.github` and `.gitignore` (some file browsers hide them).
3. Keep `LICENSE` to allow reuse under MIT. Change the display attribution if you prefer a different public author name.
4. Confirm the **Validate skill package** workflow passes. In repository settings, require it through a branch rule if desired; including a workflow does not automatically enforce merging rules.
5. Others can use **Code → Download ZIP**, clone the repository, or download a release asset. Add the ZIP to a release if you want a versioned download.

Optional command-line upload after creating an empty repository (replace the example owner/repository URL):

```bash
git init -b main
git add .
git commit -m "Add production app skillset"
git remote add origin https://github.com/YOUR-USERNAME/production-app-skillset.git
git push -u origin main
```

Do not run these initialization commands inside an unrelated existing repository. This distribution contains no Git history or account credentials. No public GitHub repository is created by the package itself.

## Maintain the catalog

Edit `data/rules.json`, preserve stable IDs and regenerate pillar references with `python3 scripts/render_references.py`. Run tests and validation before contributing. See `CONTRIBUTING.md` and `SECURITY.md`. Recheck source guidance when applying it to a specific stack; the links are reference points, not a perpetual freshness guarantee.
