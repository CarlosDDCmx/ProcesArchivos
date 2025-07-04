# menu/navigator.py
#  Navegador que gestiona la pila de menús y la navegación entre ellos.

import logging
from utils.i18n.safe import safe_gettext as _
from typing import Callable
from menu.menu import Menu

class Navigator:
    def __init__(self):
        self.stack: list[Menu] = []
        self.expand_breadcrumb = False  # Opcional: mostrar rastro completo

    def go_to(self, menu_or_builder: Callable[[], Menu] | Menu):
        """Navega a un nuevo menú (objeto o constructor)."""
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
        """Vuelve al menú anterior si es posible."""
        if len(self.stack) > 1:
            self.stack.pop()
            self._show_current()

    def exit(self):
        """Finaliza el programa."""
        exit(0)

    def _show_current(self):
        """Muestra el menú actual en el tope de la pila."""
        if not self.stack:
            logging.error(_("error_menu_display"))
            return
        current = self.stack[-1]
        current.show(self)

    def toggle_breadcrumb(self):
        """Alterna si se muestra el breadcrumb completo o abreviado."""
        self.expand_breadcrumb = not self.expand_breadcrumb

    def get_breadcrumb(self):
        """Devuelve el rastro de navegación del menú actual."""
        titles = [menu.title for menu in self.stack if menu.title]
        if self.expand_breadcrumb or len(titles) <= 3:
            return _("→").join(titles)
        else:
            return _("→").join([titles[0], "…", titles[-1]])

    def replace_current(self, menu_or_builder: Callable[[], Menu] | Menu):
        """Reemplaza el menú actual por otro sin alterar el resto de la pila."""
        if not self.stack:
            logging.error(_("error_menu_display"))
            return
        self.stack.pop()
        self.go_to(menu_or_builder)
