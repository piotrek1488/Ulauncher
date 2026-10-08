# Screenshots for the v6 "icon grid layout for frequent apps" pull request

Rendered from `ResultsView` inside the same widget tree `UlauncherWindow` builds
(`theme_root(.app)` -> prompt + results), at the default `base_width` of 750px,
with the built-in `light` and `dark` themes and 48px icons.

| file | layout |
| --- | --- |
| `list.png` | current list layout (unchanged default), 8 apps, 556px tall |
| `grid-name-and-shortcut.png` | grid default labels, 8 apps, 356px tall |
| `grid-name.png` | labels = `name` |
| `grid-shortcut.png` | labels = `shortcut` |
| `grid-icons-only.png` | labels = `none` |
| `grid-partial-last-row.png` | 6 apps in 4 columns: padded so columns keep equal width |
| `grid-5-columns.png` | 10 apps, `recent_apps_grid_columns = 5` |
