"""
Settings helpers and limits for the "frequent apps" feature.

The limits live here rather than next to the widget, so that the preferences routes, the
preferences UI and the renderer all clamp to the same values without the preferences
dialog having to import a GTK widget module.

The number of frequent apps is stored as a string, and historically also as a boolean.
On top of that, the Preferences text field accepts an optional layout, e.g. "4 grid",
as a shorthand for setting both at once. The layout is never stored there: it is split
off into the `recent-apps-layout` setting, so that there is a single source of truth.
"""

LAYOUT_LIST = 'list'
LAYOUT_GRID = 'grid'
LAYOUTS = (LAYOUT_LIST, LAYOUT_GRID)
DEFAULT_LAYOUT = LAYOUT_LIST

LABELS_NONE = 'none'
LABELS_NAME = 'name'
LABELS_SHORTCUT = 'shortcut'
LABELS_NAME_AND_SHORTCUT = 'name-and-shortcut'
LABEL_MODES = (LABELS_NONE, LABELS_NAME, LABELS_SHORTCUT, LABELS_NAME_AND_SHORTCUT)
DEFAULT_LABEL_MODE = LABELS_NAME_AND_SHORTCUT

DEFAULT_NUMBER = 3

DEFAULT_COLUMNS = 4
MIN_COLUMNS = 1
MAX_COLUMNS = 12

DEFAULT_ICON_SIZE = 48
MIN_ICON_SIZE = 16
MAX_ICON_SIZE = 128


def parse_recent_apps_value(value, default=DEFAULT_NUMBER):
    """
    :param value: raw value of the `show-recent-apps` setting
    :param int default: used when the number cannot be parsed
    :rtype: tuple(int, str or None)
    :returns: number of apps to show and the layout shorthand (None if not given)
    """
    if value is None or value is False:
        return 0, None
    if value is True:
        return DEFAULT_NUMBER, None

    parts = str(value).strip().lower().split()
    if not parts:
        return 0, None

    layout = None
    if len(parts) > 1 and parts[-1] in LAYOUTS:
        layout = parts[-1]
        parts = parts[:-1]
    elif len(parts) == 1 and parts[0] in LAYOUTS:
        # layout only, keep the default number
        return default, parts[0]

    try:
        number = int(parts[0])
    except ValueError:
        number = default

    return max(0, number), layout


def clamp(value, minimum, maximum, default):
    """
    Parses an integer setting and clamps it into range, falling back to `default`
    when it cannot be parsed.
    """
    try:
        return min(maximum, max(minimum, int(str(value))))
    except (TypeError, ValueError):
        return default


def clamp_columns(value):
    return clamp(value, MIN_COLUMNS, MAX_COLUMNS, DEFAULT_COLUMNS)


def clamp_icon_size(value):
    return clamp(value, MIN_ICON_SIZE, MAX_ICON_SIZE, DEFAULT_ICON_SIZE)
