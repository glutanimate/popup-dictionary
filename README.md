## Popup Dictionary Add-on for Anki <!-- omit in toc -->

This is an add-on for the spaced-repetition flashcard app [Anki](https://apps.ankiweb.net/). It provides the ability to quickly draw up related facts on words or phrases, just by double-clicking on them.

### Table of Contents <!-- omit in toc -->

<!-- MarkdownTOC -->

- [Screenshots](#screenshots)
- [Installation](#installation)
- [Documentation](#documentation)
- [License and Credits](#license-and-credits)

<!-- /MarkdownTOC -->

### Screenshots

![](screenshots/screencast.gif)

### Installation

**AnkiWeb**

Pop-up dictionary is still in beta, so it's not available on AnkiWeb, yet.

**Manual installation**

*Anki 2.0*

1. Go to *Tools* -> *Add-ons* -> *Open add-ons folder*
2. Find and delete `Popup Dictionary.py` and `popup_dictionary` if they already exist
3. Download and extract the latest Anki 2.0 add-on release from the [releases tab](https://github.com/Glutanimate/popup-dictionary/releases)
4. Move `Popup Dictionary.py` and `popup_dictionary` into the add-ons folder
5. Restart Anki

*Anki 2.1*

1. Go to *Tools* -> *Add-ons* -> *Open add-ons folder*
2. See if the `popup_dictionary` folder already exists
3. If you would like to keep your settings thus far: Find the `meta.json` file contained within and copy it to a safe location.
4. Proceed to delete  the `popup_dictionary` folder
3. Download and extract the latest Anki 2.1 add-on release from the [releases tab](https://github.com/Glutanimate/popup-dictionary/releases)
4. Rename the extracted folder (e.g. `v0.4.1`) to `popup_dictionary` and move it into the add-ons directory
5. Optional: Place the `meta.json` file back in the directory if you created a copy beforehand.
5. Restart Anki

### Documentation

For further information on the use of this add-on please check out [the original add-on description](docs/description.md).

### License and Credits

*Popup Dictionary* is *Copyright © 2018 [Aristotelis P.](https://glutanimate.com/)*

Development of this add-on was made possible, in part, through the kind support of two fellow Anki users. I would like to thank both of them for their help.

Ships with the following javascript libraries:

- jQuery (v1.12.4), (c) jQuery Foundation, licensed under the MIT license
- qTip2 (v2.1.1), (c) 2011-2018 Craig Michael Thompson, licensed under the MIT license
- jQuery.highlight, (c) 2007-2014 Johann Burkard, licensed under the MIT license

Licensed under the [GNU AGPLv3](https://www.gnu.org/licenses/agpl.html).