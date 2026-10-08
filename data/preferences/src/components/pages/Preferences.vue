<template>
  <div v-if="prefsLoaded">
    <h1>General</h1>

    <table>
      <tr>
        <td>
          <label for="hotkey-show-app">Hotkey</label>
        </td>
        <td>
          <b-form-input
            id="hotkey-show-app"
            @focus.native="showHotkeyDialog($event)"
            :value="prefs.hotkey_show_app"
          ></b-form-input>
        </td>
      </tr>

      <tr v-if="prefs.is_wayland">
        <td colspan="2" class="hotkey-warning">
          <b-alert show variant="warning">
            <small>
              Global hotkeys is supported on X11 only, and you are using Wayland.<br/>
              You can still set them in your desktop environment's keyboard settings, bound to the command: <code>ulauncher-toggle</code>.<br/>
              See
              <a
                href
                @click.prevent="openUrlInBrowser('https://github.com/Ulauncher/Ulauncher/discussions/1347')"
              >troubleshooting</a>
              for more details
            </small>
          </b-alert>
        </td>
      </tr>

      <tr>
        <td>
          <label for="theme-name">Color Theme</label>
        </td>
        <td>
          <b-form-select
            id="theme-name"
            class="theme-select"
            :options="prefs.available_themes"
            v-model="theme_name"
          ></b-form-select>
        </td>
      </tr>

      <tr>
        <td>
          <label for="autostart">Launch at Login</label>
        </td>
        <td>
          <b-form-checkbox
            :disabled="!prefs.autostart_allowed"
            id="autostart"
            v-model="autostart_enabled"
          ></b-form-checkbox>
        </td>
      </tr>

      <tr>
        <td>
          <label for="show-recent-apps">Number of frequent apps to show</label>
        </td>
        <td>
          <b-form-input style="width:250px" id="show-recent-apps" v-model="show_recent_apps"></b-form-input>
        </td>
      </tr>

      <tr>
        <td>
          <label for="recent-apps-layout">Frequent apps layout</label>
        </td>
        <td>
          <b-form-select
            id="recent-apps-layout"
            style="width:250px"
            :options="recentAppsLayoutOptions"
            v-model="recent_apps_layout"
          ></b-form-select>
        </td>
      </tr>

      <tr v-if="recent_apps_layout === 'grid'">
        <td>
          <label for="recent-apps-grid-columns">Icons per row</label>
        </td>
        <td>
          <b-form-input
            type="number"
            :min="gridColumnsRange.min"
            :max="gridColumnsRange.max"
            style="width:250px"
            id="recent-apps-grid-columns"
            :value="gridColumnsDraft"
            @input="gridColumnsDraft = $event"
            @change="commitGridColumns"
            @blur="commitGridColumns"
          ></b-form-input>
        </td>
      </tr>

      <tr v-if="recent_apps_layout === 'grid'">
        <td>
          <label for="recent-apps-grid-labels">Grid labels</label>
        </td>
        <td>
          <b-form-select
            id="recent-apps-grid-labels"
            style="width:250px"
            :options="recentAppsGridLabelsOptions"
            v-model="recent_apps_grid_labels"
          ></b-form-select>
        </td>
      </tr>

      <tr v-if="recent_apps_layout === 'grid'">
        <td>
          <label for="recent-apps-grid-icon-size">Grid icon size (px)</label>
        </td>
        <td>
          <b-form-input
            type="number"
            :min="gridIconSizeRange.min"
            :max="gridIconSizeRange.max"
            style="width:250px"
            id="recent-apps-grid-icon-size"
            :value="gridIconSizeDraft"
            @input="gridIconSizeDraft = $event"
            @change="commitGridIconSize"
            @blur="commitGridIconSize"
          ></b-form-input>
        </td>
      </tr>

      <tr>
        <td>
          <label for="clear_previous_query">Clear Input on Hide</label>
        </td>
        <td>
          <b-form-checkbox id="clear_previous_query" v-model="clear_previous_query"></b-form-checkbox>
        </td>
      </tr>

      <tr>
        <td>
          <label for="render-on-screen">Render On</label>
        </td>
        <td>
          <b-form-select
            id="render-on-screen"
            class="render-on-screen-select"
            :options="renderOnScreenOptions"
            v-model="render_on_screen"
          ></b-form-select>
        </td>
      </tr>

      <tr>
        <td>
          <label for="grab_mouse_pointer">Don't hide after losing mouse focus</label>
        </td>
        <td>
          <b-form-checkbox id="grab_mouse_pointer" v-model="grab_mouse_pointer"></b-form-checkbox>
        </td>
      </tr>
    </table>

    <h1>Advanced</h1>

    <table>
      <tr>
        <td>
          <label for="show-indicator-icon">Show Indicator Icon</label>
          <small>
            <p>It's supported only if gir1.2-ayatanaappindicator3-0.1 or an equivalent is installed</p>
          </small>
        </td>
        <td>
          <b-form-checkbox id="show-indicator-icon" v-model="show_indicator_icon"></b-form-checkbox>
        </td>
      </tr>

      <tr>
        <td>
          <label for="terminal-exec">Terminal Command</label>
          <small>
            <p>
              Overrides terminal for apps that are configured to be run from a terminal.
              Set to an empty value for default terminal
            </p>
          </small>
        </td>
        <td>
          <b-form-input style="width:250px" id="terminal-exec" v-model="terminal_command"></b-form-input>
        </td>
      </tr>
      <tr>
        <td class="pull-top">
          <label>Blacklisted App Dirs</label>
          <small>
            <p>Ulauncher won't search for .desktop files in these dirs</p>
            <p v-if="blacklistedDirsChanged">
              <i class="fa fa-warning"></i> Restart Ulauncher for this to take effect
            </p>
          </small>
        </td>
        <td class="pull-top">
          <editable-text-list
            width="450px"
            v-model="blacklisted_desktop_dirs"
            newItemPlaceholder="Type in an absolute path and press Enter"
          ></editable-text-list>
        </td>
      </tr>
      <tr>
        <td class="pull-top">
          <label for="disable-desktop-filters">Show All Apps</label>
          <small>
            <p>
              Display all applications, even if they are configured to not show in the current desktop environment.
            </p>
            <p v-if="disableDesktopFiltersChanged">
              <i class="fa fa-warning"></i> Restart Ulauncher for this to take effect
            </p>
          </small>
        </td>
        <td class="pull-top">
          <b-form-checkbox id="disable-desktop-filters" v-model="disable_desktop_filters"></b-form-checkbox>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import { mapState, mapMutations, mapGetters } from 'vuex'

import jsonp from '@/api'
import bus from '@/event-bus'
import EditableTextList from '@/components/widgets/EditableTextList'

const hotkeyEventName = 'hotkey-show-app'

// Must mirror the limits in ulauncher/utils/recent_apps.py, which the preferences API
// clamps to. Clamping here as well keeps the inputs from displaying a value that was
// never saved, but only on commit -- see the drafts in data().
const GRID_COLUMNS = { min: 1, max: 12, default: 4 }
const GRID_ICON_SIZE = { min: 16, max: 128, default: 48 }

function clampSetting(value, { min, max, default: fallback }) {
  const parsed = parseInt(value, 10)
  if (isNaN(parsed)) {
    return String(fallback)
  }
  return String(Math.min(max, Math.max(min, parsed)))
}

function draftFromPref(value, { default: fallback }) {
  return value === undefined || value === null || value === '' ? String(fallback) : String(value)
}

export default {
  name: 'preferences',

  components: {
    'editable-text-list': EditableTextList
  },

  created() {
    bus.$on(hotkeyEventName, this.onHotkeySet)
  },

  beforeDestroy() {
    bus.$off(hotkeyEventName, this.onHotkeySet)
  },

  data() {
    return {
      previous_theme_name: null,
      blacklistedDirsChanged: false,
      renderOnScreenOptions: {
        'mouse-pointer-monitor': 'Monitor with a mouse pointer',
        'default-monitor': 'Default monitor'
      },
      recentAppsLayoutOptions: {
        list: 'List (one app per row)',
        grid: 'Grid of icons'
      },
      recentAppsGridLabelsOptions: {
        none: 'Icons only',
        name: 'Icon + name',
        shortcut: 'Icon + shortcut',
        'name-and-shortcut': 'Icon + name + shortcut'
      },
      gridColumnsRange: GRID_COLUMNS,
      gridIconSizeRange: GRID_ICON_SIZE,
      // Drafts for the numeric grid inputs. They hold whatever is typed, unclamped, and
      // are only normalized and saved on commit (change/blur), so that a half-typed
      // "6" on the way to "64" isn't rewritten to the minimum under the cursor.
      gridColumnsDraft: String(GRID_COLUMNS.default),
      gridIconSizeDraft: String(GRID_ICON_SIZE.default)
    }
  },

  watch: {
    'prefs.recent_apps_grid_columns': {
      immediate: true,
      handler(value) {
        this.gridColumnsDraft = draftFromPref(value, GRID_COLUMNS)
      }
    },

    'prefs.recent_apps_grid_icon_size': {
      immediate: true,
      handler(value) {
        this.gridIconSizeDraft = draftFromPref(value, GRID_ICON_SIZE)
      }
    }
  },

  computed: {
    ...mapState(['prefs']),

    ...mapGetters(['prefsLoaded']),

    autostart_enabled: {
      get() {
        return this.prefs.autostart_enabled
      },
      set(value) {
        this.setPrefs({ autostart_enabled: value })
        jsonp('prefs://set/autostart-enabled', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    show_indicator_icon: {
      get() {
        return this.prefs.show_indicator_icon
      },
      set(value) {
        this.setPrefs({ show_indicator_icon: value })
        jsonp('prefs://set/show-indicator-icon', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    show_recent_apps: {
      get() {
        if (this.prefs.show_recent_apps === true) {
          return '3'
        } else if (this.prefs.show_recent_apps === false) {
          return '0'
        }
        return this.prefs.show_recent_apps
      },
      set(value) {
        this.setPrefs({ show_recent_apps: value })
        jsonp('prefs://set/show-recent-apps', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    recent_apps_layout: {
      get() {
        return this.prefs.recent_apps_layout || 'list'
      },
      set(value) {
        this.setPrefs({ recent_apps_layout: value })
        jsonp('prefs://set/recent-apps-layout', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    recent_apps_grid_labels: {
      get() {
        return this.prefs.recent_apps_grid_labels || 'name-and-shortcut'
      },
      set(value) {
        this.setPrefs({ recent_apps_grid_labels: value })
        jsonp('prefs://set/recent-apps-grid-labels', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    terminal_command: {
      get() {
        return this.prefs.terminal_command
      },
      set(value) {
        this.setPrefs({ terminal_command: value })
        jsonp('prefs://set/terminal-command', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    theme_name: {
      get() {
        return this.prefs.theme_name
      },
      set(value) {
        this.setPrefs({ theme_name: value })
        jsonp('prefs://set/theme-name', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    clear_previous_query: {
      get() {
        return this.prefs.clear_previous_query
      },
      set(value) {
        this.setPrefs({ clear_previous_query: value })
        jsonp('prefs://set/clear-previous-query', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    grab_mouse_pointer: {
      get() {
        return this.prefs.grab_mouse_pointer
      },
      set(value) {
        this.setPrefs({ grab_mouse_pointer: value })
        jsonp('prefs://set/grab-mouse-pointer', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    blacklisted_desktop_dirs: {
      get() {
        return this.prefs.blacklisted_desktop_dirs
      },
      set(value) {
        this.setPrefs({ blacklisted_desktop_dirs: value })
        this.blacklistedDirsChanged = true
        jsonp('prefs://set/blacklisted-desktop-dirs', { value: value.join(':') }).catch(err => bus.$emit('error', err))
      }
    },

    disable_desktop_filters: {
      get() {
        return this.prefs.disable_desktop_filters
      },
      set(value) {
        this.setPrefs({ disable_desktop_filters: value })
        this.disableDesktopFiltersChanged = true
        jsonp('prefs://set/disable-desktop-filters', { value: value }).catch(err => bus.$emit('error', err))
      }
    },

    render_on_screen: {
      get() {
        return this.prefs.render_on_screen
      },
      set(value) {
        this.setPrefs({ render_on_screen: value })
        jsonp('prefs://set/render-on-screen', { value: value }).catch(err => bus.$emit('error', err))
      }
    }
  },

  methods: {
    ...mapMutations(['setPrefs']),

    commitGridColumns() {
      this.gridColumnsDraft = this.commitGridSetting(
        this.gridColumnsDraft,
        GRID_COLUMNS,
        'recent_apps_grid_columns',
        'prefs://set/recent-apps-grid-columns'
      )
    },

    commitGridIconSize() {
      this.gridIconSizeDraft = this.commitGridSetting(
        this.gridIconSizeDraft,
        GRID_ICON_SIZE,
        'recent_apps_grid_icon_size',
        'prefs://set/recent-apps-grid-icon-size'
      )
    },

    commitGridSetting(draft, range, prefName, url) {
      const normalized = clampSetting(draft, range)
      if (normalized !== draftFromPref(this.prefs[prefName], range)) {
        this.setPrefs({ [prefName]: normalized })
        jsonp(url, { value: normalized }).catch(err => bus.$emit('error', err))
      }
      return normalized
    },

    openUrlInBrowser(url) {
      jsonp('prefs://open/web-url', { url: url })
    },

    showHotkeyDialog(e) {
      jsonp('prefs://show/hotkey-dialog', { name: hotkeyEventName })
      e.target.blur()
    },

    onHotkeySet(e) {
      jsonp('prefs://set/hotkey-show-app', { value: e.value }).then(
        () => this.setPrefs({ hotkey_show_app: e.displayValue }),
        err => bus.$emit('error', err)
      )
    }
  }
}
</script>

<style lang="css" scoped>
/* use tables to support WebKit on Ubuntu 14.04 */
table {
  width: 100%;
  margin: 25px 15px 15px 40px;
}
.pull-top {
  vertical-align: top;
}
h1 {
  margin: 30px 0 0 25px;
  font-size: 110%;
  color: #aaa;
  text-shadow: 1px 1px 1px #fff;
}
td:first-child {
  box-sizing: border-box;
  width: 220px;
  padding-right: 20px;
}
td {
  padding-bottom: 20px;
}
tr:last-child td {
  padding-bottom: 0;
}
label {
  cursor: pointer;
}
label + small {
    position: relative;
    top: -5px;
    line-height: 1.3em;
    display: block;
    color: #888;
}
#hotkey-show-app {
  cursor: pointer;
  width: 200px;
}
/* overrides the width and padding that td:first-child gives this full-width cell */
td.hotkey-warning {
  width: auto;
  padding-right: 0;
}
.hotkey-warning .alert {
  max-width: 550px;
  margin: 0;
  padding: 0.4em 0.7em;
  line-height: 1.4;
}
.theme-select,
.render-on-screen-select {
  width: auto;
}
</style>
