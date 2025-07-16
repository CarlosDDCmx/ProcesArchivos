"""
Manejo de hojas de cálculo ODS.
"""

from ofimatic.loader_opendoc import read_opendocument, stats_opendoc, metadata_opendoc


def read_ods(path):
    """Delegado directo a lectura OpenDocument."""
    return read_opendocument(path)


def stats_ods(data):
    """Delegado directo a estadísticas OpenDocument."""
    return stats_opendoc(data)


def metadata_ods(path):
    """Delegado directo a metadatos OpenDocument."""
    return metadata_opendoc(path)
