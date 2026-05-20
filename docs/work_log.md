# Work Log

## Template
- **Date:**
- **Branch:**
- **Commit:**
- **Area:**
- **Files changed:**
- **Summary of change:**
- **Reason for change:**
- **Testing/checks performed:**
- **Client-facing note:**
- **Outstanding questions:**

---

## 2026-04-27
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted
- **Area:** Planning / repository safety baseline
- **Files changed:** `docs/update_plan.md`, `docs/work_log.md`, `docs/risk_register.md`, `docs/local_setup_notes.md`, `docs/copilot_working_notes.md`, `.github/copilot-instructions.md`
- **Summary of change:** Created planning and risk documents, captured local environment baseline evidence, and set phased execution order.
- **Reason for change:** Establish safe modernization path before touching implementation code.
- **Testing/checks performed:** Repository inspection and read-only evidence capture. Command execution in this session is unavailable; commands queued for manual run: `python --version`, `python -m django --version`, `python -m pip freeze`, `python manage.py check`.
- **Client-facing note:** No application behaviour was changed. This entry only establishes plan, risk controls, and local setup baseline.
- **Outstanding questions:** Confirm when to start Phase 2 command verification and whether to keep current `.gitignore` hygiene diff in planning commit.

## 2026-04-27 (follow-up)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted
- **Area:** Phase 2 baseline preparation
- **Files changed:** `docs/update_plan.md`, `docs/local_setup_notes.md`, `docs/work_log.md`
- **Summary of change:** Added explicit run-as-is smoke checklist and command-output capture template to accelerate baseline verification.
- **Reason for change:** Continue execution without touching implementation files while terminal execution is unavailable in this tool session.
- **Testing/checks performed:** Attempted to run non-destructive commands through tooling; execution capability unavailable in-session.
- **Client-facing note:** Planning/docs are now ready for immediate baseline capture once commands are run locally.
- **Outstanding questions:** Please provide command outputs so Phase 2 can be marked complete.

## 2026-04-27 (Phase 2A completed)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted
- **Area:** Local baseline verification
- **Files changed:** `docs/local_setup_notes.md`, `docs/work_log.md`, `docs/update_plan.md`
- **Summary of change:** Recorded non-destructive baseline command outputs and marked Phase 2A as complete.
- **Reason for change:** Confirm local runtime before any hardening or upgrade activity.
- **Testing/checks performed:**
	- `python --version` -> `Python 3.12.4`
	- `python -m django --version` -> `4.0.6`
	- `python -m pip freeze` -> package baseline captured
	- `python manage.py check` -> `System check identified no issues (0 silenced).`
- **Client-facing note:** The project baseline is healthy in local environment; no code or schema changes were made.
- **Outstanding questions:** Proceed to Phase 2B run-as-is smoke checklist now?

## 2026-04-27 (Phase 2B completed)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted
- **Area:** Run-as-is smoke baseline
- **Files changed:** `docs/local_setup_notes.md`, `docs/update_plan.md`, `docs/work_log.md`
- **Summary of change:** Completed route smoke checklist and logged baseline runtime observations.
- **Reason for change:** Validate current application behaviour before security hardening and upgrade planning.
- **Testing/checks performed:**
	- Started local server and probed key routes (`/`, `/about/`, `/artists/`, `/entries/`, `/entries-table-simple/`, `/entries-table-adv/`, `/museums/`, `/city-of-execution/`, `/dttg-login/`).
	- All checklist routes responded successfully; admin path redirects to login as expected.
	- Reproduced known error on `/artists/?page=21` with `NoReverseMatch` for `city-of-execution-detail` and empty city argument.
- **Client-facing note:** The site runs locally and core pages load, but at least one pagination-related artist page error is confirmed and should be fixed in the maintenance phase.
- **Outstanding questions:** Approve moving to Phase 3 planning detail and then implementation of confirmed bug fixes in controlled, small commits?

## 2026-04-27 (Phase 3 planning detailed)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted
- **Area:** Security/config hardening planning
- **Files changed:** `docs/update_plan.md`, `docs/risk_register.md`, `docs/work_log.md`
- **Summary of change:** Expanded Phase 3 into a concrete hardening checklist with sequencing, acceptance criteria, and pre-implementation decision gates.
- **Reason for change:** Prepare safe implementation order after local baseline completion.
- **Testing/checks performed:** Planning-only documentation updates; no implementation changes.
- **Client-facing note:** The hardening phase is now explicitly staged to reduce risk and avoid deployment drift.
- **Outstanding questions:** Confirm env variable policy and whether settings should remain single-file or split before hardening implementation begins.

## 2026-04-27 (Phase 3 inventory confirmed)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted
- **Area:** Security/config inventory refinement
- **Files changed:** `docs/update_plan.md`, `docs/copilot_working_notes.md`, `docs/work_log.md`
- **Summary of change:** Added confirmed current-settings inventory details and updated tooling constraints notes.
- **Reason for change:** Ensure hardening plan is based on concrete repo state before implementation starts.
- **Testing/checks performed:** Read-only review of `dttg_new/settings.py` and `dttg_new/urls.py`.
- **Client-facing note:** Planning now explicitly reflects the current config risks and practical verification constraints.
- **Outstanding questions:** Confirm env var naming/policy and settings structure choice (single-file vs split module).

## 2026-04-27 (Phase 3 decisions confirmed)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted
- **Area:** Hardening policy decisions
- **Files changed:** `docs/update_plan.md`, `docs/risk_register.md`, `docs/work_log.md`, `docs/copilot_working_notes.md`
- **Summary of change:** Locked env var policy, settings structure, and security-header timing decisions into planning docs.
- **Reason for change:** Remove ambiguity before controlled settings hardening implementation.
- **Testing/checks performed:** Planning documentation updates only; no runtime or code changes.
- **Client-facing note:** The hardening approach is now fully agreed and staged safely for this legacy deployment context.
- **Outstanding questions:** None for policy; next action is implementation planning order (bug-fix first vs hardening first in code phase).

## 2026-04-27 (Django 4.2 checkpoint)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted (manual commit pending)
- **Area:** Framework/runtime upgrade checkpoint
- **Files changed:** `requirements.txt`, `docs/update_plan.md`, `docs/work_log.md`, `docs/local_setup_notes.md`
- **Summary of change:** Upgraded Django from `4.0.6` to `4.2.30`, pinned requirements, and completed 4.2 validation checks.
- **Reason for change:** Follow agreed upgrade-first sequencing before functional bug-fix work.
- **Testing/checks performed:**
	- `python -m django --version` -> `4.2.30`
	- `python manage.py check` -> `System check identified no issues (0 silenced).`
	- Route smoke (local server) -> `/`, `/about/`, `/artists/`, `/entries/`, `/entries-table-simple/`, `/entries-table-adv/`, `/museums/`, `/city-of-execution/`, `/dttg-login/` all successful.
- **Client-facing note:** Django 4.2 checkpoint is stable locally with no upgrade-blocking runtime failures.
- **Outstanding questions:** Proceed directly to Django 5.2 checkpoint.

## 2026-04-27 (Django 5.2 checkpoint)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted (manual commit pending)
- **Area:** Framework/runtime upgrade checkpoint
- **Files changed:** `requirements.txt`, `docs/update_plan.md`, `docs/work_log.md`, `docs/local_setup_notes.md`, `docs/copilot_working_notes.md`
- **Summary of change:** Upgraded Django from `4.2.30` to `5.2.13`; resolved one upgrade blocker by updating `django-filter` from `22.1` to `25.2`.
- **Reason for change:** Complete agreed LTS checkpoint path before functional bug-fix tranche.
- **Testing/checks performed:**
	- `python -m django --version` -> `5.2.13`
	- `python manage.py check` -> `System check identified no issues (0 silenced).`
	- Initial route smoke identified one blocker: `/entries-table-adv/` returned `500`.
	- Traceback review indicated `django-filter==22.1` compatibility issue under Django 5.2.
	- After blocker-only dependency update, route smoke passed on `/`, `/about/`, `/artists/`, `/entries/`, `/entries-table-simple/`, `/entries-table-adv/`, `/museums/`, `/city-of-execution/`, `/dttg-login/`.
- **Client-facing note:** Django 5.2 checkpoint is stable locally. Existing known functional issues outside upgrade blockers remain deferred by plan.
- **Outstanding questions:** Approve checkpoint commit, then begin post-checkpoint functional fixes.

## 2026-04-27 (Dependency usage + compatibility audit)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** uncommitted (manual commit pending)
- **Area:** Dependency compatibility and cleanup
- **Files changed:** `requirements.txt`, `dttg_new/settings.py`, `docs/work_log.md`
- **Summary of change:** Audited extension compatibility and code usage; removed unused `django-htmx` and `django-extensions` from settings and pinned requirements.
- **Reason for change:** Reduce maintenance surface and remove packages not used by runtime app code.
- **Testing/checks performed:**
	- `python -m pip check` -> no broken requirements.
	- `python manage.py check` -> no issues.
	- Imported remaining declared extension modules (`django`, `PIL`, `crispy_forms`, `django_filters`) successfully.
	- Uninstalled `django-htmx` and `django-extensions` from `.venv` and re-ran checks.
	- Smoke probes after uninstall: `/`, `/entries-table-simple/`, `/entries-table-adv/` all `200`.
- **Client-facing note:** Compatibility remains clean after removal; `django-filter` and `django-crispy-forms` are actively used by forms/templates and should remain.
- **Outstanding questions:** None for compatibility; next functional tranche can proceed.

## 2026-04-27 (Bug fixes — artist pagination, museum UI)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** `fix: artist pagination crash, hide artists without artworks, museum city/country and website display`
- **Area:** Application bug fixes
- **Files changed:** `data/views.py`, `data/templates/data/artist_list.html`, `data/templates/data/museum_list.html`
- **Summary of change:** Fixed four confirmed bugs:
	1. Artist list pagination hard crash (`NoReverseMatch`) on pages where an artist had an empty city-of-birth or city-of-death — birth/death city links are now conditionally rendered.
	2. Artists with no artworks in the database were appearing in the artist list — the view now filters them out.
	3. Museum cards showed `UNKNOWN,` when no country was stored — the comma separator is now conditional on the country field being non-empty; location text centred.
	4. Museum cards always showed a `(Site)` link even when no website URL was stored — the link is now conditional on `museum.website` being non-empty.
- **Reason for change:** Functional correctness and UI cleanliness; bug #1 caused a hard 500 error visible to users.
- **Testing/checks performed:**
	- `python manage.py check` -> clean.
	- `/artists/?page=21` (previously crashing) -> `200`.
	- All artist pages 11–22 -> `200` confirmed in server log during manual review.
	- `/museums/` -> `200`.
- **Client-facing note:** Pagination on the artist overview no longer crashes. Artists without artworks are hidden. Museum location and website display is now clean.
- **Outstanding questions:** None.

## 2026-04-27 (Security hardening — environment-driven configuration)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** `security: env-driven settings, CSRF trusted origins, deployment notes for RKD IT`
- **Area:** Settings hardening / production readiness
- **Files changed:** `dttg_new/settings.py`, `.env.example`, `.gitignore`, `docs/update_plan.md`
- **Summary of change:** Moved `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `STATIC_ROOT`, and `MEDIA_ROOT` from hardcoded values to environment variable reads with safe local fallbacks. Added `.env.example` as a reference template. Added `.env` to `.gitignore` to prevent secrets being committed.
- **Reason for change:**
	- The hardcoded `SECRET_KEY` in source is a security risk.
	- `DEBUG=True` hardcoded meant debug output was exposed on the live site.
	- The CSRF 403 error seen at `https://downtotheground.rkdstudies.nl/dttg-login/` was caused by `CSRF_TRUSTED_ORIGINS` not being set for the production hostname.
- **Testing/checks performed:**
	- `python manage.py check` -> clean.
	- Settings values verified with no env vars set: `DEBUG=True`, empty `ALLOWED_HOSTS`, empty `CSRF_TRUSTED_ORIGINS` (correct local-dev defaults).
- **Client-facing note:** The application is now safe to deploy without secrets in source code. The CSRF 403 login error will be resolved once the RKD IT officer sets the four required environment variables on the server (documented in `docs/update_plan.md` under "Open question for RKD IT officer").
- **Action required (RKD IT officer — before go-live):**
	- Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS` as environment variables in the server process.
	- Restart the Django process after setting them.
	- Run `python manage.py check --deploy` on the server to confirm production readiness.
	- Full instructions and variable values are in `docs/update_plan.md` → "Open question for RKD IT officer".
- **Outstanding questions:** RKD IT officer to confirm how environment variables are injected into the Django process (Apache mod_wsgi, systemd, uWSGI, etc.).

## 2026-04-27 (User/auth reset)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** N/A (database change only — not version controlled)
- **Area:** Authentication / user management
- **Files changed:** None (DB only)
- **Summary of change:** All four legacy admin accounts (last active 2022, passwords lost) were deleted and a new superuser was created. Additional staff accounts created via Django admin for active users.
- **Reason for change:** Passwords to existing accounts were lost; fresh start required.
- **Testing/checks performed:** Login confirmed working via `/dttg-login/`.
- **Client-facing note:** Users can change their own password at any time via `/dttg-login/password_change/`.
- **Outstanding questions:** None.

## 2026-04-27 (RKD image sync complete + refresh runbook)
- **Date:** 2026-04-27
- **Branch:** `dttg-deployment-update`
- **Commit:** `1ea6ef8`, `1a7611b`
- **Area:** RKD image integration operations
- **Files changed:** `data/management/commands/fetch_rkd_images.py`, `README.md`
- **Summary of change:** Completed RKD image URL backfill and added an operational runbook for future refreshes when new `rkd_link` values are added.
- **Reason for change:** Ensure maintainers can safely re-run synchronization without manual supervision.
- **Testing/checks performed:**
	- Verified command supports `--dry-run`, `--max-updates`, and `--until-stable`.
	- Verified database state after sync:
		- Artists with RKD links: `196`; fetched: `119`; remaining: `77`.
		- Artworks with RKD links: `409`; fetched: `407`; remaining: `2` (`M723`, `M724`).
	- Spot checks showed remaining records are due to upstream RKD no-image responses or API errors.
- **Client-facing note:** For future updates, run `python manage.py fetch_rkd_images --until-stable`; it stops automatically when no new URLs can be fetched.
- **Outstanding questions:** None.
---

## 2026-04-27 — Documentation hub restructure
- **Date:** 2026-04-27
- **Branch:** `content-ui-refresh`
- **Commit:** `617d349`
- **Area:** Content / UI refresh — Phase 3 (Documentation page)
- **Files changed:** `data/templates/data/db-info.html`, `data/static/data/main.css`
- **Summary of change:** Replaced legacy Bootstrap tab UI in `db-info.html` with a long-form documentation hub. Added top anchor navigation and 8 content sections: How to Use, Reliability System, Colour System, Terminology, Cross-Section Images, Database Notes, Database Development, Citation & Reuse. Added additive `doc-hub__*` CSS component block to `main.css` with mobile responsive overrides.
- **Reason for change:** Phase 3 of `content-ui-refresh` plan approved prior to this session. Tab layout was inaccessible and did not scale gracefully on mobile.
- **Testing/checks performed:**
  - `python manage.py check` — no issues.
  - Template loaded successfully via `Engine.find_template` (bypassing cache).
  - Route `/db_info/`, URL name `database-info`, and nav label "Documentation" all unchanged.
  - Inbound deep-link anchors `#how-to-use` and `#colour-system` (used by homepage CTAs) are present.
  - Colour system section uses `colour_reference.html` partial in `mode='full'`.
  - Reliability text normalised to 1–4 throughout; legacy "1 to 5" text removed.
  - Legacy tab CSS left intact in `main.css` (no regressions on other pages).
- **Client-facing note:** The Documentation page is now a single scrollable page with anchor links at the top. All previous tab content is preserved and reorganised. The colour swatch system is now fully visible without tab interaction.
- **Outstanding questions:** None.

---

## 2026-04-28 — Documentation colour checker refinements
- **Date:** 2026-04-28
- **Branch:** `content-ui-refresh`
- **Commit:** uncommitted
- **Area:** Content / UI refresh — Documentation colour checker interaction polish
- **Files changed:** `data/templates/data/db-info.html`, `data/templates/data/partials/colour_reference.html`, `data/static/data/main.css`, `docs/work_log.md`
- **Summary of change:** Refined colour checker presentation in documentation hub to a structured row layout with Light → Mid → Dark ordering for chromatic groups, separate Black/White rows, full-width swatches per grid cell, single separator treatment, and improved hover readability. Replaced pseudo-element HEX overlay with real selectable text so users can copy HEX values directly.
- **Reason for change:** Improve legibility and usability for researchers who need to reference and copy exact colour values.
- **Testing/checks performed:**
	- `python manage.py check` — no issues.
	- Template parse checks passed for `db-info.html` and `partials/colour_reference.html`.
	- Visual behavior verified in CSS rules: full-width swatches, no double separator line, hover overlay with bold white HEX text.
- **Client-facing note:** On Documentation → Colour System, users can now highlight and copy HEX values directly from swatches while keeping the same dark-overlay hover cue.
- **Outstanding questions:** None.