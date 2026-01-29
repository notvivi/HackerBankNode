# Hacker bank node
`Authors: Maksym Solonitsyn, Vilma Tomanová`
- This project is P2P (peer-to-peer) node for banks, implemented using TCP/IP communication. 
- It has extension for hacking and robbing other banks.

## Requirements
- python 3.9.0 and more
- customtkinter 5.2.2
- sqlalchemy 2.0.25
- black 26.1.0
- mypy 1.8.0
- ruff 0.2.1
- pytest 8.0.0
- asyncio
- aiosqlite

## Key features
- Creating and managing bank accounts
- Deposits and withdrawals in USD$
- Persistent storage (Database in SQLite)
- TCP server with configurable `log file, port, timeout, ip network and mask`
- Robber plan command for hacking/robbing other banks
- `CustomTkinter UI` for node monitoring
- Logging

## Table of Contents
- [Installation](#installation)
- [Server Usage](#server-usage)
- [Client usage](#client-usage)
- [Configuration](#configuration)
- [Supported Commands](#supported-commands)
- [Workflow](#workflow)
- [Old project links](#old-project-links)
- [Documentation](#documentation)


## Installation
```bash
git clone https://github.com/notvivi/HackerBankNode.git
cd HackerBankNode/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Server Usage
1. Open a terminal and navigate to the project root directory and start the ui:
```bash
cd HackerBankNode/
python src/ui/app.py
```
2. To modify configuration parameters, select **Return to Configuration**, adjust the settings as needed, and save the changes.
3. Start the server by running:
```bash
python src/main.py
```

## Client usage
1. Open PuTTY.
2. Configure the connection with the following settings:
- Host Name (or IP address): Enter the server’s IP address.
- Port: Enter the server’s port number.
- Connection type: Select Raw.
- Click Open to establish the connection.
3. Once connected, type ui and press Enter to display all available server commands.


## Configuration
See example configuration: [`config.json`](src/config.json)

```json
{
  "log_file": "file-path.txt",
  "port": port-number,
  "timeout": timeout-number,
  "ip_network": "ip-network",
  "ip_mask": ip-mask,
  "database": {
    "sqlite_path": "db-connection"
  }
}
```
Explanation: 
- log_file - path to the log file where all application events are stored (`string`).
- port - TCP port on which the bank node listens for incoming connections (`integer`). 
- timeout - global timeout in seconds (`integer`).
- ip_network - base IP address of the local network used for P2P node discovery and communication (`string`).
- ip_mask - network mask defining the size of the IP network used by the P2P system (`integer`).
- database.sqlite_path - path to the SQLite database file used for **persistent storage** (`string`).

All configuration values are loaded at application startup.
Invalid or missing parameters result in application startup failure.

## Supported Commands

| Name                     | Code | Call                          | Success Response        | Error Response |
|--------------------------|------|-------------------------------|-------------------------|----------------|
| Bank code                | BC   | `BC`                          | `BC <ip>`               | `ER <message>` |
| Account create           | AC   | `AC`                          | `AC <account>/<ip>`     | `ER <message>` |
| Account deposit          | AD   | `AD <account>/<ip> <number>`  | `AD`                    | `ER <message>` |
| Account withdrawal       | AW   | `AW <account>/<ip> <number>`  | `AW`                    | `ER <message>` |
| Account balance          | AB   | `AB <account>/<ip>`           | `AB <number>`           | `ER <message>` |
| Account remove           | AR   | `AR <account>/<ip>`           | `AR`                    | `ER <message>` |
| Bank total amount        | BA   | `BA`                          | `BA <number>`           | `ER <message>` |
| Bank number of clients   | BN   | `BN`                          | `BN <number>`           | `ER <message>` |

Explanation:
- `<ip>` IP address in the format `0.0.0.0 - 255.255.255.255`, which is used as the **bank code** (used as **unique identifier** for each bank node).
- `<account>` A positive integer in the range `10000 to 99999`, which is used as the **bank account number** within a bank.
- `<number>` A non-negative integer in the range `0 to 9223372036854775807`

### Command extension for our assignment + bonus

| Name                  | Code | Call            | Success Response | Error Response |
|-----------------------|------|-----------------|------------------|----------------|
| Robbery plan (local)  | RP   | `RP <number>`   | `RP <message>`   | `ER <message>` |
| User interface        | ui   | `ui`            | `Bank header`    | `ER <message>` |


- RP 1000000
- Example response: `RP To reach 1000000$, banks 10.1.2.3 and 10.1.2.85 must be robbed, affecting only 21 clients.`

## Workflow
1. Client connects via TCP (PuTTY)
2. Command is received and validated
3. Command is: executed locally or proxied to another node
4. Response is returned to client
5. Client closes the connection

## Old project links
`Author: Tomanová Vilma`
- [User interface](https://github.com/notvivi/Debian-Autoconfig/blob/master/src/userinterface.py)
- [Relative paths](https://github.com/notvivi/Debian-Autoconfig/blob/master/lib/resource_path.py)
- [Documentation structure](https://github.com/notvivi/DatabaseManagementForShop/blob/main/doc/documentation.pdf)


## Documentation
- README.md – project overview and usage
- [CHANGELOG.md](CHANGELOG.md) – contribution log for team members
- [CONTRIBUTING.md](CONTRIBUTING.md) - tutorial for contribution into project
- [documentation.pdf](doc/documentation.pdf) - overall documentation (readme is shortened )
- [license](LICENSE) - used license for this project

####  Useful command: `pyinstaller --paths ../../lib --add-data "../../src/config.json;src" app.py`
