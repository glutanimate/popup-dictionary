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

# Enable custom dictionary deck with prioritized results
ENABLE_DICTIONARY_DECK = True
# Show tooltip even if no results found?
ALWAYS_SHOW = True
# Warn above n results. Set to 0 to disable
WARN_LIMIT = 1000
# Hotkey to manually invoke search on selected text
HOTKEY = "Ctrl+Shift+D"

# DICTIONARY MODE

NOTETYPE = "Dictionary Entry"
TERM_FIELD = "Term"
DEFINITION_FIELD = "Definition"

# SNIPPET MODE
EXCLUDED_FIELDS = ["Extra", "Note ID", "Quellen", "Bidirektional"]
LIMIT_TO_CURRENT_DECK = True



##############  USER CONFIGURATION END  ##############

# TODO: Rework into .json based config
