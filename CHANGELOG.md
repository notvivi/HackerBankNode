# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


### [0.1.0] - 2026-01-24
#### Added
- Added requirements.txt for pip env installation

#### Changed
- N/A

#### Deprecated
- N/A

#### Removed
- N/A

#### Fixed
- Python Github Actions CI pipeline for mypy, linters, black

#### Security
- N/A

### [0.1.0] - 2026-01-23
#### Added
- Added `AccountModel` ORM entity for database representation of bank accounts.
  - Columns: `id` (primary key), `number` (unique, non-null), `balance` (non-null).
- Added `Account` domain entity to encapsulate bank account business rules.
  - Enforces invariants: account number must be in range `[10000, 99999]`, balance must not be negative.
  - Read-only properties: `number`, `balance`.
  - Methods to modify state safely: `deposit(amount: int)` and `withdraw(amount: int)`.
  - Input validation for initial number and balance.
- Added `DomainError` exception handling in domain methods for invariant violations.
- Implemented docstrings for all classes and methods following detailed specifications.

#### Changed
- N/A

#### Deprecated
- N/A

#### Removed
- N/A

#### Fixed
- N/A

#### Security
- Direct modification of account state is prohibited; all changes must go through domain methods to maintain business invariants.

### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
