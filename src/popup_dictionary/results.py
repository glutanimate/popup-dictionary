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

"""
Parses collection for pertinent notes and generates result list
"""

import re
from typing import TYPE_CHECKING, List, Optional, Sequence, Union

from aqt import mw
from aqt.utils import askUser

from .config import config
from .libaddon.debug import logger

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.notes import Note, NoteId

PYCMD_IDENTIFIER: str = "popupDictionary"

# UI messages

WRN_RESCOUNT: str = (
    "<b>{}</b> relevant notes found.<br>"
    "The tooltip could take a lot of time to render and <br>"
    "temporarily slow down Anki.<br><br>"
    "<b>Are you sure you want to proceed?</b>"
)

# HTML format strings for results

html_reslist: str = """<div class="pdict-reslist">{}</div>"""

html_res_normal: str = f"""\
<div class="pdict-res" data-nid={{}}>{{}}<div title="Browse..." class="pdict-brws"
onclick='pycmd("{PYCMD_IDENTIFIER}Browse:" + this.parentNode.dataset.nid)'>&rarr;</div></div>\
"""

html_res_dict: str = f"""\
<div class="pdict-res pdict-dict" data-nid={{}}>
    <div class="pdict-dict-title">Definition:</div>
    {{}}
    <div title="Browse..." class="pdict-brws" onclick='pycmd("{PYCMD_IDENTIFIER}Browse:" + this.parentNode.dataset.nid)'>&rarr;</div>
</div>"""

html_field: str = """<div class="pdict-fld">{}</div>"""

# RegExes for cloze marker removal

cloze_re_str = r"\{\{c(\d+)::(.*?)(::(.*?))?\}\}"
cloze_re = re.compile(cloze_re_str)

# RegExes for sound file marker removal
sound_re_str = "\[.*?\.mp3\]"

# Anki API shims


def get_note(collection: "Collection", note_id: "NoteId") -> "Note":
    try:
        return collection.get_note(note_id)
    except AttributeError:
        return collection.getNote(note_id)


def find_notes(collection: "Collection", query: str, **kwargs) -> Sequence["NoteId"]:
    try:
        return collection.find_notes(query, **kwargs)
    except AttributeError:
        return collection.findNotes(query, **kwargs)  # type:ignore[attr-defined]


# Functions that compose tooltip content


def get_content_for(term: str, ignore_nid: str) -> str:
    """Compose tooltip content for search term.
    Returns HTML string."""
    conf = config["local"]

    dict_entry = None
    note_content = None
    content = []

    if conf["dictionaryEnabled"]:
        dict_entry = search_definition_for(term)
        if dict_entry:
            content.append(dict_entry)

    if conf["snippetsEnabled"]:
        note_content = get_note_snippets_for(term, ignore_nid)

        if note_content:
            content.extend(note_content)  # type: ignore

    if content:
        return html_reslist.format("".join(content))
    elif note_content is False:
        return ""
    elif note_content is None and conf["generalConfirmEmpty"]:
        return "No other results found."

    return ""


def get_note_snippets_for(term: str, ignore_nid: str) -> Union[List[str], bool, None]:
    """Find relevant note snippets for search term.
    Returns list of HTML strings."""

    conf = config["local"]

    logger.debug("getNoteSnippetsFor called")
    # exclude current note
    current_nid = mw.reviewer.card.note().id
    exclusion_tokens = ["-nid:{}".format(current_nid)]

    if ignore_nid:
        exclusion_tokens.append("-nid:{}".format(ignore_nid))

    if conf["snippetsLimitToCurrentDeck"]:
        exclusion_tokens.append("deck:current")

    if conf["snippetsExcludeNewNotes"]:
        exclusion_tokens.append("-is:new")

    # construct query string
    query = """"{}" {}""".format(term, " ".join(exclusion_tokens))

    # NOTE: performing the SQL query directly might be faster
    res = sorted(find_notes(collection=mw.col, query=query))
    logger.debug("getNoteSnippetsFor query finished.")

    if not res:
        return None

    # Prevent slowdowns when search term is too common
    res_len = len(res)
    warn_limit = conf["snippetsResultsWarnLimit"]
    if warn_limit > 0 and res_len > warn_limit:
        if not askUser(WRN_RESCOUNT.format(res_len), title="Popup Dictionary"):
            return False

    note_content: List[str] = []
    excluded_flds = conf["snippetsExcludedFields"]

    for nid in res:
        note = get_note(collection=mw.col, note_id=nid)
        valid_flds = [
            html_field.format(i[1]) for i in note.items() if i[0] not in excluded_flds
        ]
        joined_flds = "".join(valid_flds)
        # remove cloze markers
        filtered_flds = cloze_re.sub(r"\2", joined_flds)
        # remove sound file markers
        filtered_flds = re.sub(sound_re_str, ' ', filtered_flds)
        note_content.append(html_res_normal.format(nid, filtered_flds))

    return note_content


def search_definition_for(term: str) -> Optional[str]:
    """Look up search term in dictionary deck.
    Returns HTML string."""
    conf = config["local"]
    query = """note:"{}" {}:"{}" """.format(
        conf["dictionaryNoteTypeName"], conf["dictionaryTermFieldName"], term
    )
    res = find_notes(collection=mw.col, query=query)
    if res:
        nid = res[0]
        note = get_note(collection=mw.col, note_id=nid)
        try:
            result = note[conf["dictionaryDefinitionFieldName"]]
        except KeyError:
            return None
        return html_res_dict.format(nid, result)

    return None
