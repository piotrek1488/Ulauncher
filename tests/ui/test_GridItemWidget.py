import pytest
import mock
from gi.repository import GdkPixbuf
from ulauncher.api.shared.item.ResultItem import ResultItem
from ulauncher.ui.GridItemWidget import GridItemWidget
from ulauncher.utils.recent_apps import (DEFAULT_ICON_SIZE, DEFAULT_LABEL_MODE,
                                         MIN_ICON_SIZE, MAX_ICON_SIZE)


class TestGridItemWidget:

    @pytest.fixture
    def item_obj(self):
        return mock.create_autospec(ResultItem)

    @pytest.fixture(autouse=True)
    def Theme(self, mocker):
        return mocker.patch('ulauncher.ui.ResultItemWidget.Theme')

    @pytest.fixture(autouse=True)
    def scale_factor(self, mocker):
        """
        set_icon() multiplies by the monitor scale factor and switches to set_from_surface
        above 1x, so pin it here instead of depending on the host's DPI.
        """
        return mocker.patch('ulauncher.ui.GridItemWidget.get_monitor_scale_factor', return_value=1)

    @pytest.fixture
    def builder(self):
        return mock.MagicMock()

    @pytest.fixture
    def pixbuf(self):
        return mock.Mock(spec=GdkPixbuf.Pixbuf)

    @pytest.fixture
    def widget(self, builder, item_obj):
        widget = GridItemWidget()
        widget.initialize(builder, item_obj, 0, 'query')
        return widget

    def test_defaults(self):
        widget = GridItemWidget()
        assert widget.icon_size == DEFAULT_ICON_SIZE
        assert widget.label_mode == DEFAULT_LABEL_MODE
        assert DEFAULT_LABEL_MODE == 'name-and-shortcut'

    def test_configure(self):
        widget = GridItemWidget()
        widget.configure(icon_size=64, label_mode='shortcut')
        assert widget.icon_size == 64
        assert widget.label_mode == 'shortcut'

    def test_configure_rejects_unknown_label_mode(self):
        widget = GridItemWidget()
        widget.configure(label_mode='nonsense')
        assert widget.label_mode == DEFAULT_LABEL_MODE

    def test_configure_clamps_the_icon_size(self):
        widget = GridItemWidget()
        widget.configure(icon_size=4)
        assert widget.icon_size == MIN_ICON_SIZE
        widget.configure(icon_size=4096)
        assert widget.icon_size == MAX_ICON_SIZE

    def test_set_icon_scales_the_request_on_hidpi(self, builder, item_obj, pixbuf, mocker):
        mocker.patch('ulauncher.ui.GridItemWidget.get_monitor_scale_factor', return_value=2)
        item_obj.get_icon_at_size = mock.Mock(return_value=pixbuf)
        widget = GridItemWidget()
        widget.configure(icon_size=48)
        widget.initialize(builder, item_obj, 0, 'query')
        item_obj.get_icon_at_size.assert_called_with(96)

    def test_set_icon_asks_the_item_for_the_configured_size(self, builder, item_obj, pixbuf):
        item_obj.get_icon_at_size = mock.Mock(return_value=pixbuf)
        widget = GridItemWidget()
        widget.configure(icon_size=64)
        widget.initialize(builder, item_obj, 0, 'query')
        item_obj.get_icon_at_size.assert_called_with(64)
        builder.get_object.return_value.set_from_pixbuf.assert_called_with(pixbuf)

    def test_set_icon_falls_back_to_the_default_pixbuf(self, builder, item_obj, pixbuf):
        item_obj.get_icon.return_value = pixbuf
        item_obj.get_icon_at_size = mock.Mock(return_value=None)
        widget = GridItemWidget()
        widget.initialize(builder, item_obj, 0, 'query')
        builder.get_object.return_value.set_from_pixbuf.assert_called_with(pixbuf)

    def test_set_icon_applies_a_size_request(self, builder, item_obj, pixbuf):
        item_obj.get_icon.return_value = pixbuf
        widget = GridItemWidget()
        widget.configure(icon_size=56)
        widget.initialize(builder, item_obj, 0, 'query')
        builder.get_object.return_value.set_size_request.assert_called_with(56, 56)

    def test_set_shortcut_tolerates_a_missing_label(self, widget, builder):
        builder.get_object.return_value = None
        widget.set_shortcut('Alt+1')  # must not raise

    @pytest.mark.parametrize('label_mode,name_hidden,shortcut_hidden', [
        ('none', True, True),
        ('name', False, True),
        ('shortcut', True, False),
        ('name-and-shortcut', False, False),
    ])
    def test_label_mode_toggles_the_labels(self, builder, item_obj, label_mode, name_hidden, shortcut_hidden):
        labels = {'item-name': mock.MagicMock(), 'item-shortcut': mock.MagicMock()}
        builder.get_object.side_effect = lambda name: labels.get(name, mock.MagicMock())

        widget = GridItemWidget()
        widget.configure(label_mode=label_mode)
        widget.initialize(builder, item_obj, 0, 'query')

        labels['item-name'].set_no_show_all.assert_called_with(name_hidden)
        labels['item-shortcut'].set_no_show_all.assert_called_with(shortcut_hidden)
        assert labels['item-name'].hide.called is name_hidden
        assert labels['item-shortcut'].hide.called is shortcut_hidden

    def test_shortcut_text_is_still_assigned(self, builder, item_obj, mocker):
        widget = GridItemWidget()
        set_shortcut = mocker.patch.object(widget, 'set_shortcut')
        widget.initialize(builder, item_obj, 4, 'query')
        set_shortcut.assert_called_once_with('Alt+5')
