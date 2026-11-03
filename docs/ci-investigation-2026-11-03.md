# CI investigation — 2026-11-03

Baseline: `827ac675a8e12b3c5dc4e17e58a7e1ef7e2a1c5e`.
The last four weekly E2E runs (October 12, 19, 26 and November 2) failed on this unchanged revision.

Evidence: [run 41429085843](https://github.com/Nellie-ai/stellar-burgers-ui-tests/actions/runs/41429085843), both job logs and both Allure artifacts. Failure screenshots were inspected.

| Observation | Classification | Action |
| --- | --- | --- |
| Both browsers open Krator bun N-200i while assertion expects Fluorescent bun R2-D3 | Confirmed test defect: positional selection | Select the expected bun by exact name; compare the modal name exactly; use the same card for drag and counter |
| Counter tests discard the created order number | Confirmed false-positive risk, not a demonstrated application defect | Require that exact order in the completed section, then require global counter growth |
| Firefox `about:neterror?e=netTimeout` and API registration `ReadTimeout` | Confirmed connectivity/availability failures; server vs runner cause unproven | Preserve failures; no retry, skip or timeout increase |
| Firefox feed title times out; screenshot shows “Loading…” | Feed data did not become available; application vs WebSocket/network cause unproven | Preserve failure and report limitation |

The public client was inspected read-only: completed orders are `status == done`, but only five are displayed. Shared counters do not establish causality or exact increment size. No application defect is claimed without further evidence. The transient “In progress” observation can also be missed on a shared stand.

Local verification after the fix (Python 3.13, Windows):

- PASS: `python -m pytest tests/test_assertion_guards.py -q` — 5 passed.
- PASS: `python -m pytest --collect-only -q` — 21 cases (16 browser + 5 offline).
- PASS: `python -m compileall -q pages locators tests utils conftest.py`.
- PASS: `git diff --check`.
- PASS: `python -m pytest tests/test_constructor.py -m chrome -q --alluredir=../evidence/ui-local-chrome --clean-alluredir` — 5 passed, 5 deselected, 78 seconds, against the educational stand. This does not validate order-feed scenarios or Firefox.
- Initial sandboxed browser attempt was BLOCKED at WebDriver startup; the permitted run above completed successfully.

No tests were disabled and timeout values were not increased. Full browser checks are triggered on this PR; their links and conclusions belong in the PR validation record.
