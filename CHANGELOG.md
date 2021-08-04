# Changelog

All notable changes to Pop-up Dictionary will be documented here. You can click on each release number to be directed to a detailed log of all code commits for that particular release. The download links will direct you to the GitHub release page, allowing you to manually install a release if you want.

If you enjoy Pop-up Dictionary, please consider supporting my work on Patreon, or by buying me a cup of coffee :coffee::

<p align="center">
<a href="https://www.patreon.com/glutanimate" rel="nofollow" title="Support me on Patreon 😄"><img src="https://glutanimate.com/logos/patreon_button.svg"></a>      <a href="https://ko-fi.com/X8X0L4YV" rel="nofollow" title="Buy me a coffee 😊"><img src="https://glutanimate.com/logos/kofi_button.svg"></a>
</p>

:heart: My heartfelt thanks goes out to everyone who has supported this add-on through their tips, contributions, or any other means (you know who you are!). All of this would not have been possible without you. Thank you for being awesome!

## [Unreleased]

## [1.0.0-beta.1] - 2021-08-04

### [Download](https://github.com/glutanimate/popup-dictionary/releases/tag/v1.0.0-beta.1)

### Added

- Added suport for modern Anki versions (tested up to Anki 2.1.46)
- The add-on now sports a sleek new pop-up design and effects, optimized both for light mode and dark mode
- Searches can now also be triggered by selecting a phrase and right-clicking
- Added an option to exclude new notes from snippet results (thanks to @zjosua!)

### Fixed

- Changed the default add-on hotkey to "Alt+Shift+D" (⌥+⇧+D on macOS) to avoid a conflict with default key bindings on Anki 2.1.41 and up
- Fixed an issue that would cause an error when opening cards in the browser (thanks to @Nanco300 for the report!)
- Fixed an issue that would cause images within the pop-ups to not be sized correctly (thanks to @padenw24 for the report!)
- Made the add-on more resilient against conflicts with user-made deck styling
- Made the add-on more resilient against conflicts with other add-ons (tested against the top 200 most popular add-ons)

### Changed

- Refactored major parts of the add-on, making it more robust and future-proof
- Dropped support for older Anki versions. The minimum supported version is now 2.1.23.
- Upgraded qTip2 to v3.0.3. This should hopefully fix a number of bugs with the pop-ups and make for an overall smoother user experience (thanks to @ansaso!)

## [1.0.0-dev.1] - 2019-08-27

### [Download](https://github.com/glutanimate/popup-dictionary/releases/tag/v1.0.0-dev.1)

### Changed

- Dropped 2.0.x support
- Refactored major parts of the add-on

## [0.5.0-beta.1] - 2019-02-28

### Changed

- Added footer to tooltip
- Updated packaging scheme to simplify installation process
    
## [0.4.2] - 2018-08-19

### Fixed

- Quick fix for Anki 2.1 support.
    
## [0.4.1] - 2018-03-18

### Changed

- Changed: Renamed add-on to Pop-up Dictionary
- Changed: New default values for excluded fields

### Fixed
    
- Fixed: Anki 2.1 support

## [0.4.0] - 2018-03-06

### Added

- **New**: Anki 2.1 support (please wait for the next 2.1 beta)
- **New**: merged original dictionary lookup functionality with new note snippets
- **New**: highlight search terms
- **New**: show note in browser
- **New**: hotkey to invoke tooltip manually on custom selection (Ctrl+Shift+D)
- **New**: warn when looking up term with too many hits
- **New**: invoke tooltip on double-click rather than select
- **New**: config file with full support of Anki 2.1's config editor

### Fixed

- **Fixed**: a lot of smaller issues and bugs
    
## [0.3.0] - 2018-03-05

### Added

- nested tooltips
- refined theme
    
## [0.2.0] - 2018-03-03

### Added

- Switch to displaying snippets of notes in the current deck, instead of using the dictionary deck

## v0.1.0 - 2018-02-19

### Added

Initial release

[Unreleased]: https://github.com/glutanimate/popup-dictionary/compare/v1.0.0-dev.1...HEAD
[1.0.0-dev.1]: https://github.com/glutanimate/popup-dictionary/compare/v0.5.0-beta.1...v1.0.0-dev.1
[0.5.0-beta.1]: https://github.com/glutanimate/popup-dictionary/compare/v0.4.2...v0.5.0-beta.1
[0.4.2]: https://github.com/glutanimate/popup-dictionary/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/glutanimate/popup-dictionary/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/glutanimate/popup-dictionary/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/glutanimate/popup-dictionary/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/glutanimate/popup-dictionary/compare/v0.1.0...v0.2.0

-----

The format of this file is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).