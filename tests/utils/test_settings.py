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

    def test_dash_to_underscore(self) -> None:
        s = Settings()
        assert s.theme_name == "light"
        s.update({"theme-name": "asdf"})
        assert not hasattr(s, "theme-name")
        assert hasattr(s, "theme_name")
        assert s.theme_name == "asdf"
