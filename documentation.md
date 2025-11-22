STATEMeNT TITLe:
The Al Flow State Facilitator
DESGRIPTION:
In the modern digital environment, students are in a constant battle against distractions. The
"attention economy" is
designed to pull focus, making the deep, sustained concentration required for effective learning-often called a
"flow state"-increasingly difficult to achieve. productivity tools are static; they fail to adapt to an individual's unique cognitive rhythms.
The challenge is to create an Al-driven "Focus Facilitator" that not only detects when a user enters a flow state but actively works to extend and deepen that state. This system must move beyond passive timers and act as an intelligent partner that helps users build their capacity for sustained concentration, allowing them to reach their maximum cognitive potential.

THE SOLUTION COULD eNCOMPASS THe FOLLOWING:
*   REAL-TIME FLOW STATE DETECTION: An on-device Al that continuously analyzes work patterns (e.g., typing cadence, app interaction, task-switching frequency) to accurately identify the moment a user enters a flow state, distinguishing it from simple work or distraction.
*   DYNAMIC FLOW STATE AMPLIFICATION: Once flow is detected, the system intelligently amplifies it. This must include locking down the digital environment by suppressing all non-critical notifications and proactively blocking known distraction patterns specifically toprotect the active flow state.
*   INTELLIGENT STAMINA BUILDING: Instead of just suggesting breaks, the Al should help the user extend their focus. It monitors for the earliest signs of cognitive fatigue and provides micro-interventions oroptimized break suggestions designed to recharge the user just enough to return to a deep work state, gradually building their overall focus stamina.
*   POTENTIAL & PERFORMANCE ANALYTICS: A private dashboard focused on "flow potential." It should visualize how long flow states maintained, what triggers them, what breaks them,
and provide
actionable insights on how the user can
progressively
increase their capacity for deep, uninterrupted work.

1 — Single-sentence mission
Build a lightweight macOS background agent + Chrome helper + local dashboard that detects when a user enters flow, silences distractions, logs sessions, and shows a private local dashboard — rule-based detection only (no biometrics, no cloud).
2 — High-level components (what you’ll deliver)
macOS Background Agent (Agent) — runs in user session, collects events, evaluates rules, toggles protection, and writes to local DB.
Chrome Helper (Extension) — receives enable/disable signals and blocks a configured blocklist (user-editable).
Local Dashboard (Web UI) — local-only server providing session list, daily totals, and simple charts.
Local DB — SQLite storing sessions + raw events.
Tray/Menu UI (minimal) — small status menu to start/stop agent, show current state (Idle/Working/In-Flow), and a quick toggle/whitelist.
Installer / Packaging — signed notarized app later; dev builds with a packaging tool.
3 — Non-functional constraints / design choices
Privacy-first: Data stored locally only by default. Optionally export CSV. No cloud in MVP.
Rule-based detection first: Use configurable thresholds. Collect data for later ML, but don’t train in MVP.
Low-permission footprint: Only request macOS permissions that are strictly necessary (explain to user why).
Resilient: Agent should fail gracefully if DND toggle or extension message fails (log and notify user in menu).
Lightweight: Minimal CPU/memory — suitable for students running dev tools.
4 — Key UX flows (what the user experiences)
Install & Run: User runs the app, grants prompted accessibility permission, and sees a menu icon with current state.
Passive Detection: User starts working; after 5 minutes of meeting the flow rule, the app enters Flow Mode and:
Enables Do-Not-Disturb (DND).
Sends message to Chrome extension to block the blocklist.
Logs start timestamp and context (foreground app).
Flow Exit: When rule no longer holds (typing drops or switches), agent exits Flow Mode, turns DND off, disables blocking, and closes session with analytics.
Dashboard: User opens dashboard (local URL) to view today’s total flow time, session history, and simple insights.
Override & Whitelist: User can pause protection or whitelist a site/app from the menu.
5 — Exact detection rules & parameters (copy-ready config)
Rolling window: 5 minutes (300s)
Flow ON criteria (all must hold for a continuous 5-min window or configurable flow_entry_window):
typing_rate >= 40 kpm (keystrokes per minute averaged over last 60s)
app_switches <= 2 (in last 5 minutes)
max_idle_gap <= 4s (longest idle gap in last 5 minutes)
Flow OFF (if any condition persists for 30s):
typing_rate < 30 kpm OR
app_switches > 2 OR
max_idle_gap > 6s
All thresholds exposed as user-configurable settings in the dashboard.
6 — macOS-specific permissions & APIs (what the installer must prompt for)
Accessibility (AX) permission — to monitor keyboard/mouse and detect foreground app reliably. Explain: “Needed to measure typing cadence and app focus to detect flow.”
Notification permission — to show micro-intervention prompts (optional).
Network — only for local HTTP server; no external network for MVP.
Code-signing/notarization — required before public distribution (later).
7 — Data model (conceptual, no SQL shown)
Sessions: id, start_ts, end_ts, start_app, end_app, avg_typing_rate, max_idle_gap, trigger_reason, notes
Events: ts, type (keystroke, app_switch, idle, flow_on, flow_off), payload (JSON)
Retention policy: local DB rolling window for raw events (keep last 30 days or user-configurable).
8 — Chrome extension contract (how Agent and extension interact)
Message channel: Agent posts enable/disable commands to extension (local message via native messaging or a small websocket between agent and extension).
Behavior:
On enable: extension switches to blocking mode for configured domains.
On disable: extension restores browsing.
User settings: editable blocklist in extension + an integrated quick whitelist accessible via tray menu.
9 — Dashboard features (MVP screen-by-screen)
Home / Summary: Today’s total flow minutes, longest session, number of sessions.
Sessions List: Table with start, end, duration, dominant app, avg typing rate, reason ended. (Filter by day/week.)
Timeline View: Simple horizontal bars for each session on a day.
Settings: threshold values, blocklist, whitelist, toggle protection.
Export: Download CSV of sessions.
10 — Error states & user messaging (what to show)
If Accessibility permission not granted → show a concise how-to overlay explaining steps to enable with a “Retry” button.
If DND toggle fails → show a non-blocking banner in menu: “Flow active but could not enable DND — click to retry.”
If Chrome extension not installed → menu shows “Install Chrome Helper” with a one-click link/instructions.
11 — Acceptance tests (manual QA checklist — copy/paste)
Test A — Flow entry
Simulate steady typing (40+ kpm) for 5 minutes with no app switching → expected: Flow ON, DND enabled, extension blocks sites, session logged.
Test B — Flow break by switch
While in flow, switch apps 4 times in 30 seconds → expected: Flow OFF within 30s, DND disabled, session closed.
Test C — Idle break
While in flow, create a 10s idle → expected: Flow OFF, DND disabled, session logged.
Test D — Whitelist
Add a site to whitelist and trigger flow → visiting that site does not get blocked.
Test E — Permission denied flow
Deny Accessibility permission on install → app should show instructions and not crash.
12 — Security & privacy checklist
Store DB under user-specific application data folder with file permissions set to user-only.
No remote telemetry in MVP. If later enabling analytics, require explicit opt-in and anonymize data.
Allow user to delete all data from Settings.
13 — Packaging & distribution notes (non-code)
Development: local signed builds with developer signing cert.
User distribution (later): notarize installer for macOS to avoid Gatekeeper blocks.
For initial user testing, provide instructions for granting Accessibility permission and installing the Chrome extension manually.
14 — Minimal acceptance & success metrics for MVP
Functional: Detects flow and toggles DND + blocking in 9/10 simulated sessions.
Reliability: Agent runs continuously with <5% CPU impact on average.
UX: Testers report that automatic protection triggered at appropriate times and they could easily override.
Adoption metric (test group): >50% of testers use the app for at least one session per day during a 1-week pilot.
15 — Two-week sprint plan (day-by-day, non-code tasks included)
Week 1
Day 1: Finalize thresholds & UX copy. Prepare design mockups for menu + dashboard.
Day 2: Determine exact macOS permission prompts & write user-facing permission texts. Prepare extension manifest spec.
Day 3: Define DB schema and API contract between Agent ↔ Dashboard ↔ Extension. Create sequence diagrams.
Day 4–5: Implement agent event model and write acceptance tests (engineer task).
Week 2
Day 6–8: Implement flow rule engine, DND integration spec, extension messaging spec.
Day 9–10: Build dashboard wireframes & admin settings pages.
Day 11: QA run of acceptance tests and iterate.
Day 12–14: Packaging, create install instructions, onboard 5 pilot users, collect feedback.
16 — Risks & mitigations
Accessibility permission friction — mitigation: clear onboarding instructions with screenshots and Retry flow.
Chrome extension message reliability — mitigation: fallback to hosts-file temp edits with clear user consent (warn about sudo).
False positives (entering flow when not) — mitigation: conservative thresholds and visible menu status + quick override.
OS updates breaking APIs — mitigation: keep error handling and telemetry (opt-in) to catch issues early.
17 — Deliverables for handoff (what engineers/designers get)
UX mockups for menu + dashboard (PNG/Figma links).
Sequence diagrams for event flows (Agent → Extension → Dashboard).
Configurable thresholds & default values (as above).
Acceptance test scripts and QA checklist (above).
Installer & permission guide for macOS testers.

Build a macOS background agent + Chrome helper + local dashboard that:
Detects user flow state (rule-based) using local behavioural signals,
Protects flow by toggling Do-Not-Disturb and commanding the Chrome extension to block distraction domains,
Logs sessions and events into Supabase (local) for analytics and dashboard display,
Provides a local web dashboard to view sessions and adjust settings.
Supabase runs locally (Docker) as the project DB/auth/edge-for-local usage only — privacy-first: data remains on the user’s machine or local network.
High-level architecture (components & interactions)
Agent (macOS background app, user-mode)
Collects keyboard/mouse events, foreground-window changes, idle gaps.
Applies the flow detection rule engine.
On Flow ON/OFF: toggles macOS DND, sends messages to Chrome extension (via Native Messaging or local websocket), writes events/sessions to Supabase local.
Hosts a small local agent API for the dashboard to query status (e.g., http://localhost:XXXX/status) secured by local token.
Chrome Extension (Helper)
Blocks domains when the agent commands it to enable blocking.
Communicates via Chrome Native Messaging (preferred) or via local websocket to agent.
Maintains its own local blocklist (syncable with Supabase via dashboard if desired).
Dashboard (Local Web UI)
Single-page app served locally (e.g., Flask / Node/Express) or via Supabase Edge Functions (local).
Reads sessions/events from Supabase local; writes settings (thresholds, blocklist, whitelist) to Supabase.
Provides settings UI for thresholds, whitelists, manual toggles, and data export.
Supabase (Local)
Postgres DB + Realtime + Storage (no external network).
Stores sessions, events, user settings, blocklists, agent logs.
Optional local Auth (for initial test users) — but for MVP use local-only, token-based access to dashboard.
Installer / Tray UI
Minimal tray/menu UI to start/stop agent, show current state, quick whitelist, and open dashboard.
Optional: Local Worker / Scheduler
Background process for retention tasks, cleanup, and aggregated analytics.
Sequence (simplified): Agent → (Supabase local write) → Chrome Extension receives command → Dashboard reads Supabase.
Project repository structure (suggested — one repo)
One repo keeps things simple for an MVP. Use mono-repo layout with clear separation.
├─ README.md
├─ LICENSE
├─ .github/
│  ├─ workflows/
│  │  ├─ ci.yml
│  │  └─ release.yml
├─ infra/
│  ├─ supabase/
│  │  ├─ docker-compose.yml
│  │  ├─ supabase-config.toml (local)
│  │  └─ migrations/ (sql migration files)
│  └─ certs/ (dev self-signed certs if needed)
├─ agent/
│  ├─ spec.md (agent design)
│  ├─ package.json / pyproject.toml (dev metadata)
│  ├─ assets/
│  └─ resources/
│     └─ onboarding-screenshots/
├─ chrome-extension/
│  ├─ manifest.json
│  ├─ spec.md (native messaging contract)
│  ├─ ui/
│  └─ tests/
├─ dashboard/
│  ├─ ui/ (React/Vue)
│  ├─ server/ (API layer, optional)
│  ├─ spec.md (routes & auth)
│  └─ e2e-tests/
├─ docs/
│  ├─ onboarding.md
│  ├─ privacy.md
│  ├─ dev-setup.md
│  └─ qa-checklist.md
├─ scripts/
│  ├─ start-local.sh
│  ├─ stop-local.sh
│  └─ reset-db.sh
└─ tests/
   ├─ integration/
   └─ performance/
Notes:
Keep infra/supabase/migrations as canonical DB schema scripts (Postgres SQL).
agent/spec.md contains macOS permissions, accessibility actions, and exact native messaging protocol.
dashboard/server either connects directly to Supabase or proxies via a service account key (local only).
Tech stack (selected for macOS local-first MVP)
Agent: language that is comfortable for macOS system integration (team choice: Python or Swift/Node). (You chose no code; team decides exact language.)
Low-level input capture: use Accessibility API or global event taps.
DND toggle: AppleScript/NSUserNotification APIs or macOS preferences.
Dashboard UI: React (CRA/Vite) or lightweight static + vanilla JS for MVP.
Dashboard Server: Node.js (Express) or Python (Flask/FastAPI) minimal API — only if needed (otherwise UI connects directly to Supabase).
Browser Helper: Chrome Extension (Manifest v3) with Native Messaging host for direct agent-extension messaging.
Database & Realtime: Supabase local (Postgres + Realtime). Run via Docker Compose in infra/supabase.
Local Auth / Tokens: Supabase Auth (local) OR a simple static token for dashboard to query local Supabase (MVP: static token stored in local agent config with tight file permissions).
Packaging: macOS signed app (notarization later). For development: .app dev builds, distribution via DMG or signed PKG later.
CI: GitHub Actions for linting, tests, building artifacts. (See .github/workflows/ci.yml.)
Rationale summary:
Supabase provides Postgres + realtime + simple client SDKs for dashboard. Running it locally in Docker gives consistent dev/test environments while keeping data local.
Supabase local usage (how to operate & what to store)
Local setup:
infra/supabase/docker-compose.yml starts Postgres, Realtime, and Supabase API. Use fixed ports and credentials for local dev.
Migrations stored under infra/supabase/migrations/ and applied on start-local.sh.
Schemas (tables & sample columns)
Tables (canonical):
sessions
id (uuid, PK)
user_id (uuid/text) — optional; can default to local system id
start_ts (timestamptz)
end_ts (timestamptz, nullable)
start_app (text)
end_app (text)
avg_typing_rate (numeric)
max_idle_gap (numeric)
duration_seconds (int) — computed or backfilled
trigger_reason (text)
meta (jsonb) — extended info (OS version, agent version)
events
id (uuid, PK)
session_id (uuid, FK, nullable)
ts (timestamptz)
type (text: 'keystroke','app_switch','idle','flow_on','flow_off')
payload (jsonb) — counts, window snapshot
settings
id (uuid)
user_id
key (text)
value (jsonb)
Examples: thresholds, blocklist, whitelist
agent_logs
id, ts, level, message, meta
Indexes:
sessions(start_ts) for timeline queries,
events(session_id, ts) for efficient session event fetches.
Retention & cleanup:
Keep raw events for N days (configurable, default 30 days). Implement a daily cleanup job (cron or lightweight worker) to delete old events; keep aggregated session metrics indefinitely unless user deletes.
Security:
Run Supabase locally bound to localhost only. Protect with a service key used by the agent and dashboard (local-only). Do not expose externally in MVP.
Realtime:
Use Supabase Realtime to push flow_on and flow_off events to the dashboard for live UI updates.
API & contracts (Agent ↔ Supabase ↔ Extension ↔ Dashboard)
These are the exact, language-agnostic contracts you will implement.
Agent -> Supabase (writes)
POST /rpc/insert_event (or direct DB insert via client library)
payload: { ts, type, payload }
POST /rpc/start_session
payload: { start_ts, start_app, meta } → returns session_id
POST /rpc/end_session
payload: { session_id, end_ts, end_app, avg_typing_rate, max_idle_gap, trigger_reason }
Use Supabase client or direct SQL inserts (via migrations). All writes authenticate with local service key.
Agent ↔ Chrome Extension
Preferred: Native Messaging Host contract
Agent registers as native messaging host with name com.flowfacilitator.helper.
Messages (JSON) from Agent → Extension:
{"cmd":"enable_blocking","domains":["youtube.com","reddit.com"], "ttl_seconds": 3600}
{"cmd":"disable_blocking"}
{"cmd":"update_blocklist","domains":[...]}
Messages from Extension → Agent:
{"event":"block_attempt","domain":"twitter.com","ts":...} (optional for analytics)
{"event":"extension_installed"}
Fallback: Websocket between extension and agent (if native messaging is not feasible during development).
Dashboard -> Supabase (reads & writes)
Dashboard uses Supabase client to:
Query sessions: select * from sessions where start_ts >= <day start> order by start_ts desc
Query events for session: select * from events where session_id = <id> order by ts
Update settings: upsert into settings table
Export CSV: aggregate via SQL
Authentication:
Dashboard uses a short-lived token created by agent at startup or a per-installation static service key stored in agent config with local file permissions.
Agent design & internals (spec not code)
Modules
Input Collector — captures:
Keystroke timestamps (no content)
Mouse events (movement timestamps)
Foreground app detection events
Idle detector (time since last input)
Rolling Metrics Engine — maintains sliding windows (last 60s, 300s) and computes:
typing_rate (kpm)
app_switch_count (per window)
max_idle_gap (seconds)
Flow Rule Engine — applies the thresholds:
Configurable parameters: flow_entry_window, typing_threshold_on, typing_threshold_off, switch_threshold, idle_threshold_on, idle_threshold_off, off_delay_seconds.
Emits flow_on and flow_off events.
Protection Controller — executes actions on Flow ON/OFF:
Toggle macOS Do-Not-Disturb (DND)
Send command to Chrome extension (Native Messaging)
Update local tray UI state
Persistence Layer — writes events and sessions to Supabase local (via client libs)
Local API / Admin — small HTTP interface for dashboard to query agent status and allow quick overrides (start/stop protection/whitelist), secured by token.
Logging & Health — local logs written to ~/Library/Application Support/FlowFacilitator/logs/ plus agent_logs table in Supabase for aggregated diagnostics.
Operational behavior:
On startup: check Supabase connectivity; if unavailable, run in offline mode and buffer writes locally until DB available.
On permission denial: present onboarding steps via tray to open System Settings and guide enabling Accessibility permission.
User flows (detailed)
Design the user experience flows for installation, onboarding, normal use, and failure states.
1. Install & First Run
User downloads dev build or installer.
User launches app → tray/menu icon appears.
App prompts user for Accessibility permission with short justification text:
“FlowFacilitator needs Accessibility permission to measure typing cadence and detect app focus so it can help you enter & protect flow. We DO NOT record typed text.”
App checks Supabase local; if not running, prompts to start local infra or runs bundled Supabase (via Docker).
App offers a quick tour and default blocklist. Optionally, one-click to install Chrome extension.
2. Normal passive use (happy path)
User opens their work app and starts working.
Agent collects input, computes rolling metrics.
After meeting Flow ON criteria for flow_entry_window (default 5 minutes), agent:
Emits flow_on, writes session start to Supabase,
Enables DND,
Sends enable_blocking to extension,
Tray icon changes color/state to “In Flow”.
User works uninterrupted.
When criteria for Flow OFF persist for off_delay_seconds (default 30s), agent:
Emits flow_off, writes session end to Supabase,
Disables DND,
Sends disable_blocking to extension,
Tray icon updates to “Idle/Working”.
Dashboard updates live with session.
3. User override and whitelist
User can open tray and press “Pause protection” (time-limited pause). The agent stops sending enable commands and temporarily allows browsing. This is recorded as an event.
User can whitelist a domain/app: updates Supabase settings, syncs to extension & agent.
4. Permission denied / error flows
If Accessibility permission denied: tray shows “Permissions required” with a button “Show how to enable” taking user to System Settings steps + retry button.
If Chrome extension not installed: tray shows “Install Chrome helper” with instructions and link to extension (for dev, local load).
If Supabase unreachable: agent starts in offline mode and buffer events; tray shows “Local DB offline — buffering” with option to start infra.
Developer workflows (setup, development, testing, release)
Provide exact workflows to onboard engineers and testers.
Local dev setup (one-time)
Clone repo.
Start local Supabase: scripts/start-local.sh (runs Docker Compose).
Apply DB migrations from infra/supabase/migrations.
Build the Chrome extension dev build and load unpacked in Chrome.
Launch agent in dev mode (reads dev config pointing at Supabase local).
Open Dashboard at http://localhost:3000 (or configured port).
Document all steps in docs/dev-setup.md with sample env vars and ports.
Feature development workflow (branching)
Use GitHub feature branches: feature/<short-desc>.
Pull request includes:
Updated infra migrations if DB changes,
Unit tests for any logic (agent metrics, rule engine),
Integration test plan if behavior affects extension or dashboard.
CI runs linting and unit tests. Integration tests with Supabase run in CI via Docker Compose.
Testing strategy
Unit tests: rule engine thresholds, rolling metrics calculations.
Integration tests: simulate keystroke sequences and foreground changes; assert flow_on/flow_off events written to Supabase.
End-to-end: run agent + extension + dashboard locally and execute acceptance scenarios (see QA section).
Manual QA: on multiple macOS versions (12, 13, 14 if available), test Accessibility flows, DND toggles, tray overrides, and extension messaging.
Release workflow (MVP testers)
Create a signed developer build for testers (ad-hoc). Provide installer and onboarding docs:
How to enable Accessibility,
How to load Chrome extension unpacked,
How to start local Supabase (for early testers provide bundled dev infra or instructions).
Collect feedback via a form or Slack; iterate quickly.
QA, acceptance tests & metrics (copy/paste test checklist)
Acceptance tests (MVP)
Flow entry (steady typing)
Simulate ~45 kpm continuously for 5 minutes, no app switches.
Expect: flow_on event, session start in Supabase, DND enabled, Chrome extension blocks domains.
Flow exit (app switching)
While in flow, perform >3 app switches within 30s.
Expect: flow_off within 30s, DND disabled, session end recorded.
Flow exit (idle)
While in flow, leave system idle for 10s.
Expect: flow_off and session end.
Override / Pause
User selects Pause protection for 10 minutes.
Expect: No new blocking, flow detection still logs but protection suppressed.
Whitelist behavior
Add example.com to whitelist in dashboard. Trigger flow and visit the site.
Expect: extension does not block example.com.
Permission denial handling
Deny Accessibility permission. Agent should show clear instructions and not crash.
Offline DB buffering
Stop Supabase while agent is running; generate events. Start Supabase again.
Expect: buffered events are written and sessions reconcile correctly.
Performance & Reliability
Agent CPU < 3% typical, <10% worst-case on dev machines.
Memory footprint reasonable (<150MB ideally).
Agent restarts gracefully; session continuity maintained or properly closed.
Pilot metrics
% of test users who used app at least once per day in a 7-day pilot.
Median session duration and number of sessions per day.
False positive rate (user-reported inappropriate Flow ON) < 10% in pilot.
Security & privacy (must-have rules)
Local only by default: Supabase runs bound to localhost; no external network access in MVP. Make this explicit in UI and docs.
No keystroke content: store only timestamps and counts. Never persist key contents; state this clearly in privacy.md.
Data at rest: DB files stored under ~/Library/Application Support/FlowFacilitator/ or user-specified location. Ensure file permissions are user-only.
Service key handling: store Supabase service key in a local config file with strict file permissions; rotate keys in dev as needed.
Delete data: allow user to delete all data from settings. Implement DB truncation via safe API that requires explicit user confirmation.
Auditing: store agent logs in agent_logs table for debugging. Include an opt-in for sending anonymized crash/health reports for future improvements (opt-in, not default).
Packaging & distribution (notes)
Dev builds: provide unsigned dev .app bundles or signed with developer cert for testers to reduce Gatekeeper friction.
Production: sign with Apple Developer ID and notarize app for distribution. Include a clear installer and manual for enabling Accessibility.
Chrome extension: distributed via Chrome Web Store later. For pilot, instruct testers to load the extension unpacked (developer mode).
Bundling Supabase: for non-technical testers, provide a helper script or a small bundled Supabase service (Docker) and an easy “Start local DB” button from the tray that runs docker compose up -d (with clear instructions that Docker must be installed). Alternatively, run Supabase in a lightweight embedded Postgres if the team chooses.
Developer handoff deliverables (what you should produce & include)
docs/dev-setup.md — exact commands to run local Supabase, start agent, load extension, open dashboard.
infra/supabase/migrations/ — SQL schema and initial data (blocklist examples, settings).
agent/spec.md — event formats, native messaging contract, onboarding copy for permissions.
chrome-extension/spec.md — manifest, message contract, behavior for block/allow.
dashboard/spec.md — routes, queries, UI wireframes for home/sessions/settings.
qa-checklist.md — acceptance test scripts.
onboarding.md — user-facing step-by-step guides (screenshots) for first-run permission grants.
privacy.md — short privacy statement for users, explicit about no content capture and local-only storage.
Example dev/test dataset with synthetic events to simulate flow sessions for integration testing