# Experimentopedia

An unofficial fan reference to Jumba Jookiba's 629 illegal genetic experiments from Disney's Lilo & Stitch franchise: the films, Lilo & Stitch: The Series, Leroy & Stitch, the Stitch! anime and Stitch & Ai.

This project is not affiliated with, endorsed by, or connected to Disney. Lilo & Stitch and all characters belong to Disney.

## How it is laid out

Plain Markdown with headings and lists, made to read well with VoiceOver and other screen readers. There are no images and no tables.

- [INDEX.md](INDEX.md) lists every experiment by number, by series and by function.
- [ALPHABETICAL.md](ALPHABETICAL.md) lists the named experiments A to Z.
- The `experiments` folder has one page per experiment, from 000 to 629.
- The `series` folder groups them by Jumba's numbering series.
- The `categories` folder groups them by what they do, including [Transmuted experiments (Stitch! anime)](categories/transmuted.md): experiments Hämsterviel transmuted or Delia altered (the "2.0" episodes), and Stitch's anime-only Powercell powers.
- The `special` folder covers creations outside Jumba's numbering: Dark End (made by Delia), Skunkuna (made by Hämsterviel) and the Leroy clones.

Every page says how much is known about the experiment:
- rich: it has its own article on the Disney Wiki or the Lilo & Stitch Wiki.
- partial: there's a short official description, or episode guides list it in specific episodes (with plot summaries).
- function only (unverified): the only information is a one-line function from a Russian fan list (disney-classic.ru), machine-translated and clearly marked as unverified.
- sparse: nothing beyond a name or number. Nothing is made up to fill gaps.

The transmuted category separates experiments with a confirmed transmuted or altered form from ones that only appear in Hämsterviel or Delia plots.

## How it is built

Like Drugopedia, the pages are generated. `tools/rows.json` and `tools/pages.json` hold the source data, and `python3 tools/render.py` writes all the Markdown.

## Sources and license

Text is condensed and adapted from the Disney Wiki (disney.fandom.com) and the Lilo & Stitch Wiki (liloandstitch.fandom.com), with unverified function notes machine-translated from disney-classic.ru. The main sources are the wikis' "Experiments" lists, character articles and episode guides. Wiki content is licensed CC BY-SA 3.0, so this repository is shared under the same CC BY-SA 3.0 license, with attribution to the contributors of both wikis.
