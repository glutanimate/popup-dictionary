<p align="center"><img src="screenshots/screencast.gif" width=610></p>

<h2 align="center">Pop-up Dictionary for Anki</h2>

<p align="center">
<a title="Latest (pre-)release" href="https://github.com/glutanimate/popup-dictionary/releases"><img src ="https://img.shields.io/github/release-pre/glutanimate/popup-dictionary.svg?colorB=brightgreen"></a>
<a title="License: GNU AGPLv3" href="https://github.com/glutanimate/popup-dictionary/blob/master/LICENSE"><img  src="https://img.shields.io/badge/license-GNU AGPLv3-green.svg"></a>
<a title="Rate on AnkiWeb" href="https://ankiweb.net/shared/info/153625306"><img src="https://glutanimate.com/logos/ankiweb-rate.svg"></a>
<br>
<a title="Buy me a coffee :)" href="https://ko-fi.com/X8X0L4YV"><img src="https://img.shields.io/badge/ko--fi-contribute-%23579ebd.svg"></a>
<a title="Support me on Patreon :D" href="https://www.patreon.com/bePatron?u=7522179"><img src="https://img.shields.io/badge/patreon-support-%23f96854.svg"></a>
<a title="Follow me on Twitter" href="https://twitter.com/intent/user?screen_name=glutanimate"><img src="https://img.shields.io/twitter/follow/glutanimate.svg"></a>
</p>

> Connecting the flashcard-dots

This is an add-on for the spaced-repetition flashcard app [Anki](https://apps.ankiweb.net/). It provides the ability to quickly draw up related facts on words or phrases, just by double-clicking on them.

### Table of Contents <!-- omit in toc -->

<!-- MarkdownTOC levels="1,2,3" -->

- [Installation](#installation)
- [Documentation](#documentation)
- [Building](#building)
- [Contributing](#contributing)
- [License and Credits](#license-and-credits)

<!-- /MarkdownTOC -->

### Installation

#### AnkiWeb <!-- omit in toc -->

The easiest way to install Pop-up Dictionary is through [AnkiWeb](https://ankiweb.net/shared/info/153625306).

#### Manual installation <!-- omit in toc -->


<details>

<summary>Click here to see the instructions</summary>

1. Make sure you have the [latest version](https://apps.ankiweb.net/#download) of Anki 2.1 installed.
2. Download the latest `.ankiaddon` package from the [releases tab](https://github.com/glutanimate/popup-dictionary/releases) (you might need to click on *Assets* below the description to reveal the download links)
3. From Anki's main window, head to *Tools* → *Add-ons*
4. Drag-and-drop the `.ankiaddon` package onto the add-ons list
5. Restart Anki

</details>

### Documentation

For further information on the use of this add-on please check out [the description text](docs/description.md) for AnkiWeb.

### Building

With [Anki add-on builder](https://github.com/glutanimate/anki-addon-builder/) installed:

    git clone https://github.com/glutanimate/popup-dictionary.git
    cd popup-dictionary
    aab build

For more information on the build process please refer to [`aab`'s documentation](https://github.com/glutanimate/anki-addon-builder/#usage).

### Contributing

Contributions are welcome! Please review the [contribution guidelines](./CONTRIBUTING.md) on how to:

- Report issues
- File pull requests
- Support the project as a non-developer

### License and Credits

*Pop-up Dictionary* is *Copyright © 2018-2021 [Aristotelis P.](https://glutanimate.com/) (Glutanimate)*

My work on the initial version of this add-on was partially funded by two fellow Anki users. I would like to thank both of them for their help.

Ships with the following javascript libraries:

- jQuery (v1.12.4), (c) jQuery Foundation, licensed under the MIT license
- qTip2 (v3.0.3), (c) 2011-2018 Craig Michael Thompson, licensed under the MIT license
- jQuery.highlight, (c) 2007-2014 Johann Burkard, licensed under the MIT license
- jQuery Migrate, (c) OpenJS Foundation and other contributors, https://openjsf.org/, licensed under the MIT license

Pop-up Dictionary is free and open-source software. The add-on code that runs within Anki is released under the GNU AGPLv3 license, extended by a number of additional terms. For more information please see the [LICENSE](https://github.com/glutanimate/popup-dictionary/blob/master/LICENSE) file that accompanied this program.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.

----

<b>
<div align="center">The continued development of this add-on is made possible <br>thanks to my <a href="https://www.patreon.com/glutanimate">Patreon</a> and <a href="https://ko-fi.com/X8X0L4YV">Ko-Fi</a> supporters.
<br>You guys rock ❤️ !</div>
</b>