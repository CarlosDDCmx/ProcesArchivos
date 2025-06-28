from pathlib import Path
from zipfile import ZipFile, BadZipFile
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Dict
from utils.i18n.safe import safe_gettext as _


class InvalidZipFile(Exception):
    """Excepción para ZIP no válidos."""


def read_zip_entry(path: str | Path, entry_name: str) -> bytes:
    """Lee una entrada individual dentro de un archivo ZIP."""
    path = Path(path)
    try:
        with ZipFile(path) as zf:
            return zf.read(entry_name)
    except BadZipFile as exc:
        raise InvalidZipFile(_("loader_error").format(error=str(exc))) from exc


def read_multiple_zip_entries(
    path: str | Path,
    names: Iterable[str],
    workers: int = 4,
) -> Dict[str, bytes]:
    """
    Lee varias entradas de forma concurrente y devuelve un dict nombre→bytes.
    """
    path = Path(path)
    if workers <= 0:
        # Lectura secuencial (útil para depuración)
        return {name: read_zip_entry(path, name) for name in names}

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {
            pool.submit(read_zip_entry, path, name): name for name in names
        }
        return {futures[f]: f.result() for f in futures}