"""
Manejo de documentos ODT.
"""

from ofimatic.loader_opendoc import read_opendocument, stats_opendoc, metadata_opendoc

def read_odt(path):
    return read_opendocument(path)

def stats_odt(data):
    return stats_opendoc(data)

def metadata_odt(path):
    return metadata_opendoc(path)
