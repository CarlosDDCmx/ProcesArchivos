from .core import get_translator
import builtins

if not hasattr(builtins, "_"):
    builtins._ = lambda x: x

_ = builtins._
__all__ = ["get_translator", "_"]