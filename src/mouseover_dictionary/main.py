# -*- coding: utf-8 -*-

"""
This file is part of the Mouseover Dictionary add-on for Anki.

Main Module, hooks add-on methods into Anki.

Copyright: (c) 2018 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

from aqt.qt import *
from aqt import mw
from aqt.reviewer import Reviewer
from anki.hooks import wrap, addHook

from .js import html
from .consts import *
from .config import (DECK, NOTETYPE, TERM_FIELD,
                     DEFINITION_FIELD, USER_STYLES)
from .template import addModel


class DictionaryLookup(QObject):
    """
    A single instance of the class is created and stored in the module's dictLookup
    variable. This instance is then added as a javascript object to the reviewer's
    main frame. We then get callbacks from qtip's set functions requesting
    the html to display
    """

    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot(str, result=str)
    def definitionFor(self, term):
        return self.generateDefinition(term)

    def generateDefinition(self, term):
        return searchDefinitionFor(term.strip())


dictLookup = DictionaryLookup()


def searchDefinitionFor(term):
    query = u"""note:"{}" {}:"{}" """.format(NOTETYPE, TERM_FIELD, term)
    res = mw.col.findNotes(query)
    if res:
        nid = res[0]
        note = mw.col.getNote(nid)
        return note[DEFINITION_FIELD]
    return "No dictionary entry found."


def addJavascriptObjects(self):
    # add the callback object
    self.web.page().mainFrame().addToJavaScriptWindowObject("pyDictLookup", dictLookup)


def setupAddon():
    """Prepare note type and deck"""
    did = mw.col.decks.byName(DECK)
    if not did:
        mw.col.decks.id(DECK)
    mid = mw.col.models.byName(NOTETYPE)
    if not mid:
        addModel(mw.col)
    if not did or not mid:
        mw.reset()


# Hooks

addHook("profileLoaded", setupAddon)
Reviewer._initWeb = wrap(Reviewer._initWeb, addJavascriptObjects, "after")
Reviewer._revHtml += "<style>{}</style>".format(USER_STYLES) + html
