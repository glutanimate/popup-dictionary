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
Note type and card templates.
"""

from typing import TYPE_CHECKING, NamedTuple, Optional, Tuple

from aqt import mw
from aqt.main import AnkiQt

from .config import config

if TYPE_CHECKING:
    from anki.models import FieldDict, ModelManager, NotetypeDict, TemplateDict


class CardTemplate(NamedTuple):
    name: str
    qfmt: str
    afmt: str


class NoteType(NamedTuple):
    name: str
    fields: Tuple[str, ...]
    templates: Tuple[CardTemplate, ...]
    css: str


_dictionary_card_template: CardTemplate = CardTemplate(
    name="Definition",
    qfmt="""\
<b>Define</b>: {{%s}}
"""
    % config["local"]["dictionaryTermFieldName"],
    afmt="""\
{{FrontSide}}

<hr id=answer>

{{%s}}
"""
    % config["local"]["dictionaryDefinitionFieldName"],
)

_dictionary_note_type = NoteType(
    name=config["local"]["dictionaryNoteTypeName"],
    fields=(
        config["local"]["dictionaryTermFieldName"],
        config["local"]["dictionaryDefinitionFieldName"],
    ),
    templates=(_dictionary_card_template,),
    css="""\
.card {
    font-family: arial;
    font-size: 20px;
    text-align: center;
    color: black;
    background-color: white;
}
""",
)

# Anki API shims


def models_new_field(model_manager: "ModelManager", name: str) -> "FieldDict":
    try:
        return model_manager.new_field(name)
    except AttributeError:
        return model_manager.newField(name)  # type:ignore[attr-defined]


def models_new_template(model_manager: "ModelManager", name: str) -> "TemplateDict":
    try:
        return model_manager.new_template(name)
    except AttributeError:
        return model_manager.newTemplate(name)  # type:ignore[attr-defined]


def models_by_name(
    model_manager: "ModelManager", name: str
) -> Optional["NotetypeDict"]:
    try:
        return model_manager.by_name(name)
    except AttributeError:
        return model_manager.byName(name)  # type:ignore[attr-defined]


# Note type creation


def maybe_add_note_type(mw: AnkiQt, note_type: NoteType) -> bool:
    if mw.col is None:
        print("Collection not ready")
        return False

    model_manager = mw.col.models

    if models_by_name(model_manager=model_manager, name=note_type.name):
        # note type already exists (by name)
        return False

    anki_model = model_manager.new(note_type.name)

    # Add fields:
    for field_name in note_type.fields:
        field = models_new_field(model_manager=model_manager, name=field_name)
        model_manager.addField(anki_model, field)

    # Add card templates:
    for card_template in note_type.templates:
        template = models_new_template(
            model_manager=model_manager, name=card_template.name
        )
        template["qfmt"] = card_template.qfmt
        template["afmt"] = card_template.afmt
        model_manager.addTemplate(anki_model, template)

    anki_model["css"] = note_type.css

    model_manager.add(anki_model)

    return True


def maybe_create_template():
    if mw is None:
        return

    if not config["local"]["dictionaryEnabled"]:
        return

    if maybe_add_note_type(mw, _dictionary_note_type):
        mw.reset()


def initialize_template():
    from aqt.gui_hooks import profile_did_open

    profile_did_open.append(maybe_create_template)
