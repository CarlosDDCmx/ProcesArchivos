import builtins
from .i18n import get_translator

builtins._ = get_translator()