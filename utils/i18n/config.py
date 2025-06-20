try:
    import builtins
    _ = builtins._
except (ImportError, AttributeError):
    def _(message):
        return message