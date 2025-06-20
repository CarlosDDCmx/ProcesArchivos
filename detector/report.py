from utils.i18n.safe import safe_gettext as _

def report_result(result: dict, logger):
    logger.info(_("reporte_ruta").format(path=result["path"]))
    logger.info(_("reporte_bytes").format(size=result["size"]))
    logger.info(_("reporte_b_leido").format(header_bytes=result["header_bytes"]))
    logger.info(_("reporte_encabezado").format(header=result["header"]))
    logger.info(_("reporte_extension").format(extension=result["extension"]))
    logger.info(_("reporte_MIME").format(mime_type=result["mime_type"] or "N/A"))
    logger.info(_("reporte_tipo").format(detected_type=result["detected_type"]))