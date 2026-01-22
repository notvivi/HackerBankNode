# Contributing Guide
## This document describes the rules and workflow for contributing.

To get started, clone repository with `git clone https://github.com/notvivi/HackerBankNode.git`.
Create a new branch from `main` for your changes. We use Trunk-Based Development with short-lived feature branches.

Branch naming convention:
- `feature/<short-description>`,
- `fix/<short-description>`,
- `refactor/<short-description>`,
- `docs/<short-description>`.

Examples:
- `feature/authentication`,
- `fix/null-reference`,
- `docs/api-readme`.

## We follow Conventional Commits for commit messages.
Format: `<type>(optional-scope): <description>`.

Types include:
- `feat` for new features,
- `fix` for bug fixes,
- `refactor` for code refactoring,
- `docs` for documentation,
- `test` for tests,
- and `chore` for maintenance.

Examples:
- `feat(auth): add JWT authentication`,
- `fix(api): handle null user case`,
- `refactor(core): simplify validation logic`.

Before creating a Pull Request, make sure the code builds successfully, all tests pass, code follows project style, and your branch is up to date with `main`. PRs should contain small, focused changes with a clear description of what was done. Link related issues if applicable. Each PR must be reviewed by at least one teammate. Address all review comments before merging. Prefer squash merge to keep history clean. Follow the existing coding style, write tests for new features, and avoid large unrelated changes in one PR. When creating an issue, provide a description of the problem or feature, steps to reproduce if it's a bug, expected behavior, and screenshots/logs if applicable.
