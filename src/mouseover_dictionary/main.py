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
from .config import (ENABLE_DICTIONARY_DECK, NOTETYPE, TERM_FIELD,
                     DEFINITION_FIELD, USER_STYLES,
                     EXCLUDED_FIELDS, ALWAYS_SHOW, WARN_LIMIT,
                     HOTKEY, LIMIT_TO_CURRENT_DECK)
from .template import addModel

# support for JS Booster add-on
try:
    from jsbooster import review_hack
    JSBOOSTER = True
except ImportError:
    JSBOOSTER = False


# UI messages

WRN_RESCOUNT = ("<b>{}</b> relevant notes found.<br>"
                "The tooltip could take a lot of time to render and <br>"
                "temporarily slow down Anki.<br><br>"
                "<b>Are you sure you want to proceed?</b>")


# HTML format strings for results

pycmd = "pycmd" if anki21 else "py.link"

html_reslist = """<div class="tt-reslist">{}</div>"""

html_res_normal = """\
<div class="tt-res" data-nid={{}}>{{}}<div title="Browse..." class="tt-brws"
onclick='{}("dctBrws:" + this.parentNode.dataset.nid)'>&rarr;</div></div>\
""".format(pycmd)

html_res_dict = """\
<div class="tt-res tt-dict" data-nid={{}}>
    <div class="tt-dict-title">Definition:</div>
    {{}}
    <div title="Browse..." class="tt-brws" onclick='{}("dctBrws:" + this.parentNode.dataset.nid)'>&rarr;</div>
</div>""".format(pycmd)

html_field = """<div class="tt-fld">{}</div>"""

# RegExes for cloze marker removal

cloze_re_str = r"\{\{c(\d+)::(.*?)(::(.*?))?\}\}"
cloze_re = re.compile(cloze_re_str)


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
        term = term.strip()
        return getContentFor(term, ignore_nid)


# DictionaryLookup instance that gets added as a JS object
dictLookup = DictionaryLookup()


def addJavascriptObjects(self):
    """Add python object to JS"""
    self.web.page().mainFrame().addToJavaScriptWindowObject("pyDictLookup", dictLookup)


def getContentFor(term, ignore_nid):
    """Compose tooltip content for search term.
    Returns HTML string."""

    content = []

    if ENABLE_DICTIONARY_DECK:
        dict_entry = searchDefinitionFor(term)
        if dict_entry:
            content.append(dict_entry)

    note_content = getNoteSnippetsFor(term, ignore_nid)

    if note_content:
        content.extend(note_content)

    if content:
        return html_reslist.format("".join(content))
    elif note_content is False:
        return ""
    elif note_content is None:
        return "No other results found." if ALWAYS_SHOW else ""


def getNoteSnippetsFor(term, ignore_nid):
    """Find relevant note snippets for search term.
    Returns list of HTML strings."""

    print("getNoteSnippetsFor")
    # exclude current note
    current_nid = mw.reviewer.card.note().id
    exclusion_tokens = ["-nid:{}".format(current_nid)]

    if ignore_nid:
        exclusion_tokens.append("-nid:{}".format(ignore_nid))

    if LIMIT_TO_CURRENT_DECK:
        exclusion_tokens.append("deck:current")

    # construct query string
    query = u'''"{}" {}'''.format(term, " ".join(exclusion_tokens))

    # NOTE: performing the SQL query directly might be faster
    res = sorted(mw.col.findNotes(query))
    print("Query finished.")

    if not res:
        return None

    # Prevent slowdowns when search term is too common
    res_len = len(res)
    if WARN_LIMIT > 0 and res_len > WARN_LIMIT:
        if not askUser(WRN_RESCOUNT.format(res_len), title="Mouseover Dictionary"):
            return False

    note_content = []
    for nid in res:
        note = mw.col.getNote(nid)
        valid_flds = [html_field.format(
            i[1]) for i in note.items() if i[0] not in EXCLUDED_FIELDS]
        joined_flds = "".join(valid_flds)
        # remove cloze markers
        filtered_flds = cloze_re.sub(r"\2", joined_flds)
        note_content.append(html_res_normal.format(nid, filtered_flds))

    return note_content


def searchDefinitionFor(term):
    """Look up search term in dictionary deck.
    Returns HTML string."""
    query = u"""note:"{}" {}:"{}" """.format(NOTETYPE, TERM_FIELD, term)
    res = mw.col.findNotes(query)
    if res:
        nid = res[0]
        note = mw.col.getNote(nid)
        try:
            result = note[DEFINITION_FIELD]
        except KeyError:
            return None
        return html_res_dict.format(nid, result)

    return None


def onReviewerHotkey():
    if mw.state != "review":
        return
    mw.reviewer.web.eval("invokeTooltipAtSelectedElm();")


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
    # JS Booster support:
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

    if ENABLE_DICTIONARY_DECK:
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
