# Local Setup Notes

## Current status
- Local virtual environment already exists at `.venv/`.
- `.venv/` is local-only and must not be committed.
- No dependency upgrades performed in this phase.

## `.gitignore` verification
- `.gitignore` includes `.venv` and `.DS_Store` ignore patterns.
- Current unstaged `.gitignore` change removes duplicate trailing entries only; ignore behaviour remains intact.

## Environment baseline evidence

### Python version evidence
Source: `.venv/pyvenv.cfg`
- `version = 3.12.4`
- `home = /opt/homebrew/opt/python@3.12/bin`

### Installed Django evidence
Source: `.venv/lib/python3.12/site-packages/django/__init__.py`
- `VERSION = (4, 0, 6, "final", 0)`

### Dependency baseline (`requirements.txt`)
- `Django==4.0.6`
- `Pillow==9.2.0`
- `django-crispy-forms==1.14.0`
- `django-extensions==3.2.0`
- `django-filter==22.1`
- `django-htmx==1.12.1`

## Non-destructive verification commands (Phase 2)
Run from repository root with local `.venv` active:

```bash
source .venv/bin/activate
python --version
python -m django --version
python -m pip freeze
python manage.py check
```

Optional baseline runtime check:

```bash
python manage.py runserver
```

## Command output log (to fill after execution)

### `python --version`
- Exit code: `0`
- Stdout: `Python 3.12.4`
- Stderr: *(none)*

### `python -m django --version`
- Exit code: `0`
- Stdout: `4.0.6`
- Stderr: *(none)*

### `python -m pip freeze`
- Exit code: `0`
- Stdout:
	- `asgiref==3.11.1`
	- `Django==4.0.6`
	- `django-crispy-forms==1.14.0`
	- `django-extensions==3.2.0`
	- `django-filter==22.1`
	- `django-htmx==1.12.1`
	- `Pillow==9.2.0`
	- `sqlparse==0.5.5`
- Stderr: *(none)*

### `python manage.py check`
- Exit code: `0`
- Stdout: `System check identified no issues (0 silenced).`
- Stderr: *(none)*

## Expected baseline outcomes (quick interpretation)
- `python --version`: should report Python 3.12.x from local `.venv`.
- `python -m django --version`: should report Django 4.0.6 baseline.
- `python -m pip freeze`: should include the pinned packages from `requirements.txt` (plus any local extras).
- `python manage.py check`: preferred outcome is `System check identified no issues`; if not, capture full error text before making changes.

## Manual reporting format (copy/paste)
- Command:
- Exit code:
- Stdout:
- Stderr:

## Important caveat
These outputs were captured from your local terminal session and logged here as the authoritative Phase 2A baseline.

## Phase 2B run-as-is smoke results (2026-04-27)

### Route checklist results
Verified via local runserver probe:
- `/` -> `200`
- `/about/` -> `200`
- `/artists/` -> `200`
- `/entries/` -> `200`
- `/entries-table-simple/` -> `200`
- `/entries-table-adv/` -> `200`
- `/museums/` -> `200`
- `/city-of-execution/` -> `200`
- `/dttg-login/` -> app responds; server log shows redirect to login (`302` then login page `200`)

### Issues observed during baseline browsing/log inspection
- Reproduced pagination-related server error on artist listing:
	- URL: `/artists/?page=21`
	- Error: `django.urls.exceptions.NoReverseMatch`
	- Message excerpt: reverse for `city-of-execution-detail` with empty argument `''` not found.
- Observed non-critical 404 noise from browser/devtools probes:
	- `/.well-known/appspecific/com.chrome.devtools.json`
	- `/favicon.ico`

### Phase 2B conclusion
- Baseline app is generally runnable and key routes load.
- At least one known bug is confirmed and should be handled in planned bug-fix tranche before modernization work proceeds too far.

## Django 4.2 LTS checkpoint (2026-04-27)
- Upgrade performed: `Django 4.0.6` -> `Django 4.2.30`.
- `requirements.txt` updated to pin `Django==4.2.30`.
- `python manage.py check` result: `System check identified no issues (0 silenced).`

### 4.2 route smoke results
Verified via local server + urllib probes:
- `/` -> `200`
- `/about/` -> `200`
- `/artists/` -> `200`
- `/entries/` -> `200`
- `/entries-table-simple/` -> `200`
- `/entries-table-adv/` -> `200`
- `/museums/` -> `200`
- `/city-of-execution/` -> `200`
- `/dttg-login/` -> `200` (redirect/login flow working)

### Note on test-client probing
Using Django `Client()` without host override triggered `DisallowedHost` for `testserver` due current `ALLOWED_HOSTS=[]`. This did not block local runserver checks and is treated as a testing-method caveat, not an upgrade blocker.
