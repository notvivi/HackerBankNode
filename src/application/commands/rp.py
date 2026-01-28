from application.services.robbery_planner import plan_robbery
from application.commands.base import Command

class RobberyPlanCommand(Command):
    def __init__(self, target: int, scanner):
        self.target = target
        self.scanner = scanner
        self.bank_list = []
        self.total = 0
        self.clients = 0
    async def execute(self) -> str:
        banks = await self.scanner.scan()

        if not banks:
            return "RP No banks were presented in the network"

        plan = plan_robbery(banks, self.target)

        if not plan:
            return (
                f"RP Could not reach {self.target}, "
                "even when rob every bank"
            )

        total = sum(b["total"] for b in plan)
        clients = sum(b["clients"] for b in plan)

        bank_list = ", ".join(
            f'{b["ip"]}:{b["port"]}' for b in plan
        )

        self.bank_list = bank_list
        self.total = total
        self.clients = clients

        return (
            f"RP For reaching {self.target} it is needed to rob"
            f"banks {bank_list}. "
            f"Total {total}, robbed {clients} clients."
        )

    def to_raw(self) -> str:
        return (
            f"RP For reaching {self.target} it is needed to rob"
            f"banks {self.bank_list}. "
            f"Total {self.total}, robbed {self.clients} clients."
        )


