# Copilot Working Notes (Phase 1: Planning only)

## What was inspected and why
- `.gitignore`: verify local hygiene (`.venv`, `.DS_Store`, local DB/media ignore patterns).
- `requirements.txt`: record dependency baseline before any upgrade decisions.
- `.venv/pyvenv.cfg`: capture actual local Python version in current environment.
- `.venv/.../django/__init__.py`: confirm currently installed Django version in local environment.
- Core Django project/app layout (`dttg_new/*`, `data/*`, `scripts/*`, `data/csv/*`): establish modernization risk map and phased order.

## Key findings
- Project is an older Django codebase with pinned baseline around Django 4.0.6.
- Local `.venv` exists and uses Python 3.12.4.
- `.gitignore` already ignores `.venv` and `.DS_Store`; current diff appears duplicate-line cleanup only.
- Data workflow depends on CSV + import/reset scripts; reset/erase scripts are destructive and must remain blocked until explicit approval.
- Deployment assumptions cannot be fully validated from repo-only access.

## Explicit non-goals in this phase
- No code/settings/template/script/CSV/migration edits.
- No dependency upgrades.
- No destructive script execution.
- No schema changes.

## Operational constraints
- Terminal execution is available, but shell utilities are limited in this environment (for example `curl`, `ps`, `pkill` were unavailable during smoke checks).
- Python-based probes remain reliable for non-destructive verification tasks.

## Planned immediate next step
- Upgrade-first checkpoint sequence is complete through Django 5.2.13 (including blocker-only `django-filter` compatibility update).
- Next step is post-checkpoint functional bug-fix tranche per plan, starting with confirmed artist pagination error reproduction/fix in a focused commit.
