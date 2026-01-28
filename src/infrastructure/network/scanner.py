import ipaddress
import asyncio

class OnDemandNetworkScanner:
    def __init__(self, config, proxy):
        self.timeout = config.timeout
        self.network = config.ip_network
        self.mask = config.ip_mask
        self.port_range = range(65525, 65536)
        self.proxy = proxy

    def iter_ips(self):
        net = ipaddress.ip_network(
            f"{self.network}/{self.mask}", strict=False
        )
        return [str(ip) for ip in net.hosts()]

    async def scan(self) -> list[dict]:
        banks = []
        tasks = []

        for ip in self.iter_ips():
            for port in self.port_range:
                print(f"{ip}:{port}")
                tasks.append(self._probe(ip, port, banks))

        await asyncio.gather(*tasks)
        return banks

    def parse_response(self, resp: str, expected_code: str) -> int:
        parts = resp.split(maxsplit=1)

        if len(parts) != 2 or parts[0] != expected_code:
            raise ValueError(f"Invalid response: {resp}")

        return int(parts[1])

    async def _probe(self, ip, port, result):
        try:
            if not await self.proxy.is_bank(ip, port, self.timeout):
                return

            total_raw = await self.proxy.raw(ip, port, "BA")
            clients_raw = await self.proxy.raw(ip, port, "BN")

            total = self.parse_response(total_raw, "BA")
            clients = self.parse_response(clients_raw, "BN")

            result.append({
                "ip": ip,
                "port": port,
                "total": int(total),
                "clients": int(clients)
            })
        except Exception as e:
            print(e)
            pass
