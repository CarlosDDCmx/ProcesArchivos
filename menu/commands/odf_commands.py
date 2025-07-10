import logging
from utils.i18n.safe import safe_gettext as _
from ofimatic.loader_opendoc import (
    read_opendocument,
    stats_opendoc,
    metadata_opendoc,
    OpenDocError,
)
from memory import get_active_event
from memory.bus import MemoryBus
from memory.events import OfficeDocAnalyzed, ErrorEvent
from .base import Command

logger = logging.getLogger(__name__)

# ── Command 1: Leer contenido ────────────────────────────────────────────
class ReadODFContentCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt:
            print(_("docs_no_activo"))
            return

        try:
            data = read_opendocument(evt.path)
            paragraphs = data.get("paragraphs", [])
            print("\n".join(paragraphs[:10]) + (" …" if len(paragraphs) > 10 else ""))
            evt.metadata["opendoc_data"] = data
            # Emitimos evento enriquecido
            MemoryBus.emit(
                OfficeDocAnalyzed(
                    path=evt.path,
                    detected_type=evt.detected_type,
                    family=evt.family,
                    metadata=evt.metadata,
                    paragraphs=len(paragraphs),
                )
            )
        except OpenDocError as exc:
            MemoryBus.emit(ErrorEvent(origin="ReadODF", message=str(exc)))

# ── Command 2: Estadísticas ──────────────────────────────────────────────
class StatsODFCommand(Command):
    """Muestra y guarda estadísticas del documento ODF activo."""

    def execute(self, navigator):
        evt = get_active_event()
        if not evt:
            print(_("docs_no_activo"))
            return

        # El dict con todo el contenido se guarda bajo la clave "opendoc_data"
        data = evt.metadata.get("opendoc_data")
        if not data:
            print(_("docs_data_missing"))
            return

        try:
            stats = stats_opendoc(data)
            evt.metadata["stats"] = stats

            # Salida amigable
            for k, v in stats.items():
                print(f"{k}: {v}")
        except Exception as exc:
            logger.exception(_("odf_stats_error").format(error=str(exc)))

# ── Command 3: Metadatos ─────────────────────────────────────────────────
class MetaODFCommand(Command):
    def execute(self, navigator):
        evt = get_active_event()
        if not evt:
            print(_("docs_no_activo"))
            return

        try:
            meta = metadata_opendoc(evt.path)
            evt.metadata["opendoc_meta"] = meta
            if not meta:
                print(_("odf_meta_error").format(error="meta.xml vacío o sin campos estándar"))
                return

            for k, v in meta.items():
                print(f"{k}: {v}")
        except Exception as exc:
            logger.exception(_("odf_meta_error").format(error=str(exc)))
