"""
Manejo de documentos de texto ODT.
"""

from ofimatic.loader_opendoc import read_opendocument, stats_opendoc, metadata_opendoc


def read_odt(path):
    """Delegado directo a lectura OpenDocument."""
    return read_opendocument(path)


def stats_odt(data):
    """Delegado directo a estadísticas OpenDocument."""
    return stats_opendoc(data)


def metadata_odt(path):
    """Delegado directo a metadatos OpenDocument."""
    return metadata_opendoc(path)
