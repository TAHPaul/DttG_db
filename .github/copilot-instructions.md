# Copilot Instructions for DttG_db

## Current workflow priority
1. Repository hygiene + planning docs.
2. Local baseline verification using existing `.venv`.
3. Run project as-is.
4. Security/settings hardening (controlled).
5. Staged Django upgrade.

## Hard constraints
- Do not edit migrations or create migrations unless explicitly approved.
- Do not change DB schema unless explicitly approved.
- Do not run destructive scripts (`scripts/reset_*`, `scripts/erase_database.py`) unless explicitly approved.
- Do not edit CSV files unless explicitly approved.
- Do not upgrade dependencies before baseline checks are recorded.

## Change discipline
- Use atomic commits per subtask.
- If a task is risky, create a temporary sub-branch before implementation.
- Keep `docs/work_log.md` concise and client-readable.
- Explain intended files before editing in later phases.

## Local environment
- `.venv/` exists and is local-only.
- Never commit `.venv/`.
- Verify baseline with non-destructive commands before implementation changes.

## Validation expectations
- Preferred baseline checks:
  - `python --version`
  - `python -m django --version`
  - `python -m pip freeze`
  - `python manage.py check`
- If `manage.py check` fails, document errors first; do not rush into broad fixes.

## Deployment caveat
Treat the live site as behavioural reference only. Do not assume production access, logs, DB, or deployment control unless explicitly provided.
