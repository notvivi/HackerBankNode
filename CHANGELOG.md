# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


### [0.1.0] - 2026-01-29
*Author: Tomanová Vilma*
#### Added
- N/A
#### Changed
- N/A
#### Deprecated
- N/A
#### Removed
- Removed exe file
  
#### Fixed
N/A
  
#### Security
- N/A

### [0.1.0] - 2026-01-28 and 2026-01-29
*Author: Tomanová Vilma*
#### Added
- Added readme
- Added documentation
- Added exe file
- Added ui monitoring visuals for bank
- Added client for retrieving data from the server
- Added parser for parsing commands
#### Changed
- N/A
#### Deprecated
- N/A

#### Removed
- N/A
- 
#### Fixed
- fixed getting data from config file
  
#### Security
- N/A


### [0.1.0] - 2026-01-28
*Author: Solonitsyn Maksym*
#### Added
- added command menu for each tcp connection
- added proxy
- added robery plan
#### Changed
- N/A
#### Deprecated
- N/A

#### Removed
- N/A

#### Fixed
- fix: fixed account number generation (#27)
- server timeout
- fixed text format for putty
- fixed account removal
- config path
#### Security
- N/A

### [0.1.0] - 2026-01-27
*Author: Solonitsyn Maksym*
#### Added
- Implement bank commands with domain logic
- Tcp command parsing and validation
#### Changed
- Dependency injection and logging setup
- Main entrypoint and settings cleanup
#### Deprecated
- N/A

#### Removed
- N/A

#### Fixed
- Db async session lifecycle and repository awaits
- Db commit error
- pip dependencies
- fixed fatal error logging
#### Security
- N/A

### [0.1.0] - 2026-01-27
*Author: Vilma Tomanová*
#### Added
- Added config.json error handling
- Added ip network and mask visuals in the ui
#### Changed
- N/A

#### Deprecated
- N/A

#### Removed
- N/A

#### Fixed
- Fixed config.json loading

#### Security
- N/A

### [0.1.0] - 2026-01-26
*Author: Vilma Tomanová*
#### Added
- Added ip network and ip mask into the config file
#### Changed
- N/A

#### Deprecated
- N/A

#### Removed
- N/A

#### Fixed
- Fixed exception error and import error

#### Security
- N/A

### [0.1.0] - 2026-01-25
*Author: Solonitsyn Maksym*
#### Added
- Added account repository
- Added database async sessions
- Added settings for parsing 'config.json' for database connection
#### Changed
- N/A

#### Deprecated
- N/A

#### Removed
- N/A

#### Fixed
- N/A

#### Security
- N/A

### [0.1.0] - 2026-01-25
*Author: Vilma Tomanová*
#### Added
- Added config file (log file path, port and timeout)
- Added script for managing file paths
- Added basic UI visuals for monitoring bank node
#### Changed
- N/A

#### Deprecated
- N/A

#### Removed
- N/A

#### Fixed
- N/A
#### Security
- N/A

### [0.1.0] - 2026-01-24
*Author: Solonitsyn Maksym*
#### Added
- Added requirements.txt for pip env installation
- Added unit test for testing banking account
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
*Author: Solonitsyn Maksym*
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
