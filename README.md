# Production App Skillset

Turn an app or website idea into a scoped build, a working user journey and a verified deployment handoff with your coding assistant. Designed for absolute beginners and experienced developers, this skill supports HTTP/HTTPS websites, APIs, Android and iOS apps. It combines 100 development rules with practical guides for accounts, payments, mailing lists and optional private encrypted content.

**Version:** 1.1.0 (catalog 1.0.0) · **License:** MIT · **CLI:** Python 3.10+ standard library only

This package guides a coding assistant that can edit and run your application. Its offline CLI creates plans and checks recorded evidence; it does not itself generate a runnable app, provision hosting or independently verify security. The assistant implements the selected features in your project, tests them, and reports what still needs attention. Hosting accounts, domains, service fees and native signing remain project-specific decisions.

## Start here

1. Download and extract this repository.
2. Give your coding assistant `SKILL.md` and access to its referenced files.
3. Describe your idea using the beginner or experienced-builder prompt below. Your assistant should start with the smallest useful working journey and explain how to try it.

For an assistant supporting folder-based skills, place the **complete repository contents** inside a folder named `build-production-apps` in that assistant's documented skill directory. `SKILL.md`, `data`, `references`, `scripts` and `agents` must remain together. Check the assistant's current installation instructions; discovery paths and invocation syntax vary. If no skills loader is available, point the assistant directly to `SKILL.md` as project context. No MCP server or API key is required for this package.

Do not install the whole package as a new application dependency. Keep it in a tools/documentation area or the assistant's skills folder. Avoid overwriting an existing `AGENTS.md`; see `examples/AGENTS.fragment.md` for an optional integration fragment.

## Start with your idea

**New to coding?** Copy this into an assistant with access to the skill:

> Use $build-production-apps to help me build [my idea] for [the people it helps]. I am a beginner. Help me choose a small first version, explain important decisions simply, build a working journey, and guide me through testing and hosting. Track anything that is still simulated or unverified.

**Already have a stack or app?**

> Use $build-production-apps in this repository. Preserve our conventions, implement [scope], record relevant rule and launch-check evidence, and prepare a reproducible deployment handoff. Flag consequential architecture or operating-cost decisions.

For an assistant without skill invocation syntax, say “Read SKILL.md and use this skill” instead. No specific assistant brand or hosting vendor is required.

## Create a project plan

Python 3.10+ is needed only for the optional CLI. Run from the skill repository (on Windows use `py -3` if available, or the full path to an installed Python):

```bash
python3 scripts/launch.py init --name "My useful idea" --platform web --feature accounts --feature mailing-list --output my-idea-plan
```

The output must be a **new directory**. This creates `brief.md`, `plan.md`, selected `guides/`, `launch.json`, and a complete 100-rule `assessment.json`. It does not overwrite existing work or create a runnable app. Give the brief and plan to your coding assistant and ask it to implement the first journey in your chosen app repository. Planning files can live in a separate documentation directory; keep filled reviews private.

Platforms: `web`, `api`, `android`, `ios`. Repeat `--platform` for multiple targets. Optional features: `accounts`, `payments`, `mailing-list`, `e2ee`. Omit features you do not need. Android and iOS each get their own required declaration entry when selected.

```bash
python3 scripts/launch.py review my-idea-plan/launch.json
python3 scripts/launch.py review my-idea-plan/launch.json --gate --format json
```

Edit both generated JSON files as implementation progresses. Use `todo`, `pass` with evidence, `fail` with reason, `not-applicable` with reason, or `deferred` with reason/owner/date. Replace scope placeholders with repository, revision and environment. The launch gate rejects unresolved or missing checks and also reviews the sibling `assessment.json` using the full `all` profile; use `--assessment PATH` if it has moved. Dates use `YYYY-MM-DD`. Exit codes are 0 for valid declarations, 1 for findings and 2 for input errors. JSON output applies to parsed review results; input errors use stderr. Evidence truth and excluded scope still require review.

## What your assistant should deliver

A working app for the agreed scope, with actual verification evidence, source and reproducible setup/build instructions, configuration names without secrets, deployment/export instructions, and an owner-readable recovery/maintenance runbook. Native apps need platform signing/distribution; a static site export cannot replace a backend or mobile build. Begin with a preview and verify the deployed journey before calling a release complete.

## What is included

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Assistant workflow and module routing |
| `agents/openai.yaml` | Optional assistant UI metadata |
| `data/rules.json` | All 100 rules in machine-readable form |
| `references/` | Ten pillar guides, corrections, playbooks, extra safeguards and sources |
| `scripts/rules.py` | Offline search, checklist and assessment CLI |
| `scripts/launch.py` | New-project planning and combined launch declaration gate |
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
python3 scripts/rules.py review assessment.json --gate --format json
python3 -m unittest discover -s tests -v
```

Redirection creates or replaces a file; choose a new filename to preserve existing work. `rules.py` only reads files and writes stdout/stderr. The maintenance command `render_references.py` rewrites the ten bundled pillar guides unless `--check` is used. They do not contact the network, modify the target app, install dependencies or read environment secrets.

Profiles: `all`, `web`, `saas`, `ecommerce`, `api`, `mobile`. They select broad groups, not exact applicability. `ecommerce` includes all ten pillars. Use `all` when completeness matters. A SaaS app with billing must add payment rules; a mobile app may also need checkout. Use `references/platform-security.md` for dedicated web/API, Android, iOS and hybrid security/usability checks, plus `references/additional-safeguards.md` for broader gaps. The numbered CLI gate does not cover these guides. The launch planner adds selected feature/platform declaration checks; review the full guides as well, since the summaries are not exhaustive. A profile is not a complete platform audit.

## Record evidence honestly

Edit the generated assessment's `scope` to name the repository/revision/environment and reviewed features. For each rule choose:

| Status | Required supporting fields |
| --- | --- |
| `todo` | Work not assessed yet |
| `pass` | `evidence`: test command/result, reviewed path or manual observation |
| `fail` | Record finding and next action in `reason` |
| `not-applicable` | `reason`: why the condition does not apply |
| `deferred` | `reason`, `owner`, `review_by` (valid `YYYY-MM-DD`) |

`review` checks structure and supporting-field presence, including a nonblank reason for failures and a valid calendar date for deferrals. It accepts UTF-8 assessment files with or without a Windows BOM. `--format json` returns valid/gate/errors/evidence_verified fields for parsed assessments; input/catalog errors still use stderr and exit code 2. Dates record review commitments; the CLI does not enforce scheduling or reminders. `--gate` also rejects `todo`, `fail`, `deferred`, missing selected rules and unchanged scope placeholders. Exit codes: **0** validation succeeded, **1** assessment findings, **2** input/catalog error. A passing gate validates declarations, not their truth. It cannot verify application behavior, evidence quality, excluded modules or the additional safeguards. Review exceptions and evidence manually.

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

## Changes in 1.0.1

Fixed missing failure-rationale validation; added deferred-date validation, JSON assessment-review output and Windows UTF-8 BOM input support. Added platform security/usability guidance and explicit build-verification instructions. Rule IDs, catalog version and assessment schema remain unchanged. Existing failed entries without reasons must now be completed.

## Changes in 1.1.0

Added beginner/pro workflows, six implementation and handoff guides, a project-plan generator and a combined launch declaration gate. Selected features receive dedicated checks, and each chosen platform is recorded. The original R001-R100 catalog, catalog version and assessment schema remain unchanged. Existing 1.0.x assessments continue to work with `rules.py`; the new launch gate requires an `all` assessment. Creating a new plan never overwrites an existing directory.
