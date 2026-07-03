# SciSiteForge AgentOS Entry Point

Last reviewed: 2026-06-27

This repository follows the host-level AgentOS configuration at
`/home/netuser/.agentos`.

Overlay: `scisiteforge`

Default roles:

- `repository-engineer`
- `publication-operator`
- `security-operator`

Required checks:

- `public-release`
- `operations-security`
- `stale-context-audit`

Private by default:

- Workbench drafts.
- Model logs and translation queues.
- Private route plans.
- Raw source extraction.

Public release rule:

- Publish only generated, reviewed public artifact trees.
- Do not publish raw workspaces, model logs, translation queues, private
  workbench state, credentials, or local-only paths.

Before resumed complex work, public releases, or policy changes, run:

```sh
python3 /home/netuser/.agentos/automations/audit_stale_context.py
python3 /home/netuser/.agentos/automations/validate_agentos.py
```
