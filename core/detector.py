import json
import zipfile
from typing import Optional
from core.i18n import t

def load_signatures(path: str = "data/signatures.json") -> dict[str, list[bytes]]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {k: [bytes.fromhex(sig) for sig in v] for k, v in raw.items()}

def detect_from_header(header: bytes, file_path: str, signatures: dict[str, list[bytes]]) -> Optional[str]:
    for tipo, patrones in signatures.items():
        for sig in patrones:
            if header.startswith(sig):
                if tipo == "ZIP":
                    return detect_opendocument_type(file_path)
                if tipo == "Microsoft Office 97-2003 (DOC, XLS, PPT)":
                    return detect_ole2_office_type(file_path)
                return tipo
    return None

def detect_opendocument_type(file_path: str) -> str:
    try:
        with zipfile.ZipFile(file_path) as z:
            if "mimetype" in z.namelist():
                mimetype = z.read("mimetype").decode("utf-8").strip()
                return {
                    "application/vnd.oasis.opendocument.text": t("odt"),
                    "application/vnd.oasis.opendocument.spreadsheet": t("ods"),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": t("docx"),
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": t("xlsx"),
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation": t("pptx")
                }.get(mimetype, t("zip_unknown"))
            else:
                return t("zip_no_mimetype")
    except Exception as e:
        return t("zip_invalid", error=str(e))

def detect_ole2_office_type(file_path: str) -> str:
    try:
        with open(file_path, "rb") as f:
            content = f.read()
        if b"WordDocument" in content:
            return t("doc")
        if b"Workbook" in content:
            return t("xls")
        if b"PowerPoint Document" in content:
            return t("ppt")
        return t("ole2_unknown")
    except Exception as e:
        return t("ole2_invalid", error=str(e))
