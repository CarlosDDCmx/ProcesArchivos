from pathlib import Path
from core.i18n import t

def read_file_header(file_path: str, num_bytes: int = 64) -> bytes:
    """
    Lee los primeros `num_bytes` del archivo especificado.

    :param file_path: Ruta al archivo a leer.
    :param num_bytes: Número de bytes a leer desde el inicio del archivo.
    :return: Bytes leídos del encabezado.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(t("file_not_found", file=file_path))
    if not path.is_file():
        raise ValueError(t("not_a_file", file=file_path))

    with open(path, "rb") as f:
        return f.read(num_bytes)