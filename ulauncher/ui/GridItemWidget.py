import logging
from typing import Any

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
# pylint: disable=wrong-import-position
from gi.repository import Gdk

from ulauncher.ui.ResultItemWidget import ResultItemWidget
from ulauncher.utils.display import get_monitor_scale_factor
from ulauncher.search.Query import Query

logger = logging.getLogger(__name__)

LABELS_NONE = 'none'
LABELS_NAME = 'name'
LABELS_SHORTCUT = 'shortcut'
LABELS_NAME_AND_SHORTCUT = 'name-and-shortcut'
LABEL_MODES = (LABELS_NONE, LABELS_NAME, LABELS_SHORTCUT, LABELS_NAME_AND_SHORTCUT)

DEFAULT_LABEL_MODE = LABELS_NAME_AND_SHORTCUT
DEFAULT_ICON_SIZE = 48


class GridItemWidget(ResultItemWidget):
    """
    Renders a result item as a tile: icon on top, optional name and/or
    "Alt+<key>" shortcut underneath. Used by the frequent apps grid.

    It is instantiated automagically if the following is done:
        - its name is set in .ui file in class attribute
        - __gtype_name__ is set to the same class name
        - this class is be imported somewhere in the code before .ui file is built
    """

    __gtype_name__ = "GridItemWidget"

    icon_size = DEFAULT_ICON_SIZE  # type: int
    label_mode = DEFAULT_LABEL_MODE  # type: str

    def configure(self, icon_size: int = DEFAULT_ICON_SIZE, label_mode: str = DEFAULT_LABEL_MODE) -> None:
        """
        Must be called before :meth:`initialize`
        """
        self.icon_size = max(16, int(icon_size))
        self.label_mode = label_mode if label_mode in LABEL_MODES else DEFAULT_LABEL_MODE

    def initialize(self, builder: Any, item_object: Any, index: int, query: Query) -> None:
        super().initialize(builder, item_object, index, query)
        self._apply_label_mode()

    def set_icon(self, icon):
        """
        Unlike the list layout, the grid renders bigger icons, so ask the result item
        for a pixbuf of the requested size and only fall back to the default one.
        """
        icon_wgt = self.builder.get_object('item-icon')
        if not icon_wgt:
            return

        scale_factor = get_monitor_scale_factor()
        pixbuf = None
        get_icon_at_size = getattr(self.item_object, 'get_icon_at_size', None)
        if callable(get_icon_at_size):
            try:
                pixbuf = get_icon_at_size(self.icon_size * scale_factor)
            except Exception:
                logger.exception('Could not load a %spx icon', self.icon_size)
        if not pixbuf:
            pixbuf = icon
        if not pixbuf:
            return

        icon_wgt.set_size_request(self.icon_size, self.icon_size)

        if scale_factor == 1:
            icon_wgt.set_from_pixbuf(pixbuf)
            return

        try:
            surface = Gdk.cairo_surface_create_from_pixbuf(pixbuf, scale_factor, self.get_window())
            icon_wgt.set_from_surface(surface)
        except (AttributeError, TypeError):  # Fallback for older GTK or unrealized window
            icon_wgt.set_from_pixbuf(pixbuf)

    def set_shortcut(self, text):
        shortcut = self.builder.get_object('item-shortcut')
        if shortcut:
            shortcut.set_text(text)

    def _apply_label_mode(self) -> None:
        show_name = self.label_mode in (LABELS_NAME, LABELS_NAME_AND_SHORTCUT)
        show_shortcut = self.label_mode in (LABELS_SHORTCUT, LABELS_NAME_AND_SHORTCUT)
        self._set_label_visible('item-name', show_name)
        self._set_label_visible('item-shortcut', show_shortcut)

    def _set_label_visible(self, object_id: str, visible: bool) -> None:
        widget = self.builder.get_object(object_id)
        if not widget:
            return
        # set_no_show_all keeps the label hidden when the parent calls show_all()
        widget.set_no_show_all(not visible)
        if visible:
            widget.show()
        else:
            widget.hide()
