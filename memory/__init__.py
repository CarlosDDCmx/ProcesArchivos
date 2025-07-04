from collections import defaultdict
from pathlib import Path
from typing import Dict, List
from memory.events import FileAnalyzed, DetectedFamily

_registry: Dict[DetectedFamily, List[FileAnalyzed]] = defaultdict(list)
_active_event: FileAnalyzed | None = None

# ── API pública ──────────────────────────────────────────────────────────
def add_event(evt: FileAnalyzed) -> None:
    """Añade un evento al registro y lo marca como activo."""
    _registry[evt.family].append(evt)
    set_active_event(evt)

def get_registry() -> Dict[DetectedFamily, List[FileAnalyzed]]:
    """Devuelve la estructura completa {family: [events…]}."""
    return _registry

def list_events() -> List[FileAnalyzed]:
    """Devuelve todos los eventos en una lista plana (orden cronológico)."""
    return [e for eventos in _registry.values() for e in eventos]

def family_exists(family: DetectedFamily) -> bool:
    """True si existen eventos de la familia dada."""
    return family in _registry and bool(_registry[family])

def set_active_event(evt: FileAnalyzed) -> None:
    """Selecciona el evento sobre el que operarán los comandos de lectura."""
    global _active_event
    _active_event = evt

def get_active_event() -> FileAnalyzed | None:
    """Devuelve el evento activo actual (o None)."""
    return _active_event

# ── Re‑export para comodidad ──────────────
from memory.bus import MemoryBus  