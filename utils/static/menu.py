def generate_banner(title: str, attrs: list, pad: int=2) -> str:
    """
    Genera un banner ASCII con bordes decorativos y contenido centrado

    Args:
        title (str): Texto del título (primera línea)
        attrs (list): Lista de textos para las líneas restantes
        pad (int): Espacio entre texto y borde (por defecto: 2)
    
    Returns:
        str: Banner formateado
    """
    max_width = max(len(title), max((len(a) for a in attrs))) # Calcular ancho máximo del banner
    width = max_width + pad * 2  # +4 por bordes y espacios
    lines = []
    lines.append(f"╔{'═' * (width - pad)}╗")
    line_title = title.center(width - pad)
    lines.append(f"║{line_title}║")
    lines.append(f"║{' ' * (width - pad)}║")
    
    # attrs centrados
    for attr in attrs:
        attr_linea = attr.center(width - pad)
        lines.append(f"║{attr_linea}║")
    
    # Borde inferior
    lines.append(f"╚{'═' * (width - pad)}╝")
    
    return "\n".join(lines)

MENU_BANNER = generate_banner(
        "ProcesArchivos",
        [
            "Procesador de Archivos Multi-formato",
            "Versión 1.0.0",
            "Carlos D. Díaz Cano",
            "carlosd.dc.mx@gmail.com"
        ], 10
    )