class ItemNavigation:
    """
    Performs navigation through found results

    With `columns` > 1 the items are treated as a grid filled left to right,
    row by row: up/down jump a whole row, left/right move by a single item.
    """

    def __init__(self, items, columns=1):
        """
        :param list items: list of ResultItemWidget()'s
        :param int columns: number of items per row (1 means a plain vertical list)
        """
        self.items = items
        self.items_num = len(items)
        self.columns = max(1, int(columns))
        self.selected = None

    def get_selected_index(self):
        return self.selected

    def select_default(self, query):
        """
        Selects item that should be selected by default
        If no such items found, select the first one in the list
        """
        indices = (index for index, item in enumerate(self.items) if item.selected_by_default(query))
        index = next(indices, 0)
        self.select(index)

    def select(self, index):
        if not 0 <= index < self.items_num:
            index = 0

        if self.selected is not None:
            self.items[self.selected].deselect()

        self.selected = index
        self.items[index].select()

    def go_up(self):
        if not self.items_num:
            return
        if self.columns == 1:
            index = self.selected - 1 if self.selected is not None and self.selected > 0 else self.items_num - 1
            self.select(index)
            return

        current = self.selected or 0
        index = current - self.columns
        if index < 0:
            # wrap around to the bottom-most item of the same column
            column = current % self.columns
            index = column + ((self.items_num - 1 - column) // self.columns) * self.columns
        self.select(index)

    def go_down(self):
        if not self.items_num:
            return
        if self.columns == 1:
            index = self.selected + 1 if self.selected is not None and self.selected < self.items_num - 1 else 0
            self.select(index)
            return

        current = self.selected or 0
        index = current + self.columns
        if index >= self.items_num:
            # wrap around to the top-most item of the same column
            index = current % self.columns
        self.select(index)

    def go_left(self):
        if not self.items_num:
            return
        current = self.selected or 0
        self.select(current - 1 if current > 0 else self.items_num - 1)

    def go_right(self):
        if not self.items_num:
            return
        current = self.selected or 0
        self.select(current + 1 if current < self.items_num - 1 else 0)

    def enter(self, query, index=None, alt=False):
        """
        Enter into selected item, unless 'index' is passed
        Return boolean - True if Ulauncher window should be closed
        """
        if index is not None:
            if not 0 <= index < self.items_num:
                raise IndexError

            self.select(index)
            return self.enter(query)

        if self.selected is not None:
            item = self.items[self.selected]
            action = item.on_enter(query) if not alt else item.on_alt_enter(query)
            if not action:
                return True
            action.run()
            return action.keep_app_open()

        return None
