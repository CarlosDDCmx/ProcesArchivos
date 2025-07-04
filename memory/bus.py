from collections import defaultdict
from typing import Callable, Any, Type, Dict, List

Callback = Callable[[Any], None]  # Tipo para las funciones callback

class MemoryBus:
    # Diccionario: tipo de evento → lista de callbacks suscritos
    _subs: Dict[Type, List[Callback]] = defaultdict(list)

    @classmethod
    def subscribe(cls, evt_type: Type, cb: Callback) -> None:
        """Suscribe un callback a un tipo de evento."""
        cls._subs[evt_type].append(cb)

    @classmethod
    def unsubscribe(cls, evt_type: Type, cb: Callback) -> None:
        """Desuscribe un callback de un tipo de evento."""
        cls._subs[evt_type].remove(cb)

    @classmethod
    def emit(cls, evt: Any) -> None:
        """Emite un evento para ser recibido por suscriptores compatibles."""
        for cb in cls._subs.get(type(evt), []):
            cb(evt)
