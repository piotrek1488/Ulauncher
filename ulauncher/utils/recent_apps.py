"""
Helpers for the "frequent apps" feature.

Besides the dedicated `recent-apps-*` settings, the number of frequent apps can also
carry the layout, so that it can be changed from the Preferences UI text field, e.g.
"4 grid" or "6 list".
"""

LAYOUT_LIST = 'list'
LAYOUT_GRID = 'grid'
LAYOUTS = (LAYOUT_LIST, LAYOUT_GRID)

DEFAULT_NUMBER = 3


def parse_recent_apps_value(value, default=DEFAULT_NUMBER):
    """
    :param value: raw value of the `show-recent-apps` setting
    :param int default: used when the number cannot be parsed
    :rtype: tuple(int, str or None)
    :returns: number of apps to show and the layout override (None if not given)
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


def format_recent_apps_value(number, layout=None):
    """
    Inverse of :func:`parse_recent_apps_value`
    """
    if layout in LAYOUTS and layout != LAYOUT_LIST:
        return '%s %s' % (number, layout)
    return str(number)
