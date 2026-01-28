class ParsedCommand:
    def __init__(
        self,
        code: str,
        account: int | None = None,
        bank_ip: str | None = None,
        amount: int | None = None,
        connection_count: int | None = None
    ):
        self.code = code
        self.account = account
        self.bank_ip = bank_ip
        self.amount = amount
        self.connection_count = connection_count

