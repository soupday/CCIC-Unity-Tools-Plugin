# Copyright (C) 2025 Victor Soupday
# This file is part of CC/iC-Unity-Pipeline-Plugin <https://github.com/soupday/CCiC-Unity-Pipeline-Plugin>
#
# CC/iC-Unity-Pipeline-Plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CC/iC-Unity-Pipeline-Plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CC/iC-Unity-Pipeline-Plugin.  If not, see <https://www.gnu.org/licenses/>.


from utp import prefs, qt, importer, exporter, link


rl_plugin_info = { "ap": "iClone", "ap_version": "8.0" }

FBX_IMPORTER: importer.Importer = None
BLOCK_UPDATE = False


def initialize_plugin():
    global BLOCK_UPDATE

    BLOCK_UPDATE = True

    print("CC/iC Unity Pipeline Plugin: Initialize")

    prefs.detect_paths()

    icon_export = qt.get_icon("BlenderExport.png")
    icon_link = qt.get_icon("BlenderDataLink.png")
    icon_settings = qt.get_icon("BlenderSettings.png")
    icon_unity = qt.get_icon("UnityLogo.png")

    # Menu (CC4 & iClone)
    plugin_menu = qt.find_add_plugin_menu("Unity Pipeline")
    qt.clear_menu(plugin_menu)
    qt.add_menu_action(plugin_menu, "Export Character to Unity", action=menu_export, icon=icon_export)
    qt.menu_separator(plugin_menu)
    qt.add_menu_action(plugin_menu, "DataLink", action=menu_link, icon=icon_link)
    qt.menu_separator(plugin_menu)
    qt.add_menu_action(plugin_menu, "Settings", action=menu_settings, icon=icon_settings)
    qt.add_menu_action(plugin_menu, "Toolbar", action=menu_toolbar, toggle=True, on=True)

    toolbar = qt.find_add_toolbar("Unity Pipeline Toolbar", show_hide=fetch_toolbar_state)
    qt.clear_toolbar(toolbar)
    qt.add_toolbar_label(toolbar, "UnityLogoIcon.png", None)
    qt.add_toolbar_action(toolbar, icon_link, "Unity DataLink", action=menu_link, toggle=True)
    qt.add_toolbar_separator(toolbar)
    qt.add_toolbar_action(toolbar, icon_export, "Export to Unity", action=menu_export)
    qt.add_toolbar_separator(toolbar)
    qt.add_toolbar_action(toolbar, icon_settings, "Unity Pipeline Settings", action=menu_settings, toggle=True)

    if prefs.AUTO_START_SERVICE:
        link.link_auto_start()

    BLOCK_UPDATE = False


def fetch_toolbar_state(visible):
    """Update the menu Toolbar toggle with the visibilty state of the toolbar.
       CC4 / iC8 remembers the visibility state of toolbars and applies it after the
       plug-in has been initialized. This will update the menu with those changes."""
    global BLOCK_UPDATE
    if BLOCK_UPDATE: return
    plugin_menu = qt.find_plugin_menu("Unity Pipeline")
    if plugin_menu:
        menu_toolbar_action = qt.find_menu_action(plugin_menu, "Toolbar")
        if menu_toolbar_action:
            BLOCK_UPDATE = True
            menu_toolbar_action.setChecked(visible)
            BLOCK_UPDATE = False


def menu_toolbar():
    global BLOCK_UPDATE
    if BLOCK_UPDATE: return
    plugin_menu = qt.find_plugin_menu("Unity Pipeline")
    toolbar = qt.find_toolbar("Unity Pipeline Toolbar")
    if plugin_menu and toolbar:
        menu_toolbar_action = qt.find_menu_action(plugin_menu, "Toolbar")
        if menu_toolbar_action:
            BLOCK_UPDATE = True
            if menu_toolbar_action.isChecked():
                toolbar.show()
            else:
                toolbar.hide()
            BLOCK_UPDATE = False


def menu_export():
    export = exporter.get_exporter()
    if export.is_shown():
        export.hide()
    else:
        export.show()


def menu_link():
    data_link = link.get_data_link()
    if data_link.is_shown():
        data_link.hide()
    else:
        data_link.show()


def menu_settings():
    preferences = prefs.get_preferences()
    if preferences.is_shown():
        preferences.hide()
    else:
        preferences.show()


def show_settings():
    preferences = prefs.get_preferences()
    if not preferences.is_shown():
        preferences.show()


def run_script():
    initialize_plugin()


