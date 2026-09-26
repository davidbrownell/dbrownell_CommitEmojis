---
type: Change
title: Renamed CLAUDE.md to AGENTS.md
description: Moved agent instructions to the vendor-neutral AGENTS.md file and updated them to python_development template version 0.8.0.
tags: [config, agents, documentation]
status: stable
generated: { by: claude-code/claude-opus-5-5, at: 2026-09-26T22:02:05Z }
sources:
  - { id: agents-md, resource: /AGENTS.md, title: AGENTS.md }
---

# Summary

`CLAUDE.md` was removed and its content moved to `AGENTS.md`. The content was updated from template version 0.6.0 to `python_development` version 0.8.0:

- "SOLID" expanded to "SOLID design principles".
- Added a `## General` section under Python Development instructing that `python`-related tasks run through `uv`.

# Rationale

`AGENTS.md` is the vendor-neutral convention for coding-agent instructions, so a single file serves multiple agent tools rather than only Claude Code. The `uv` guidance prevents agents from invoking the system Python instead of the project environment.
