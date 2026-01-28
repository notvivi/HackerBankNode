import json
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseConfig:
    sqlite_path: str


@dataclass(frozen=True)
class AppConfig:
    log_file: str
    port: int
    timeout: int
    ip_network: str
    ip_mask: int
    database: DatabaseConfig


def load_config(path: str) -> AppConfig:
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with config_path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    return AppConfig(
        log_file=raw["log_file"],
        port=raw["port"],
        timeout=raw["timeout"],
        ip_network=raw["ip_network"],
        ip_mask=raw["ip_mask"],
        database=DatabaseConfig(
            sqlite_path=raw["database"]["sqlite_path"]
        )
    )

