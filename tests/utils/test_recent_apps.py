from ulauncher.utils.recent_apps import parse_recent_apps_value, format_recent_apps_value


class TestParseRecentAppsValue:

    def test_disabled_values(self):
        assert parse_recent_apps_value(None) == (0, None)
        assert parse_recent_apps_value(False) == (0, None)
        assert parse_recent_apps_value('') == (0, None)
        assert parse_recent_apps_value('0') == (0, None)

    def test_legacy_boolean_true(self):
        assert parse_recent_apps_value(True) == (3, None)

    def test_number_only(self):
        assert parse_recent_apps_value('5') == (5, None)
        assert parse_recent_apps_value(7) == (7, None)

    def test_number_with_layout(self):
        assert parse_recent_apps_value('8 grid') == (8, 'grid')
        assert parse_recent_apps_value('6 list') == (6, 'list')

    def test_is_case_and_whitespace_insensitive(self):
        assert parse_recent_apps_value('  8   GRID  ') == (8, 'grid')

    def test_layout_only_keeps_default_number(self):
        assert parse_recent_apps_value('grid') == (3, 'grid')
        assert parse_recent_apps_value('grid', default=5) == (5, 'grid')

    def test_unknown_layout_is_ignored(self):
        assert parse_recent_apps_value('8 tiles') == (8, None)

    def test_falls_back_to_default_for_garbage(self):
        assert parse_recent_apps_value('junk') == (3, None)
        assert parse_recent_apps_value('junk', default=4) == (4, None)

    def test_negative_number_is_clamped(self):
        assert parse_recent_apps_value('-2') == (0, None)


class TestFormatRecentAppsValue:

    def test_grid_layout_is_appended(self):
        assert format_recent_apps_value(8, 'grid') == '8 grid'

    def test_list_layout_is_omitted(self):
        assert format_recent_apps_value(8, 'list') == '8'
        assert format_recent_apps_value(8, None) == '8'

    def test_round_trip(self):
        for value in ('0', '5', '8 grid'):
            number, layout = parse_recent_apps_value(value)
            assert format_recent_apps_value(number, layout) == value
