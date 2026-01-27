from application.commands.bc import BankCodeCommand
from application.commands.ac import CreateAccountCommand
from application.commands.ad import DepositCommand
from application.commands.aw import WithdrawCommand
from application.commands.ab import BalanceCommand
from application.commands.ar import RemoveAccountCommand
from application.commands.ba import BankTotalAmmountCommand
from application.commands.bn import BankNumberClientCommand

class CommandFactory:
    def __init__(self, local_ip: str, repo, proxy):
        self._local_ip = local_ip
        self._repo = repo
        self._proxy = proxy

    def create(self, parsed):
        match parsed.code:
            case "BC":
                return BankCodeCommand(self._local_ip)

            case "AC":
                return CreateAccountCommand(
                    account_number=parsed.account,
                    bank_ip=self._local_ip,
                    local_ip=self._local_ip,
                    repo=self._repo,
                    proxy=self._proxy,
                )

            case "AD":
                return DepositCommand(
                    account=parsed.account,
                    bank_ip=parsed.bank_ip,
                    amount=parsed.amount,
                    local_ip=self._local_ip,
                    repo=self._repo,
                    proxy=self._proxy,
                )

            case "AW":
                return WithdrawCommand(
                    account=parsed.account,
                    bank_ip=parsed.bank_ip,
                    amount=parsed.amount,
                    local_ip=self._local_ip,
                    repo=self._repo,
                    proxy=self._proxy,
                )

            case "AB":
                return BalanceCommand(
                    account=parsed.account,
                    bank_ip=parsed.bank_ip,
                    local_ip=self._local_ip,
                    repo=self._repo,
                    proxy=self._proxy,
                )

            case "AR":
                return RemoveAccountCommand(
                    account_number=parsed.account,
                    bank_ip=parsed.bank_ip,
                    local_ip=self._local_ip,
                    repo=self._repo,
                    proxy=self._proxy,
                )

            case "BA":
                return BankTotalAmmountCommand(
                    repo=self._repo,
                    bank_ip=parsed.bank_ip,
                    local_ip=self._local_ip,
                    proxy=self._proxy
                )

            case "BN":
                return BankNumberClientCommand(
                    repo=self._repo,
                    bank_ip=parsed.bank_ip,
                    local_ip=self._local_ip,
                    proxy=self._proxy
                )

            case _:
                raise RuntimeError("Command not supported")

