from menu.menu import Menu
from menu.commands.odf_commands import (
    ReadODFContentCommand,
    StatsODFCommand,
    MetaODFCommand,
)
from menu.commands.concrete_command import BackCommand
from utils.i18n.safe import safe_gettext as _

def build_docs_menu() -> Menu:
    menu = Menu(title=_("menu_docs"))
    menu.add_command("1", ReadODFContentCommand(), _("docs_leer"))
    menu.add_command("2", StatsODFCommand(),      _("docs_stats"))
    menu.add_command("3", MetaODFCommand(),       _("docs_meta"))
    menu.add_command("0", BackCommand(),          _("volver"))
    return menu
