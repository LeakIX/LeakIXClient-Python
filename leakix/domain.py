import dataclasses
from datetime import datetime

from l9format.l9format import Model


@dataclasses.dataclass
class L9Subdomain(Model):
    subdomain: str = ""
    distinct_ips: int = 0
    last_seen: datetime | None = None
