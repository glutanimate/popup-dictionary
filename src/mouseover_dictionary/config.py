# -*- coding: utf-8 -*-

"""
This file is part of the Mouseover Dictionary add-on for Anki.

Configuration module

Copyright: (c) 2018 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

# GENERAL

# Mode selection
MODE = "snippets"  # dictionary/snippets
# Show tooltip even if no results found?
ALWAYS_SHOW = False

# DICTIONARY MODE
DECK = "Dictionary"
NOTETYPE = "Dictionary Entry"
TERM_FIELD = "Term"
DEFINITION_FIELD = "Definition"

# SNIPPET MODE
EXCLUDED_FIELDS = ["Extra", "Quellen", "Bidirektional"]
LIMIT_TO_CURRENT_DECK = True

# TOOLTIP STYLING
USER_STYLES = r"""
.qtip {
    max-width: 440px;
    max-height: 440px;
    font-family: "arial", sans-serif;
    color: #141414;
    background-color: white;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.4);
}
.night_mode > .qtip{
    background-color: #141414;
    border-color: #515151;
    border-width: 1px;
    color: white;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.4);
}
.qtip-bootstrap .qtip-content {
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 5px;
    padding-bottom: 5px;
}
.qtip-content {
    margin-top: 5px;
    margin-left: 0;
    margin-right: 0;
    margin-bottom: 5px;
    max-width: 400px;
    max-height: 400px;
    overflow-y: auto;
}
.tt-res {
    position:relative;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    padding-top: 0.5em;
    padding-bottom: 0.5em;
    padding-left: 0.5em;
    padding-right: 0.5em;
    border-style: solid;
    border-width: 0.1em;
    border-color: #7E7680;
    border-radius: 0.1em;
}
.tt-fld {
    margin-top: 0.5em;
}
.tt-reslist {
    text-align: center;
}
.tt-brws {
    position: absolute;
    bottom: 0;
    right: 0;
    line-height 5px;
    vertical-align: bottom;
    color: #A0A0A0;
    cursor: pointer;
}
.highlight {
    background-color: yellow;
}
.night_mode > .qtip .highlight {
    color: black
}
"""

##############  USER CONFIGURATION END  ##############

# TODO: Rework into .json based config

