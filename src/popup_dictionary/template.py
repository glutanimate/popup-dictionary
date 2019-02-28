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
Note type and card templates.
"""

from __future__ import unicode_literals

from .config import CONFIG


fields = (
    CONFIG["dictionaryTermFieldName"],
    CONFIG["dictionaryDefinitionFieldName"]
)

# Default card template
card_front = """
<b>Define</b>: {{%s}}
""" % CONFIG["dictionaryTermFieldName"]

card_back = """
{{FrontSide}}

<hr id=answer>

{{%s}}
""" % CONFIG["dictionaryDefinitionFieldName"]

css = """
.card {
font-family: arial;
font-size: 20px;
text-align: center;
color: black;
background-color: white;
}
"""


def addModel(col):
    models = col.models
    def_model = models.new(CONFIG["dictionaryNoteTypeName"])
    # Add fields:
    for fname in fields:
        fld = models.newField(fname)
        models.addField(def_model, fld)
    # Add template
    template = models.newTemplate("Definition")
    template['qfmt'] = card_front
    template['afmt'] = card_back
    def_model['css'] = css
    models.addTemplate(def_model, template)
    models.add(def_model)
    return def_model
