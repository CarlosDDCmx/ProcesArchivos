from memory.events import FileAnalyzed, ErrorEvent, DetectedFamily
from memory.bus import MemoryBus
from dataclasses import asdict
import json, logging
from pathlib import Path


_REGISTRY: dict[DetectedFamily, list[FileAnalyzed]] = {}

def _registry_add(evt: FileAnalyzed) -> None:
    _REGISTRY.setdefault(evt.family, []).append(evt)

def get_registry():
    return _REGISTRY

def family_exists(family: DetectedFamily) -> bool:
    return family in _REGISTRY

_OUT = Path("results"); _OUT.mkdir(exist_ok=True)

def _persist(evt: FileAnalyzed):
    data = asdict(evt)
    data["path"]   = str(data["path"])
    data["family"] = data["family"].name 
    dest = _OUT / f"{evt.path.name}.json"
    dest.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def _log_error(evt: ErrorEvent) -> None:
    logging.error("[%s] %s", evt.origin, evt.message)

MemoryBus.subscribe(FileAnalyzed, _registry_add)
MemoryBus.subscribe(FileAnalyzed, _persist)
MemoryBus.subscribe(ErrorEvent,   _log_error)