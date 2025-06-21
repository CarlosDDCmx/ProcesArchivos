import os
import json
from utils.i18n.safe import safe_gettext as _

def load_signatures():
    """Carga firmas mágicas principales y ambiguas desde el archivo JSON."""
    signatures_path = os.path.join(os.path.dirname(__file__), "signatures.json")
    try:
        with open(signatures_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            main = {bytes.fromhex(k): v for k, v in data.get("signatures", {}).items()}
            ambiguous = data.get("ambiguous_signatures", [])
            return main, ambiguous
    except Exception as e:
        print(_("loader_error").format(error=str(e)))
        return {}, []