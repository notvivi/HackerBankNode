from application.commands.bc import BankCodeCommand
from application.commands.ac import CreateAccountCommand
from application.commands.ad import DepositCommand
from application.commands.aw import WithdrawCommand
from application.commands.ab import BalanceCommand
from application.commands.ar import RemoveAccountCommand
from application.commands.ba import BankTotalAmmountCommand
from application.commands.bn import BankNumberClientCommand

class CommandFactory:
    def __init__(self, local_ip: str):
        self._local_ip = local_ip

    def create(self, parsed, repo, proxy):
        match parsed.code:
            case "BC":
                return BankCodeCommand(self._local_ip)

            case "AC":
                return CreateAccountCommand(
                    local_ip=self._local_ip,
                    repo=repo,
                    proxy=proxy,
                )

            case "AD":
                return DepositCommand(
                    account=parsed.account,
                    bank_ip=parsed.bank_ip,
                    amount=parsed.amount,
                    local_ip=self._local_ip,
                    repo=repo,
                    proxy=proxy,
                )

            case "AW":
                return WithdrawCommand(
                    account=parsed.account,
                    bank_ip=parsed.bank_ip,
                    amount=parsed.amount,
                    local_ip=self._local_ip,
                    repo=repo,
                    proxy=proxy,
                )

            case "AB":
                return BalanceCommand(
                    account=parsed.account,
                    bank_ip=parsed.bank_ip,
                    local_ip=self._local_ip,
                    repo=repo,
                    proxy=proxy,
                )

            case "AR":
                return RemoveAccountCommand(
                    account_number=parsed.account,
                    bank_ip=parsed.bank_ip,
                    local_ip=self._local_ip,
                    repo=repo,
                    proxy=proxy,
                )

            case "BA":
                return BankTotalAmmountCommand(
                    repo=repo,
                    bank_ip=parsed.bank_ip,
                    local_ip=self._local_ip,
                    proxy=proxy
                )

            case "BN":
                return BankNumberClientCommand(
                    repo=repo,
                    bank_ip=parsed.bank_ip,
                    local_ip=self._local_ip,
                    proxy=proxy
                )

            case _:
                raise RuntimeError("Command not supported")

