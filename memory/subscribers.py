from memory.events import FileAnalyzed, ErrorEvent, DetectedFamily
from memory.bus import MemoryBus
from dataclasses import asdict
import json, logging
from pathlib import Path

# ── Registro principal de eventos por familia ─────────────────────────────
_REGISTRY: dict[DetectedFamily, list[FileAnalyzed]] = {}

def _registry_add(evt: FileAnalyzed) -> None:
    """Agrega un evento de análisis al registro."""
    _REGISTRY.setdefault(evt.family, []).append(evt)

def get_registry():
    """Devuelve el registro completo de análisis realizados."""
    return _REGISTRY

def family_exists(family: DetectedFamily) -> bool:
    """Verifica si hay archivos analizados de una familia específica."""
    return family in _REGISTRY

# ── Ruta donde se guardarán los archivos JSON con los análisis ───────────
_OUT = Path("results")
_OUT.mkdir(exist_ok=True)

def _persist(evt: FileAnalyzed):
    """Guarda los datos del evento como archivo JSON en disco."""
    data = asdict(evt)
    data["path"] = str(data["path"])
    data["family"] = data["family"].name
    dest = _OUT / f"{evt.path.name}.json"
    dest.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def _log_error(evt: ErrorEvent) -> None:
    """Registra errores personalizados desde eventos."""
    logging.error("[%s] %s", evt.origin, evt.message)

# ── Subscripciones automáticas ───────────────────────────────────────────
MemoryBus.subscribe(FileAnalyzed, _registry_add)
MemoryBus.subscribe(FileAnalyzed, _persist)
MemoryBus.subscribe(ErrorEvent,   _log_error)
