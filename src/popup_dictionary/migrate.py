# -*- coding: utf-8 -*-

# Pop-up Dictionary Add-on for Anki
#
# Copyright (C)  2018-2021 Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

import copy
from typing import Any, Dict, List

from .config import config
from .libaddon.anki.configmanager import ConfigManager
from .libaddon.platform import checkAnkiVersion

_KEY_GENERAL_HOTKEY = "generalHotkey"


def reset_config_defaults(
    config_dict: Dict[str, Any],
    default_config_dict: Dict[str, Any],
    keys_to_reset: List[str],
) -> Dict[str, Any]:
    for key in keys_to_reset:
        config_dict[key] = default_config_dict[key]
    return config_dict


def migrate_config(config_manager: ConfigManager):
    local_config = copy.deepcopy(config_manager["local"])
    default_config = config_manager.defaults["local"]
    keys_to_reset = []

    if (
        checkAnkiVersion("2.1.41")
        and local_config[_KEY_GENERAL_HOTKEY] == "Ctrl+Shift+D"
    ):
        # Anki 2.1.41 and up conflict with the old default key binding
        keys_to_reset.append(_KEY_GENERAL_HOTKEY)

    if not keys_to_reset:
        return

    config_manager["local"] = reset_config_defaults(
        config_dict=local_config,
        default_config_dict=default_config,
        keys_to_reset=keys_to_reset,
    )
    config_manager.save(storage_name="local")


def migrate_addon():
    migrate_config(config_manager=config)
