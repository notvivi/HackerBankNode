import re
from application.dtos.parsed_command import ParsedCommand
from application.dtos.validation_error import ValidationError

ACCOUNT_RE = re.compile(r"^(\d{5})/(\d+\.\d+\.\d+\.\d+)$")

def parse(raw: str) -> ParsedCommand:
    parts = raw.strip().split()

    if not parts:
        raise ValidationError("Empty command")

    code = parts[0]

    match code:
        case "BC" | "BA" | "BN":
            if len(parts) != 1:
                raise ValidationError("Invalid command format")
            return ParsedCommand(code=code)

        case "AC":
            if len(parts) != 2:
                raise ValidationError("Invalid AC format")
            try:
                account_str, ip_str = parts[1].split("/")
                account_number = int(account_str)
            except ValueError:
                raise ValidationError("Account number must be integer")
            return ParsedCommand(code=code, account=account_number, bank_ip=ip_str)
        case "AB" | "AR":
            if len(parts) != 2:
                raise ValidationError("Invalid command format")

            m = ACCOUNT_RE.match(parts[1])
            if not m:
                raise ValidationError("Invalid account format")

            return ParsedCommand(
                code=code,
                account=int(m.group(1)),
                bank_ip=m.group(2),
            )

        case "AD" | "AW":
            if len(parts) != 3:
                raise ValidationError("Invalid command format")

            m = ACCOUNT_RE.match(parts[1])
            if not m:
                raise ValidationError("Invalid account format")

            if not parts[2].isdigit():
                raise ValidationError("Invalid amount")

            return ParsedCommand(
                code=code,
                account=int(m.group(1)),
                bank_ip=m.group(2),
                amount=int(parts[2]),
            )

        case _:
            raise ValidationError("Unknown command")

