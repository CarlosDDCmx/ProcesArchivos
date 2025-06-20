import os
import json
from utils.i18n.safe import safe_gettext as _

def load_signatures():
    """Carga las firmas mágicas desde el archivo JSON."""
    signatures_path = os.path.join(os.path.dirname(__file__), "signatures.json")
    try:
        with open(signatures_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            return {bytes.fromhex(k): v for k, v in raw.items()}
    except Exception as e:
        print(_("error_firmas_carga").format(error=str(e)))
        return {}