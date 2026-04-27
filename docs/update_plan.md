# Update Plan — DttG_db (Conservative, staged)

## Scope and guardrails (current phase)
- Planning/docs only.
- Do not edit app code, settings, templates, scripts, CSVs, migrations, or `requirements.txt` yet.
- Do not create/alter migrations.
- Do not run destructive reset/import scripts.
- Treat CSV files as source of truth, but do not edit CSVs in this phase.
- Treat live site as behavioural/content reference only.

## Practical execution order (agreed)
1. Repository hygiene and planning docs.
2. Reproducible local environment notes (`.venv` already exists).
3. Run current project locally as-is and record baseline behaviour.
4. Plan/implement settings & security hardening (controlled, reversible).
5. Plan/implement staged Django upgrade.

## Status snapshot (2026-04-27)
- Phase 1 (repository hygiene + planning docs): completed.
- Phase 2A (local baseline commands): completed.
- Phase 2B (run-as-is smoke checklist): completed.
- Phase 3 (settings hardening): completed — env-driven config, CSRF trusted origins, `.env.example`, `.gitignore` updated.
- Django 4.2 upgrade checkpoint: completed (`4.2.30`).
- Django 5.2 upgrade checkpoint: completed (`5.2.13`, blocker-only `django-filter` fix).
- Dependency audit: completed — removed unused `django-htmx` and `django-extensions`.
- Phase 5 bug fixes: completed — artist pagination crash, artists-without-artworks filter, museum city/country display, museum website link guard.
- User/auth reset: completed — legacy accounts deleted, new superuser and staff accounts created.
- **Pending (local code complete):** RKD IT officer to set env vars on server and run `manage.py check --deploy` (see "Open question for RKD IT officer" section below).
- **Next optional work:** Phase 6 (CSV import workflow), Phase 7 (content/UI updates).

## Phase plan and dependencies

### Phase 1 — Repository review & safety baseline (P0)
**Depends on:** none  
**Output:** planning docs, risk baseline, scope limits.

- Confirm git branch/state and current local changes.
- Confirm `.gitignore` coverage for local-only files.
- Record what must never be committed.
- Capture baseline architecture and known hotspots.

### Phase 2 — Local baseline verification (P0)
**Depends on:** Phase 1 complete  
**Output:** reproducible local run notes and baseline checks.

- `.venv` exists locally; verify it remains ignored by git.
- Capture current runtime/dependency baseline from repo + local environment evidence.
- Run non-destructive checks:
  - `python --version`
  - `python -m django --version`
  - `python -m pip freeze`
  - `python manage.py check`
- Start app locally and verify core routes as-is (no code changes).

#### Phase 2A — Command baseline (required before any hardening)
- Capture and record exact outputs for:
  - `python --version`
  - `python -m django --version`
  - `python -m pip freeze`
  - `python manage.py check`
- If `manage.py check` returns errors, log them first; do not apply broad fixes yet.

#### Phase 2B — Run-as-is smoke checklist (no implementation edits)
- `python manage.py runserver`
- Verify pages load without code changes:
  - `/` (home)
  - `/about/`
  - `/artists/`
  - `/entries/`
  - `/entries-table-simple/`
  - `/entries-table-adv/`
  - `/museums/`
  - `/city-of-execution/`
  - `/dttg-login/`
- Record any tracebacks or visible UI issues in `docs/work_log.md` before changing code.

### Phase 3 — Security/config hardening plan (P1)
**Depends on:** project runs locally as-is  
**Output:** controlled hardening tasks (not executed yet in this phase).

- Move secret/debug/host controls toward environment-based configuration.
- Review static/media/deployment assumptions.
- Preserve local developer ergonomics while introducing safe defaults.
- Add deployment caveat: final behaviour requires production access/instructions to verify.

#### Phase 3A — Hardening inventory (planning only)
- Catalogue current settings risk points in `dttg_new/settings.py`:
  - hardcoded `SECRET_KEY`
  - `DEBUG=True`
  - `ALLOWED_HOSTS=[]`
  - static/media assumptions for local vs deployed runtime
- Identify all settings that should become environment-driven vs safe local defaults.
- Document what is explicitly out-of-scope until later approval (no deployment-only changes that cannot be tested locally).

Current inventory snapshot (confirmed):
- `SECRET_KEY` is hardcoded in source.
- `DEBUG` is enabled by default.
- `ALLOWED_HOSTS` is empty.
- Database defaults to sqlite file `BASE_DIR / 'db.sqlite3'`.
- Media serving is conditionally appended in `dttg_new/urls.py` only when `DEBUG` is true.
- No `.env` loading/helper is currently configured in project settings.

#### Phase 3B — Target configuration model (planning only)
- Define planned configuration split and precedence:
  - base defaults (local-safe)
  - environment override layer
  - explicit production-only requirements checklist
- Define required environment variables (approved set):
  - `DJANGO_SECRET_KEY`
  - `DJANGO_DEBUG`
  - `DJANGO_ALLOWED_HOSTS`
  - `DJANGO_CSRF_TRUSTED_ORIGINS` (document now, implement later)
  - `DJANGO_STATIC_ROOT`
  - `DJANGO_MEDIA_ROOT`
- Define fallback behaviour so local development remains runnable without production secrets.

Approved parsing policy:
- Multi-value settings use comma-separated strings.
- Boolean settings use `True` / `False` string values.
- Never commit real secrets; use placeholders in documentation only.

#### Phase 3C — Rollout sequence (implementation phase later)
- Step 1: introduce env reads with backward-compatible defaults.
- Step 2: switch sensitive defaults off for production mode only.
- Step 3: run local checks (`manage.py check`) and smoke routes.
- Step 4: document deployment caveat and unresolved production-only validation items.
- Step 5: only then proceed to staged dependency/framework upgrade.

Important timing constraint:
- Security header implementation (CSP, iframe/X-Frame-Options policy, CSRF trusted origins enforcement, SSL/HSTS redirects) is deferred until after Django 4.2 and 5.2 checkpoints are working locally.

#### Phase 3D — Hardening acceptance criteria
- Local app still runs with `.venv` and current DB/media setup.
- No migration or schema impact.
- No destructive scripts invoked.
- Baseline routes continue to load.
- Clear rollback path documented (single-commit revert for each hardening step).

#### Phase 3E — Decision checklist before implementation
Decisions confirmed (2026-04-27):
- Use `DJANGO_`-prefixed env vars with approved names listed in Phase 3B.
- Keep a single `settings.py` for now (no settings-module split at this stage).
- Defer security-header implementation until post-upgrade checkpoints.

### Phase 4 — Staged framework upgrade plan (P1/P2)
**Depends on:** Phase 3 planning complete  
**Output:** staged compatibility path.

- Conservative path: Django 4.0.6 -> 4.2 LTS checkpoint -> 5.2 LTS target.
- Python target baseline: 3.12 (already present in local `.venv`).
- Upgrade dependencies incrementally with verification gates.
- No migration/schema changes unless explicitly approved.

### Phase 5 — Bug-fix and stability tranche (P2)
**Depends on:** baseline + hardening/upgrade checkpoints  
**Output:** targeted fixes with minimal scope.

- Artist pagination issue(s).
- Artists with no artworks visibility rules.
- Malformed city display entries (e.g., `UNKNOWN,`).
- Conditional UI issues (e.g., website button visibility).
- Query/template correctness and basic performance wins (`select_related`/`prefetch_related` where needed).

### Phase 6 — Data integrity & CSV workflow (P2)
**Depends on:** app stability restored  
**Output:** safe, documented import/update workflow.

- Validate idempotency and failure modes of import scripts.
- Define safe import order and rollback/back-up steps.
- Keep destructive reset scripts blocked until explicit approval.
- Plan duplicate cleanup through CSV + importer flow only.

### Phase 7 — Content/structure updates (P3)
**Depends on:** core technical stability  
**Output:** approved content/navigation changes.

- Homepage/About restructuring and placeholders.
- Terminology update (`Tabular data` -> `Search`).
- Publication/submission/hosting info updates.
- Team/logo clean-up and layout fixes.

### Phase 8 — Optional backlog (P4)
- Mobile notice.
- RKD image-linking exploration.
- Secure embedding (JHNA context), without weakening security defaults.

## High-risk tasks
- Settings hardening without breaking deployment assumptions.
- Dependency compatibility across Django 4.2/5.2 checkpoints.
- Destructive script misuse (`reset_*`, `erase_database.py`).
- Template/view logic regressions in list/detail/query pages.
- Data integrity drift between DB and CSV source-of-truth.

## Suggested files for later implementation review
- Core config: `dttg_new/settings.py`, `dttg_new/urls.py`, `manage.py`, `.gitignore`, `requirements.txt`.
- App logic: `data/views.py`, `data/forms.py`, `data/urls.py`, `data/models.py`.
- Templates: `data/templates/data/*.html` (especially artist/museum/city/query templates).
- Data pipeline: `scripts/load_*.py`, `scripts/reset_*.py`, `scripts/erase_database.py`, `data/csv/*.csv`.

## Branch and commit strategy
- Current strategy: single branch is acceptable for now.
- Use atomic commits per subtask (`docs:`, `chore:`, `fix:`, `security:`, `deps:`, `content:`).
- If a task becomes risky, create a temporary sub-branch and merge back after checks.

## Local `.venv` strategy
- `.venv/` already exists locally.
- Keep `.venv/` ignored and never commit it.
- Record interpreter/dependency baseline before any upgrades.

## Dependency and Django strategy
- Baseline first, then staged upgrades.
- Do not jump directly to Django 6.0.
- Prefer conservative path to Django 5.2 LTS, with intermediate checkpoint if needed.
- No dependency upgrades in this planning phase.

## Testing strategy (when implementation begins)
- Start with non-destructive framework checks (`manage.py check`).
- Then route-level smoke checks (home/about/list/detail/query/export/admin).
- Reproduce known bugs before and after each fix.
- Keep changes small and validate per-commit.

## Client report structure (concise)
1. Scope completed.
2. Decisions made and why.
3. Risks addressed / deferred.
4. What changed (by phase).
5. Checks performed.
6. Remaining questions / requested client decisions.

## Deployment verification caveat
Deployment behaviour cannot be fully verified from repository-only access. Full verification requires production/server access and/or explicit deployment runbook details (hosting, env vars, process manager, static/media strategy, DB/runtime details).

## Open question for RKD IT officer — environment variable injection (action required before go-live)

The application now reads its production configuration from environment variables (see `.env.example` for the full list). Before the updated code can be deployed successfully, the RKD IT officer needs to confirm **how environment variables are injected into the Django process** on the server, and then set the following values:

| Variable | Required value |
|----------|---------------|
| `DJANGO_SECRET_KEY` | A new random secret key (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `downtotheground.rkdstudies.nl` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://downtotheground.rkdstudies.nl` |
| `DJANGO_FRAME_ANCESTORS` | Optional allowlist for iframe embedding, e.g. `https://jhna.org,https://www.jhna.org` |
| `DJANGO_STATIC_ROOT` | Absolute path to where static files should be served from on the server |
| `DJANGO_MEDIA_ROOT` | Absolute path to where uploaded media files are stored on the server |

Depending on the server setup, the injection method will be one of:
- **Apache with `mod_wsgi`**: `SetEnv` directives in the Apache `.conf` file for the virtual host.
- **Apache with `mod_wsgi` daemon mode**: `SetEnvIf` in `.conf` or a `WSGIPassAuthorization` + separate env file.
- **systemd service**: `Environment=` or `EnvironmentFile=` directive in the unit file.
- **uWSGI**: `env =` lines in the `.ini` config file, or an `--env` argument.
- **Gunicorn + supervisor/systemd**: env vars in the supervisor `.conf` or systemd unit.
- **Plain `.env` file loaded at startup**: supported if the process manager sources a `.env` file before launching Django.

The IT officer should let us know which of these applies. We can then provide the exact lines to add to their config. **Do not commit a `.env` file or any secrets to the repository.**

After the IT officer confirms the mechanism and sets the variables, `python manage.py check --deploy` should be run on the server to verify the production configuration is sound.

Embedding note (optional): if external embedding is required, set `DJANGO_FRAME_ANCESTORS` to an explicit comma-separated origin allowlist and restart the Django process. Then verify the response header includes `Content-Security-Policy: frame-ancestors ...` and that the target page loads inside an iframe on the allowed site.