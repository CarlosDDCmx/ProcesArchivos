from collections import defaultdict
from typing import Callable, Any, Type, Dict, List

Callback = Callable[[Any], None]

class MemoryBus:
    _subs: Dict[Type, List[Callback]] = defaultdict(list)

    @classmethod
    def subscribe(cls, evt_type: Type, cb: Callback) -> None:
        cls._subs[evt_type].append(cb)

    @classmethod
    def unsubscribe(cls, evt_type: Type, cb: Callback) -> None:
        cls._subs[evt_type].remove(cb)

    @classmethod
    def emit(cls, evt: Any) -> None:
        for cb in cls._subs.get(type(evt), []):
            cb(evt)
