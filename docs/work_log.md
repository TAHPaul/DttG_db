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
