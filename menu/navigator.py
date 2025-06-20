import logging
from utils.i18n.safe import safe_gettext as _
from typing import Callable
from menu.menu import Menu

class Navigator:
    def __init__(self):
        self.stack: list[Menu] = []
        self.expand_breadcrumb = False

    def go_to(self, menu_or_builder: Callable[[], Menu] | Menu):
        try:
            if callable(menu_or_builder):
                menu = menu_or_builder()
            elif isinstance(menu_or_builder, Menu):
                menu = menu_or_builder
            else:
                raise TypeError(_("error_menu_go_to"))
        except Exception as e:
            logging.error(_("error_menu_const").format(error=str(e)))
            return

        logging.debug("...Breadcrumb: %s", self.get_breadcrumb())
        self.stack.append(menu)
        self._show_current()

    def back(self):
        if len(self.stack) > 1:
            self.stack.pop()
            self._show_current()

    def exit(self):
        exit(0)

    def _show_current(self):
        if not self.stack:
            logging.error(_("error_menu_display"))
            return
        current = self.stack[-1]
        current.show(self)

    def toggle_breadcrumb(self):
        self.expand_breadcrumb = not self.expand_breadcrumb

    def get_breadcrumb(self):
        titles = [menu.title for menu in self.stack if menu.title]
        if self.expand_breadcrumb or len(titles) <= 3:
            return _("→").join(titles)
        else:
            return _("→").join([titles[0], "…", titles[-1]])

