# -*- coding: utf-8 -*-

"""
This file is part of the Mouseover Dictionary add-on for Anki.

Main Module, hooks add-on methods into Anki.

Copyright: (c) 2018 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

import re

import aqt
from aqt.qt import *
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import askUser
from anki.hooks import wrap, addHook

from .js import html
from .consts import *
from .config import (MODE, DECK, NOTETYPE, TERM_FIELD,
                     DEFINITION_FIELD, USER_STYLES,
                     EXCLUDED_FIELDS, ALWAYS_SHOW, WARN_LIMIT,
                     HOTKEY)
from .template import addModel

# support for JS Booster add-on
try:
    from jsbooster import review_hack
    JSBOOSTER = True
except ImportError:
    JSBOOSTER = False

pycmd = "pycmd" if anki21 else "py.link"


WRN_RESCOUNT = ("<b>{}</b> relevant notes found.<br>"
                "The tooltip could take a lot of time to render and <br>"
                "temporarily slow down Anki.<br><br>"
                "<b>Are you sure you want to proceed?</b>")


class DictionaryLookup(QObject):
    """
    A single instance of the class is created and stored in the module's dictLookup
    variable. This instance is then added as a javascript object to the reviewer's
    main frame. We then get callbacks from qtip's set functions requesting
    the html to display

    Based on deck hover tooltip by Steve AW
    """

    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot(str, str, result=str)
    def definitionFor(self, term, ignore_nid):
        return getNoteSnippetsFor(term.strip(), ignore_nid)


dictLookup = DictionaryLookup()


html_reslist = """<div class="tt-reslist">{}</div>"""
html_res = ("""<div class="tt-res" data-nid={{}}>{{}}<div title="Browse..." class="tt-brws" """
            """onclick='{}("dctBrws:" + this.parentNode.dataset.nid)'>"""
            """&rarr;</div></div>""".format(pycmd))
html_field = """<div class="tt-fld">{}</div>"""

cloze_re_str = r"\{\{c(\d+)::(.*?)(::(.*?))?\}\}"
cloze_re = re.compile(cloze_re_str)


def getNoteSnippetsFor(term, ignore_nid):
    """Find relevant note snippets for search term"""

    print("getNoteSnippetsFor")
    # exclude current note
    current_nid = mw.reviewer.card.note().id
    exclusion_string = "-nid:{} ".format(current_nid)

    if ignore_nid:
        exclusion_string += " -nid:{}".format(ignore_nid)

    # construct query string
    query = u'''deck:current "{}" {}'''.format(term, exclusion_string)

    # NOTE: performing the SQL query directly might be faster
    res = sorted(mw.col.findNotes(query))

    if not res:
        return "No other results found." if ALWAYS_SHOW else ""
    print("Query finished.")

    # Prevent slowdowns when search term is too common
    res_len = len(res)
    if WARN_LIMIT > 0 and res_len > WARN_LIMIT:
        if not askUser(WRN_RESCOUNT.format(res_len), title="Mouseover Dictionary"):
            return ""

    content = []
    for nid in res:
        note = mw.col.getNote(nid)
        valid_flds = [html_field.format(
            i[1]) for i in note.items() if i[0] not in EXCLUDED_FIELDS]
        joined_flds = "".join(valid_flds)
        # remove cloze markers
        filtered_flds = cloze_re.sub(r"\2", joined_flds)
        content.append(html_res.format(nid, filtered_flds))

    html = html_reslist.format("".join(content))
    print("Html compiled")

    return html


def searchDefinitionFor(term):
    """Look up search term in dictionary deck"""
    query = u"""note:"{}" {}:"{}" """.format(NOTETYPE, TERM_FIELD, term)
    res = mw.col.findNotes(query)
    if res:
        nid = res[0]
        note = mw.col.getNote(nid)
        return note[DEFINITION_FIELD]
    return "No dictionary entry found."


def onReviewerHotkey():
    if mw.state != "review":
        return
    mw.reviewer.web.eval("invokeTooltipAtSelectedElm();")


def addJavascriptObjects(self):
    """Add python object to JS"""
    self.web.page().mainFrame().addToJavaScriptWindowObject("pyDictLookup", dictLookup)


def linkHandler(self, url, _old):
    """Extend link handler with browser links"""
    if not url.startswith("dctBrws"):
        return _old(self, url)
    (cmd, arg) = url.split(":", 1)
    if not arg:
        return
    browseToNid(arg)


def browseToNid(nid):
    """Open browser and find cards by nid"""
    browser = aqt.dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText("nid:'{}'".format(nid))
    browser.onSearch()


def setupAddon():
    """Setup hooks, prepare note type and deck"""
    # JSBooster support:
    if not JSBOOSTER:
        Reviewer._initWeb = wrap(
            Reviewer._initWeb, addJavascriptObjects, "after")
        Reviewer._revHtml += html + "<style>{}</style>".format(USER_STYLES)
    else:
        review_hack.review_html_scripts += html + \
            "<style>{}</style>".format(USER_STYLES)
        Reviewer._showQuestion = wrap(
            Reviewer._showQuestion, addJavascriptObjects)
        Reviewer._showAnswer = wrap(Reviewer._showAnswer, addJavascriptObjects)

    if MODE == "dictionary":
        did = mw.col.decks.byName(DECK)
        if not did:
            mw.col.decks.id(DECK)
        mid = mw.col.models.byName(NOTETYPE)
        if not mid:
            addModel(mw.col)
        if not did or not mid:
            mw.reset()


# Menus and hotkeys
QShortcut(QKeySequence(HOTKEY), mw, activated=onReviewerHotkey)

# Hooks
Reviewer._linkHandler = wrap(Reviewer._linkHandler, linkHandler, "around")
addHook("profileLoaded", setupAddon)
