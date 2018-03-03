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
EXCLUDED_FIELDS = ["Extra"]
LIMIT_TO_CURRENT_DECK = True

# TOOLTIP STYLING
USER_STYLES = r"""
.qtip {
    font-family: "arial", sans-serif;
    max-width: 400px;
    max-height: 400px;
    overflow-y: auto;
    color: #141414;
    background-color: white;  
}
.night_mode > .qtip{
    background-color: #141414;
    color: white;  
}
.qtip-bootstrap .qtip-content {
    padding-left: 0.5em;
    padding-right: 0.5em;
    padding-top: 0.2em;
    padding-bottom: 0.2em;
}

.tt-res {
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
"""

##############  USER CONFIGURATION END  ##############
