from .bus import MemoryBus
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from memory.events import Event, FileAnalyzed, DetectedFamily

_registry: Dict[DetectedFamily, List[FileAnalyzed]] = defaultdict(list)
_active_event: FileAnalyzed | None = None


def add_event(evt: FileAnalyzed) -> None:
    """Guarda un nuevo evento en la memoria."""
    _registry[evt.family].append(evt)


def get_registry() -> Dict[DetectedFamily, List[FileAnalyzed]]:
    """Devuelve todo el registro (lectura)."""
    return _registry


def family_exists(family: DetectedFamily) -> bool:
    """Indica si existe al menos un evento de la familia dada."""
    return family in _registry and bool(_registry[family])


def set_active_event(evt: FileAnalyzed) -> None:
    """Define el archivo «principal» sobre el que actuarán los comandos."""
    global _active_event
    _active_event = evt


def get_active_event() -> FileAnalyzed | None:
    """Devuelve el evento marcado como activo (o None)."""
    return _active_event