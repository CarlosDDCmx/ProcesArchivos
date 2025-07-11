"""
Manejo de hojas de cálculo ODS.
"""

from ofimatic.loader_opendoc import read_opendocument, stats_opendoc, metadata_opendoc

def read_ods(path):
    return read_opendocument(path)

def stats_ods(data):
    return stats_opendoc(data)

def metadata_ods(path):
    return metadata_opendoc(path)