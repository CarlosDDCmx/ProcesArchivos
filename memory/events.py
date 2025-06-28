from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Any


class DetectedFamily(Enum):
    OPENDOCUMENT = auto()     # ODT, ODS, ODP…
    OFFICE_ZIP   = auto()     # DOCX, XLSX, PPTX
    PDF          = auto()
    IMAGE        = auto()
    ARCHIVE      = auto()     # ZIP, 7Z, RAR…
    DISK_IMAGES  = auto()     # ISO, DMG…
    AUDIO        = auto()
    VIDEO        = auto()
    EXECUTABLE   = auto()
    UNKNOWN      = auto()


# ── Evento base ──────────────────────────────────────────────────────────
@dataclass
class Event:
    """Clase base para todos los eventos."""


# ── Evento genérico tras detectar tipo de archivo ───────────────────────
@dataclass
class FileAnalyzed(Event):
    path: Path
    detected_type: str
    family: DetectedFamily
    metadata: Dict[str, Any]


# ── Evento específico para documentos ofimáticos ────────────────────────
@dataclass
class OfficeDocAnalyzed(FileAnalyzed):
    paragraphs: int
    tables: int | None = None
    embedded_objects: int | None = None


# ── Evento específico para imágenes ──────────────────────────────────────
@dataclass
class ImageAnalyzed(FileAnalyzed):
    width: int
    height: int
    color_space: str
    exif: Dict[str, Any] | None = None


# ── Evento para registrar errores ────────────────────────────────────────
@dataclass
class ErrorEvent(Event):
    origin: str
    message: str
