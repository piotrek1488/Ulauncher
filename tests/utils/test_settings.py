from ulauncher.utils.settings import Settings


class TestSettings:
    def test_defaults(self) -> None:
        assert Settings().theme_name == "light"
        assert Settings(theme_name="asdf").theme_name == "asdf"

    def test_recent_apps_defaults_to_the_list_layout(self) -> None:
        settings = Settings()
        assert settings.recent_apps_layout == "list"
        assert settings.recent_apps_grid_columns == 4
        assert settings.recent_apps_grid_labels == "name-and-shortcut"
        assert settings.recent_apps_grid_icon_size == 48

    def test_numeric_settings_accept_hand_edited_strings(self) -> None:
        """settings.json is hand-editable, and Gtk.Adjustment rejects strings outright."""
        settings = Settings()
        settings.update(
            {
                "base_width": "900",
                "max_recent_apps": "8",
                "recent_apps_grid_columns": "4",
                "recent_apps_grid_icon_size": "64",
                "window_shadow": "3",
            }
        )
        assert settings.base_width == 900
        assert settings.max_recent_apps == 8
        assert settings.recent_apps_grid_columns == 4
        assert settings.recent_apps_grid_icon_size == 64
        assert settings.window_shadow == 3

    def test_unusable_numeric_value_falls_back_to_the_default(self) -> None:
        settings = Settings()
        settings.update({"recent_apps_grid_columns": "lots", "recent_apps_grid_icon_size": None})
        assert settings.recent_apps_grid_columns == 4
        assert settings.recent_apps_grid_icon_size == 48

    def test_dash_to_underscore(self) -> None:
        s = Settings()
        assert s.theme_name == "light"
        s.update({"theme-name": "asdf"})
        assert not hasattr(s, "theme-name")
        assert hasattr(s, "theme_name")
        assert s.theme_name == "asdf"
