# -*- coding: utf-8 -*-

# Popup Dictionary Add-on for Anki
#
# Copyright (C)  2018-2019 Aristotelis P. <https://glutanimate.com/>
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

"""
Modifications to Anki's Reviewer
"""

import json
from typing import TYPE_CHECKING, Any, Optional, Tuple, Union

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from aqt import mw
from aqt.reviewer import Reviewer

from .browser import browse_to_nid
from .config import config
from .results import PYCMD_IDENTIFIER, getContentFor
from .web import popup_integrator

if TYPE_CHECKING:  # 2.1.22+
    from aqt.webview import WebContent


def onReviewerHotkey():
    if mw.state != "review":
        return
    mw.reviewer.web.eval("invokeTooltipAtSelectedElm();")


# Legacy


def link_handler(self: Reviewer, url: str, _old) -> Optional[str]:
    """JS <-> Py bridge"""

    if not url.startswith(PYCMD_IDENTIFIER):
        return _old(self, url)

    return webview_message_handler(url)


def on_rev_html(self, _old) -> str:
    return _old(self) + popup_integrator


# New


def webview_message_handler(message: str) -> Optional[str]:
    cmd, arg = message.split(":", 1)
    subcmd = cmd.replace(PYCMD_IDENTIFIER, "")

    if subcmd == "Browse":
        (cmd, arg) = message.split(":", 1)
        if not arg:
            return None
        browse_to_nid(arg)
    elif subcmd == "Lookup":
        (cmd, payload) = message.split(":", 1)
        term, ignore_nid = json.loads(payload)
        term = term.strip()
        return getContentFor(term, ignore_nid)
    else:
        print(f"Unrecognized pop-up dictionary pycmd identifier {subcmd}")

    return None


def on_webview_will_set_content(
    web_content: "WebContent", context: Union[Reviewer, Any]
):
    if not isinstance(context, Reviewer):
        return

    # Appending to body rather than using header. Not best practice, but let's stay
    # on the safe side
    web_content.body += popup_integrator


def on_webview_did_receive_js_message(
    handled: Tuple[bool, Any], message: str, context: Union[Reviewer, Any]
):
    if not isinstance(context, Reviewer):
        return handled

    if not message.startswith(PYCMD_IDENTIFIER):
        return handled

    callback_value = webview_message_handler(message)

    return (True, callback_value)


# ensure that we only patch once on first profile load
_reviewer_patched: bool = False


def patch_reviewer():
    global _reviewer_patched

    if _reviewer_patched:
        return

    try:  # 2.1.22+
        from aqt.gui_hooks import (
            webview_will_set_content,
            webview_did_receive_js_message,
        )

        webview_will_set_content.append(on_webview_will_set_content)
        webview_did_receive_js_message.append(on_webview_did_receive_js_message)

    except (ImportError, ModuleNotFoundError):
        from anki.hooks import wrap

        Reviewer.revHtml = wrap(Reviewer.revHtml, on_rev_html, "around")
        Reviewer._linkHandler = wrap(Reviewer._linkHandler, link_handler, "around")

    _reviewer_patched = True


def setup_shortcuts():
    QShortcut(  # type: ignore
        QKeySequence(config["local"]["generalHotkey"]), mw, activated=onReviewerHotkey
    )


def initialize_reviewer():
    """Delay patching reviewer to counteract bad practices in other add-ons that
    overwrite revHtml and _linkHandler in their entirety"""

    try:  # 2.1.20+
        from aqt.gui_hooks import profile_did_open

        profile_did_open.append(patch_reviewer)
    except (ImportError, ModuleNotFoundError):
        from anki.hooks import addHook

        addHook("profileLoaded", patch_reviewer)

    setup_shortcuts()
