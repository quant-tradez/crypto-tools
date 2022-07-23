from dataclasses import dataclass
from typing import Dict

from dataclasses_json import dataclass_json

from domain.symbol_stats import SymbolStats


@dataclass_json
@dataclass
class SymbolStatsDict:
    stats: Dict[str, SymbolStats]
