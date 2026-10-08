import pytest
import mock
from ulauncher.ui.ItemNavigation import ItemNavigation


class TestItemNavigation:

    @pytest.fixture
    def items(self):
        return [mock.MagicMock() for _ in range(5)]

    @pytest.fixture
    def nav(self, items):
        return ItemNavigation(items)

    def test_select_is_called(self, nav, items):
        nav.select(1)
        assert nav.selected == 1
        items[1].select.assert_called_once_with()

    def test_select_and_deselect_is_called(self, nav, items):
        nav.select(1)
        nav.select(5)
        items[1].deselect.assert_called_once_with()
        items[0].select.assert_called_once_with()
        assert nav.selected == 0, "First element is not selected"

    def test_go_up_from_start(self, nav, items):
        nav.go_up()
        items[4].select.assert_called_once_with()

    def test_go_up_from_1st(self, nav, items):
        nav.select(1)
        nav.go_up()
        items[0].select.assert_called_once_with()

    def test_go_up_from_last(self, nav, items):
        nav.select(4)
        nav.go_up()
        items[3].select.assert_called_once_with()

    def test_go_down_from_2nd(self, nav, items):
        nav.select(2)
        nav.go_down()
        items[3].select.assert_called_once_with()

    def test_go_down_from_last(self, nav, items):
        nav.select(4)
        nav.go_down()
        items[0].select.assert_called_once_with()

    def test_enter_by_index(self, nav, items):
        nav.enter('test', 3)
        items[3].on_enter.assert_called_with('test')

    def test_enter_no_index(self, nav, items):
        nav.select(2)
        assert nav.enter('test') is items[2].on_enter.return_value.keep_app_open.return_value
        items[2].on_enter.return_value.run.assert_called_with()

    def test_enter__alternative(self, nav, items):
        nav.select(2)
        assert nav.enter('test', alt=True) is items[2].on_alt_enter.return_value.keep_app_open.return_value
        items[2].on_alt_enter.return_value.run.assert_called_with()

    def test_select_default(self, nav, items, mocker):
        select = mocker.patch.object(nav, 'select')
        for item in items:
            item.selected_by_default.return_value = False
        items[3].selected_by_default.return_value = True
        nav.select_default('q')
        select.assert_called_with(3)

        # no default
        items[3].selected_by_default.return_value = False
        nav.select_default('q')
        select.assert_called_with(0)

    def test_columns_default_to_one(self, nav):
        assert nav.columns == 1


class TestItemNavigationGrid:
    """
    6 items in 4 columns, i.e.
        0 1 2 3
        4 5
    """

    @pytest.fixture
    def items(self):
        return [mock.MagicMock() for _ in range(6)]

    @pytest.fixture
    def nav(self, items):
        nav = ItemNavigation(items, columns=4)
        nav.select(0)
        return nav

    def test_invalid_column_count_falls_back_to_one(self, items):
        assert ItemNavigation(items, columns=0).columns == 1

    def test_go_right(self, nav):
        nav.go_right()
        assert nav.get_selected_index() == 1

    def test_go_right_wraps_to_first(self, nav):
        nav.select(5)
        nav.go_right()
        assert nav.get_selected_index() == 0

    def test_go_left_wraps_to_last(self, nav):
        nav.go_left()
        assert nav.get_selected_index() == 5

    def test_go_down_jumps_a_row(self, nav):
        nav.select(1)
        nav.go_down()
        assert nav.get_selected_index() == 5

    def test_go_down_wraps_within_the_column(self, nav):
        nav.select(5)
        nav.go_down()
        assert nav.get_selected_index() == 1

    def test_go_down_stays_put_when_column_has_one_row(self, nav):
        nav.select(3)
        nav.go_down()
        assert nav.get_selected_index() == 3

    def test_go_up_jumps_a_row(self, nav):
        nav.select(4)
        nav.go_up()
        assert nav.get_selected_index() == 0

    def test_go_up_wraps_to_the_bottom_of_the_column(self, nav):
        nav.select(1)
        nav.go_up()
        assert nav.get_selected_index() == 5

    def test_go_up_wraps_to_the_last_row_that_has_the_column(self, nav):
        nav.select(3)
        nav.go_up()
        assert nav.get_selected_index() == 3

    def test_navigation_is_safe_without_items(self):
        nav = ItemNavigation([], columns=4)
        nav.go_up()
        nav.go_down()
        nav.go_left()
        nav.go_right()
        assert nav.get_selected_index() is None
