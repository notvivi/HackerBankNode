#Author: Tomanová Vilma

def parse_command_responses(raw_response, allowed_commands=None):
    """
    Parses responses like:
        BA 3000
        BN 12
    Returns a dict {command: value}

    allowed_commands: optional set to filter commands
    """
    results = {}
    if allowed_commands is None:
        allowed_commands = {"BA", "BN", "BC", "CC"}

    for line in raw_response.splitlines():
        line = line.strip()
        parts = line.split()
        if len(parts) >= 2:
            cmd, value = parts[0], parts[1]
            if cmd in allowed_commands:
                results[cmd] = value
    return results
