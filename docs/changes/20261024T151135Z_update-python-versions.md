---
type: Change
title: Updated supported Python versions to 3.11-3.14
description: Dropped Python 3.10, added Python 3.14, and updated the project scaffolding from copier-UvScaffolding v0.5.11 to v0.5.14.
tags: [config, python, ci, release]
status: stable
generated: { by: claude-code/claude-opus-5-5, at: 2026-10-24T15:11:35Z }
sources:
  - { id: pyproject, resource: /pyproject.toml, title: pyproject.toml }
  - { id: copier-answers, resource: /.copier-answers.yml, title: .copier-answers.yml }
  - { id: cicd, resource: /.github/workflows/CICD.yml, title: CICD.yml }
  - { id: cicd-impl, resource: /.github/workflows/CICD_impl.yml, title: CICD_impl.yml }
  - { id: release-impl, resource: /.github/actions/release_impl/action.yml, title: release_impl/action.yml }
  - { id: development, resource: /DEVELOPMENT.md, title: DEVELOPMENT.md }
---

# Summary

Supported Python versions changed from 3.10-3.13 to 3.11-3.14:

- `requires-python` raised to `>= 3.11`; trove classifiers updated to match.
- CI matrix now tests 3.14, 3.13, 3.12, and 3.11; packages are built with 3.11.
- `uv.lock` regenerated, dropping 3.10-only backports (`async-timeout`, `backports-asyncio-runner`, `exceptiongroup`, `typing-extensions`, and others).

The project was also updated from copier-UvScaffolding `v0.5.11` to `v0.5.14`:

- `CICD.yml` gained a concurrency group so superseded PR runs are cancelled and push runs are never dropped; `python_package_version` was renamed `build_python_version`.
- `CICD_impl.yml` added job timeouts and renamed `package_coverage` to `postprocess_coverage`.
- The release action takes explicit inputs, retries network operations via `retry.sh`, keeps the signing key in a step-scoped temp file, and uploads to an existing release on rerun.
- `DEVELOPMENT.md` documents how commit messages control semantic version increments; `README.md` fixes the `.minisig` extension.

# Rationale

Python 3.10 is near end of life and Python 3.14 is released, so the supported range shifts forward by one version. Raising the minimum supported Python version changes who can install the package, so the release increments the minor version instead of the patch version. The scaffolding update brings in release reliability and security fixes from the template.
