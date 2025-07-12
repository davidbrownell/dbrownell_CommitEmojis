**Project:**
[![License](https://img.shields.io/github/license/davidbrownell/dbrownell_CommitEmojis?color=dark-green)](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/master/LICENSE)

**Package:**
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbrownell_CommitEmojis?color=dark-green)](https://pypi.org/project/dbrownell_CommitEmojis/)
[![PyPI - Version](https://img.shields.io/pypi/v/dbrownell_CommitEmojis?color=dark-green)](https://pypi.org/project/dbrownell_CommitEmojis/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/dbrownell_CommitEmojis)](https://pypistats.org/packages/dbrownell_CommitEmojis)

**Development:**
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![CI](https://github.com/davidbrownell/dbrownell_CommitEmojis/actions/workflows/CICD.yml/badge.svg)](https://github.com/davidbrownell/dbrownell_CommitEmojis/actions/workflows/CICD.yml)
[![Code Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/davidbrownell/f15146b1b8fdc0a5d45ac0eb786a84f7/raw/dbrownell_CommitEmojis_code_coverage.json)](https://github.com/davidbrownell/dbrownell_CommitEmojis/actions)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/davidbrownell/dbrownell_CommitEmojis?color=dark-green)](https://github.com/davidbrownell/dbrownell_CommitEmojis/commits/main/)

<!-- Content above this delimiter will be copied to the generated README.md file. DO NOT REMOVE THIS COMMENT, as it will cause regeneration to fail. -->

## Contents
- [Overview](#overview)
- [Installation](#installation)
- [Development](#development)
- [Additional Information](#additional-information)
- [License](#license)

## Overview
`dbrownell_CommitEmojis` offers command line tools useful when creating git commit messages based on [gitmoji](https://gitmoji.dev/).

### How to use `dbrownell_CommitEmojis`

### Display

| Scenario | Command |
| --- | --- |
| Without installation | `uvx --from dbrownell_CommitEmojis commit_emojis Display` |
| When installed as a package dependency | `uv run commit_emojis Display` |

![Display screenshot](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/main/.github/Images/Display.png)

### Transform

| Scenario | Command |
| --- | --- |
| Without installation | `uvx --from dbrownell_CommitEmojis commit_emojis Transform <commit message>` |
| When installed as a package dependency | `uv run commit_emojis Transform <commit message> ` |

Examples for `<commit message>` are:

| Input | Output |
| --- | --- |
| :+project: Initial checkin | 🎉 [+project] Initial checkin |
| :+feature: A new feature was added | ✨ [+feature] A new feature was added |

See [Display](#display) for a list of all supported emoji and alias values.

<!-- Content below this delimiter will be copied to the generated README.md file. DO NOT REMOVE THIS COMMENT, as it will cause regeneration to fail. -->

## Installation

| Installation Method | Command |
| --- | --- |
| Via [uv](https://github.com/astral-sh/uv) | `uv add dbrownell_CommitEmojis` |
| Via [pip](https://pip.pypa.io/en/stable/) | `pip install dbrownell_CommitEmojis` |

### Verifying Signed Artifacts
Artifacts are signed and verified using [py-minisign](https://github.com/x13a/py-minisign) and the public key in the file `./minisign_key.pub`.

To verify that an artifact is valid, visit [the latest release](https://github.com/davidbrownell/dbrownell_CommitEmojis/releases/latest) and download the `.minisign` signature file that corresponds to the artifact, then run the following command, replacing `<filename>` with the name of the artifact to be verified:

```shell
uv run --with py-minisign python -c "import minisign; minisign.PublicKey.from_file('minisign_key.pub').verify_file('<filename>'); print('The file has been verified.')"
```

## Development
Please visit [Contributing](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/main/CONTRIBUTING.md) and [Development](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/main/DEVELOPMENT.md) for information on contributing to this project.

## Additional Information
Additional information can be found at these locations.

| Title | Document | Description |
| --- | --- | --- |
| Code of Conduct | [CODE_OF_CONDUCT.md](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/main/CODE_OF_CONDUCT.md) | Information about the norms, rules, and responsibilities we adhere to when participating in this open source community. |
| Contributing | [CONTRIBUTING.md](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/main/CONTRIBUTING.md) | Information about contributing to this project. |
| Development | [DEVELOPMENT.md](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/main/DEVELOPMENT.md) | Information about development activities involved in making changes to this project. |
| Governance | [GOVERNANCE.md](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/main/GOVERNANCE.md) | Information about how this project is governed. |
| Maintainers | [MAINTAINERS.md](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/main/MAINTAINERS.md) | Information about individuals who maintain this project. |
| Security | [SECURITY.md](https://github.com/davidbrownell/dbrownell_CommitEmojis/blob/main/SECURITY.md) | Information about how to privately report security issues associated with this project. |

## License
dbrownell_CommitEmojis is licensed under the <a href="https://choosealicense.com/licenses/MIT/" target="_blank">MIT</a> license.
