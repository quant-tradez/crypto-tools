from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class SymbolStats:
    symbol: str
    percent_change: float
    relative_volume: float
