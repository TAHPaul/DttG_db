# Risk Register

| Risk | Severity | Likelihood | Mitigation | Owner | Decision Needed |
|---|---|---|---|---|---|
| Confirmed artist pagination runtime error (`/artists/?page=21`) | High | High | Fix URL generation guard for empty city references before broader modernization; re-run route smoke checks | Dev | Approve bug-fix tranche ordering (bug-first) |
| Hardcoded secret/debug/hosts assumptions in settings | High | High | Introduce approved `DJANGO_` env vars in single settings file with backward-compatible defaults | Dev | None (policy confirmed) |
| Dependency incompatibility during Django upgrade | High | High | Staged path (4.2 checkpoint then 5.2), verify after each step | Dev | Approve checkpoint strategy |
| Destructive data scripts accidentally run (`reset_*`, `erase_database.py`) | High | Medium | Explicitly block destructive commands until approved | Dev + Client | Confirm safe command allowlist |
| CSV/DB integrity drift | High | Medium | Treat CSV as source of truth; define import order + validation workflow before any cleanup | Dev + Data Owner | Confirm canonical import workflow |
| Template/view logic regressions while fixing UI bugs | Medium | Medium | Reproduce bug first, patch minimally, smoke test impacted routes | Dev | Confirm acceptance criteria for behaviour changes |
| Performance bottlenecks in query/list templates | Medium | Medium | Profile obvious hotspots and apply targeted queryset improvements only | Dev | Confirm performance threshold priorities |
| Unknown production deployment behaviour | High | High | Document assumptions and limits; require production/server access or runbook for verification | Client/Infra | Provide deployment instructions/access |
| Security hardening without deployment runbook may introduce deploy drift | High | Medium | Keep hardening changes incremental and local-safe; defer security headers until post-upgrade checkpoints | Dev + Client/Infra | Confirm deployment variable contract before applying strict production defaults |
| Local-only artifacts committed by accident (`.venv`, media, local DB) | Medium | Low | Maintain `.gitignore`, atomic commits, review changed files before commit | Dev | Confirm commit hygiene policy |

## Risk notes from current inspection
- Existing `.gitignore` diff appears hygiene-only: duplicate trailing `.venv/` and `.DS_Store` lines removed while equivalent ignore entries remain earlier in the file.
- Deployment behaviour cannot be fully validated without production/server access or explicit deployment documentation.
- Phase 2B confirmed a reproducible runtime error on artist pagination (`NoReverseMatch` with empty city argument), now tracked as a priority maintenance item.
- Policy decisions confirmed: `DJANGO_` env-var naming, single `settings.py` for now, security headers deferred until after 4.2/5.2 upgrade checkpoints.
