import sys
import json
import logging
from .base import Command
from typing import List
from memory import get_registry, list_events, set_active_event
from dataclasses import asdict
from menu.navigator import Navigator
from utils.i18n.safe import safe_gettext as _

class ExitCommand(Command):
    def execute(self, navigator):
        print(_("salir"))
        sys.exit(0)


class SayHelloCommand(Command):
    def execute(self, navigator):
        print(_("saluda_usuario"))


class BackCommand(Command):
    def execute(self, navigator):
        navigator.back()


class ShowResultsCommand(Command):
    def execute(self, navigator):
        store = get_registry()
        if not store:
            print(_("sin_resultados"))
            return

        for fam, eventos in store.items():
            print(f"\n[{fam.name}]")
            for idx, evt in enumerate(eventos, 1):
                meta = evt.metadata
                print(f" {idx}. {meta['path']}  ->  {evt.detected_type}")

class SelectActiveCommand(Command):
    """Lista los archivos analizados y permite seleccionar el activo."""

    def execute(self, navigator: Navigator):
        eventos: List = list_events()
        if not eventos:
            print(_("sin_resultados"))
            return

        # Muestra lista numerada
        print(_("seleccionar_archivo_titulo"))
        for idx, evt in enumerate(eventos, 1):
            print(f"{idx}. {evt.path}  →  {evt.detected_type}")

        try:
            choice = int(input(_("eleccion_entra")))
            if not 1 <= choice <= len(eventos):
                raise ValueError
        except ValueError:
            print(_("error_no_valido"))
            return

        set_active_event(eventos[choice - 1])
        logging.info(_("archivo_activo_cambiado").format(path=eventos[choice - 1].path))

        # Refresca el menú actual para que se actualicen las opciones
        from menu.menus.tools_menu import build_tools_menu
        navigator.replace_current(build_tools_menu)

class MemoryInspectCommand(Command):
    def execute(self, navigator):
        MAX_PARAGRAPHS = 5
        MAX_TABLES = 2
        MAX_ROWS_PER_TABLE = 3
        MAX_STRING_LENGTH = 100
        MAX_LIST_ITEMS = 5
        MAX_DICT_ITEMS = 5

        def truncate_value(value):
            """Trunca strings largos, listas y diccionarios."""
            if isinstance(value, str):
                return value[:MAX_STRING_LENGTH] + ("…" if len(value) > MAX_STRING_LENGTH else "")
            elif isinstance(value, list):
                if len(value) > MAX_LIST_ITEMS:
                    return value[:MAX_LIST_ITEMS] + [f"... (+{len(value) - MAX_LIST_ITEMS} {_('elemen_omitidos')})"]
                return [truncate_value(v) for v in value]
            elif isinstance(value, dict):
                items = list(value.items())[:MAX_DICT_ITEMS]
                return {k: truncate_value(v) for k, v in items}
            return value

        def truncate_opendoc_docx_content(evt_dict):
            """Recorta contenido extenso de opendoc_data y docx_data."""
            metadata = evt_dict.get("metadata", {})

            for key in ("opendoc_data", "docx_data"):
                data = metadata.get(key)
                if not isinstance(data, dict):
                    continue

                # Truncar párrafos
                paragraphs = data.get("paragraphs")
                if isinstance(paragraphs, list) and len(paragraphs) > MAX_PARAGRAPHS:
                    data["paragraphs"] = (
                        paragraphs[:MAX_PARAGRAPHS]
                        + [f"... (+{len(paragraphs) - MAX_PARAGRAPHS} {_('parrafos_mas')})"]
                    )

                # Truncar tablas
                tables = data.get("tables")
                if isinstance(tables, list) and len(tables) > 0:
                    preview = []
                    for t in tables[:MAX_TABLES]:
                        preview.append(t[:MAX_ROWS_PER_TABLE])
                    if len(tables) > MAX_TABLES:
                        preview.append([["... (+{} {})".format(len(tables) - MAX_TABLES, _('tablas_mas'))]])
                    data["tables"] = preview

            return evt_dict

        registry = {
            fam.name: [
                truncate_value(
                    truncate_opendoc_docx_content(
                        asdict(evt) | {
                            "path": str(evt.path),
                            "family": evt.family.name
                        }
                    )
                )
                for evt in eventos
            ]
            for fam, eventos in get_registry().items()
        }

        print(json.dumps(registry, indent=2, ensure_ascii=False))
