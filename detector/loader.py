import json
import os
from typing import Dict, List, Any, Tuple
from utils.i18n.safe import safe_gettext as _

def load_signatures() -> Tuple[Dict[bytes, str], List[Dict[str, Any]]]:
    """
    Devuelve un par (signatures_dict, ambiguous_list).

    • signatures_dict : dict[bytes, str]           cabecera → descripción
    • ambiguous_list  : list[dict[str, Any]]       reglas para heurística
    """
    # Ruta al JSON (misma carpeta que este archivo)
    sig_path = os.path.join(os.path.dirname(__file__), "signatures.json")
    try:
        with open(sig_path, encoding="utf-8") as fh:
            data = json.load(fh)
        # Firmas claras → bytes para comparación rápida
        signatures = {
            bytes.fromhex(hx.lower()): desc
            for hx, desc in data.get("signatures", {}).items()
        }
        # Firmas ambiguas tal cual
        ambiguous = data.get("ambiguous_signatures", [])
        return signatures, ambiguous

    except Exception as exc:
        # Mensaje definido en tu catálogo messages.po
        print(_("loader_error").format(error=str(exc)))
        return {}, []