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

import aqt
from aqt.qt import *
from aqt import mw
from aqt.reviewer import Reviewer

from anki.hooks import wrap, addHook

from .results import getContentFor
from .web import popup_integrator
from .config import config


def linkHandler(self, url, _old):
    """JS <-> Py bridge"""
    if url.startswith("dctBrws"):
        (cmd, arg) = url.split(":", 1)
        if not arg:
            return
        browseToNid(arg)
    elif url.startswith("dctLookup"):
        (cmd, payload) = url.split(":", 1)
        term, ignore_nid = json.loads(payload)
        term = term.strip()
        return getContentFor(term, ignore_nid)
    elif url.startswith("dctDebug"):
        (cmd, msg) = url.split(":", 1)
        
    else:
        return _old(self, url)


def browseToNid(nid):
    """Open browser and find cards by nid"""
    browser = aqt.dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText("nid:'{}'".format(nid))
    browser.onSearchActivated()


def onRevHtml(self, _old):
    return _old(self) + popup_integrator


def onProfileLoaded():
    """Monkey-patch Reviewer delayed in order to counteract bad practices
    in other add-ons that overwrite revHtml and _linkHandler in their
    entirety"""
    Reviewer.revHtml = wrap(Reviewer.revHtml, onRevHtml, "around")
    Reviewer._linkHandler = wrap(Reviewer._linkHandler, linkHandler, "around")


def onReviewerHotkey():
    if mw.state != "review":
        return
    mw.reviewer.web.eval("invokeTooltipAtSelectedElm();")


def setupShortcuts():
    QShortcut(QKeySequence(config["local"]["generalHotkey"]),
              mw, activated=onReviewerHotkey)


def initializeReviewer():
    setupShortcuts()
    addHook("profileLoaded", onProfileLoaded)
