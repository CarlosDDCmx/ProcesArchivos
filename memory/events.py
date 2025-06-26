from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Any

class DetectedFamily(Enum):
    OPENDOCUMENT = auto()     # ODT, ODS, ODP…
    OFFICE_ZIP   = auto()     # DOCX, XLSX, PPTX (OpenXML)
    PDF          = auto()
    IMAGE        = auto()
    ARCHIVE      = auto()     # ZIP, 7Z, RAR…
    AUDIO        = auto()
    VIDEO        = auto()
    EXECUTABLE   = auto()
    UNKNOWN      = auto()

@dataclass(frozen=True)
class FileAnalyzed:
    path: Path
    detected_type: str
    family: DetectedFamily
    metadata: dict[str, Any]

@dataclass(frozen=True)
class ErrorEvent:
    origin: str
    message: str