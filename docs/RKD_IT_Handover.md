# DttG Database — IT Handover Guide

**System:** Down to the Ground (DttG) Database  
**Live URL:** https://downtotheground.rkdstudies.nl  
**GitHub:** https://github.com/TAHPaul/DttG_db  
**Contact:** hall-aquitania@rkd.nl / dttg@rkd.nl  

---

## What is this system?

The DttG Database is a Django web application that provides an open-access searchable database of colored ground layers in Netherlandish painting. It consists of:

- A **SQLite database** (`db.sqlite3`) holding all research data.
- A **Django application** serving browse, search, and export pages.
- A **media directory** holding artist and artwork images.
- A **Django admin interface** at `/admin/` for data management.

---

## Server requirements

| Requirement | Details |
|---|---|
| Python | 3.9 or higher (3.12 recommended) |
| Web server | Any WSGI-capable server: Apache + mod_wsgi, Gunicorn, uWSGI |
| Storage | SQLite file + media directory (images); no separate database server needed |
| OS | Linux (any modern distribution) |

Python package dependencies are listed in `requirements.txt` and can be installed via pip.

---

## Getting the code onto the server

If the code is not already present, clone from GitHub:

```bash
git clone https://github.com/TAHPaul/DttG_db.git
cd DttG_db
```

To update an existing installation with the latest code:

```bash
git pull origin main
```

After pulling, always run the steps in the **Post-deployment checklist** section below.

---

## Python environment setup

Create and activate a virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The virtual environment directory (`.venv/`) is excluded from version control and must be created on the server.

---

## Production configuration (environment variables)

The application reads all sensitive settings from environment variables. These must be set on the server before starting the Django process. **Never commit real values to the repository.**

A template showing all available variables is in `.env.example`.

### Required variables

| Variable | Value |
|---|---|
| `DJANGO_SECRET_KEY` | A long random string (generate one — see below) |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `downtotheground.rkdstudies.nl` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://downtotheground.rkdstudies.nl` |
| `DJANGO_STATIC_ROOT` | Absolute path to the directory where static files should be served from |
| `DJANGO_MEDIA_ROOT` | Absolute path to the directory where uploaded images are stored |

### Optional variables

| Variable | Purpose |
|---|---|
| `DJANGO_FRAME_ANCESTORS` | Comma-separated list of external origins permitted to embed this site in an iframe (e.g. `https://jhna.org,https://www.jhna.org`). Leave unset to keep default iframe protection. |

### Generating a secret key

Run this once on the server and save the output as `DJANGO_SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### How to set variables — by server type

**Option A: `.env` file (simplest)**  
Copy `.env.example` to `.env` in the project root and fill in the values. Django will load it automatically when `.venv/` is present (which is always the case on the server).

```bash
cp .env.example .env
nano .env   # fill in your values
```

**Option B: Apache + mod_wsgi**  
Add `SetEnv` directives to the Apache virtual host configuration:

```apache
<VirtualHost *:443>
    ...
    SetEnv DJANGO_SECRET_KEY "your-key-here"
    SetEnv DJANGO_DEBUG "False"
    SetEnv DJANGO_ALLOWED_HOSTS "downtotheground.rkdstudies.nl"
    SetEnv DJANGO_CSRF_TRUSTED_ORIGINS "https://downtotheground.rkdstudies.nl"
    SetEnv DJANGO_STATIC_ROOT "/var/www/dttg/staticfiles"
    SetEnv DJANGO_MEDIA_ROOT "/var/www/dttg/media"
    ...
</VirtualHost>
```

**Option C: systemd service**  
Add an `EnvironmentFile=` directive pointing to a file containing the variables, or use inline `Environment=` directives:

```ini
[Service]
EnvironmentFile=/etc/dttg/env
```

**Option D: uWSGI**  
Add `env =` lines to the `.ini` config file:

```ini
env = DJANGO_SECRET_KEY=your-key-here
env = DJANGO_DEBUG=False
```

---

## WSGI entry point

The WSGI application is defined in `dttg_new/wsgi.py`. When configuring your web server, point it at:

```
/path/to/DttG_db/dttg_new/wsgi.py
```

The WSGI callable is `application` (this is the Django default).

**Apache + mod_wsgi example:**

```apache
WSGIDaemonProcess dttg python-home=/path/to/DttG_db/.venv python-path=/path/to/DttG_db
WSGIProcessGroup dttg
WSGIScriptAlias / /path/to/DttG_db/dttg_new/wsgi.py

<Directory /path/to/DttG_db/dttg_new>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>
```

**Serving static files via Apache:**

```apache
Alias /static/ /var/www/dttg/staticfiles/
<Directory /var/www/dttg/staticfiles>
    Require all granted
</Directory>

Alias /media/ /var/www/dttg/media/
<Directory /var/www/dttg/media>
    Require all granted
</Directory>
```

---

## Database setup

The database file is `db.sqlite3` in the project root (or wherever `DJANGO_MEDIA_ROOT` points — `db.sqlite3` always lives in the project root).

### Running migrations

Migrations must be run after the initial setup and after any code update that includes new migration files:

```bash
source .venv/bin/activate
python manage.py migrate
```

### Check production readiness

After configuring environment variables, run this to verify the deployment configuration:

```bash
python manage.py check --deploy
```

Fix any warnings before going live.

---

## Static files

Django does not serve static files itself in production — they must be collected to a directory that the web server serves directly.

Run this after initial setup and after every code update:

```bash
source .venv/bin/activate
python manage.py collectstatic --noinput
```

Files are written to the path set in `DJANGO_STATIC_ROOT`. Make sure the web server is configured to serve that directory at `/static/` (see WSGI section above).

---

## Media files

Uploaded images (artist portraits, artwork photos, site logos) are stored in the `media/` directory (or `DJANGO_MEDIA_ROOT` if overridden). These files are **not in the git repository** and must be backed up separately.

If migrating the site to a new server, copy the `media/` directory manually alongside the database file.

---

## Admin user management

The Django admin interface is at `/admin/`. Only users with `is_staff=True` can access it.

### Creating a superuser (first-time setup)

```bash
source .venv/bin/activate
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### Creating additional staff users

Log in to `/admin/`, go to **Users**, and add new accounts. Set "Staff status" if the user should access the admin. Superuser status grants full permissions.

### Password resets

Users can change their own password at `/dttg-login/password_change/`. An admin can also change any user's password from the Django admin.

---

## Post-deployment checklist

Run these steps after every code update (`git pull`):

```bash
source .venv/bin/activate
pip install -r requirements.txt      # pick up any dependency changes
python manage.py migrate             # apply any new migrations
python manage.py collectstatic --noinput  # update static files
sudo systemctl restart <your-service>    # restart the Django process
```

Verify the site is responding after restart.

---

## Ongoing maintenance

### Updating the database from CSV files

When new or corrected data is available in the `data/csv/` directory, import it using the management command:

```bash
source .venv/bin/activate

# Interactive mode (prompts for each section):
python manage.py update_db

# Run specific sections only:
python manage.py update_db --artists --museums

# Run everything non-interactively:
python manage.py update_db --all --yes

# Preview what would run without making changes:
python manage.py update_db --all --dry-run
```

### Refreshing RKD image links

When new artworks or artists with RKD links are added, run this to fetch and store their thumbnail URLs:

```bash
source .venv/bin/activate
python manage.py fetch_rkd_images --until-stable
```

This only processes records that are missing an image URL and stops automatically when nothing new is found. Useful variants:

```bash
# Count pending records without making changes:
python manage.py fetch_rkd_images --dry-run

# Artists only / artworks only:
python manage.py fetch_rkd_images --artists-only --until-stable
python manage.py fetch_rkd_images --artworks-only --until-stable
```

---

## Backup

The following must be backed up regularly:

| Item | Location | Notes |
|---|---|---|
| Database | `db.sqlite3` (project root) | Copy the file; Django must not be writing to it during copy, or use `python manage.py dumpdata` for a safe export |
| Media files | `media/` directory (or `DJANGO_MEDIA_ROOT`) | Not in git; copy directory |
| Environment variables | Your `.env` file or server config | Contains the secret key and should be stored securely |

---

## Directory structure (what each folder contains)

```
DttG_db/
├── data/               Django app: models, views, forms, templates, migrations
│   ├── csv/            Source CSV files for database updates
│   ├── management/     Custom management commands (fetch_rkd_images, update_db)
│   ├── migrations/     Database migration history
│   ├── static/         App-level static files (CSS, JS, favicon)
│   └── templates/      HTML templates
├── docs/               Documentation (PDF user guide, submission template, this file)
├── dttg_new/           Django project settings, URLs, WSGI entry point
├── media/              Uploaded images — not in git, back up separately
├── scripts/            Legacy CSV data-loading scripts (one-off initial import use)
├── .env.example        Template for production environment variables
├── db.sqlite3          SQLite database — not in git, back up separately
├── manage.py           Django management script
└── requirements.txt    Python dependencies
```

---

## Troubleshooting

**Site returns 500 errors after a code update**  
Run `python manage.py check` and check the server error log. Most common cause: pending migrations not run, or `DJANGO_SECRET_KEY` not set.

**Login returns CSRF 403 error**  
`DJANGO_CSRF_TRUSTED_ORIGINS` is not set or does not match the site's HTTPS URL exactly (including the `https://` prefix).

**Static files not loading (missing CSS/JS)**  
`python manage.py collectstatic` was not run after the update, or the web server is not serving `DJANGO_STATIC_ROOT` at `/static/`.

**Images not displaying**  
The `media/` directory is missing or the web server is not serving `DJANGO_MEDIA_ROOT` at `/media/`.

**Admin login works but public login (`/dttg-login/`) returns 403**  
Same as CSRF issue above — check `DJANGO_CSRF_TRUSTED_ORIGINS`.

---

*For application-level questions, contact paul.vanlaar@rkd.nl or hall-aquitania@rkd.nl.*
