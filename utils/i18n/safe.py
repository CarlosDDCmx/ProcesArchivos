import builtins

def safe_gettext(message):
    """
    Traduce el mensaje si builtins._ está disponible; de lo contrario, lo devuelve sin traducir.
    """
    _ = getattr(builtins, "_", None)
    return _(message) if callable(_) else message
