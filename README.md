# Experimentopedia

An unofficial fan reference to Jumba Jookiba's 629 illegal genetic experiments from Disney's Lilo & Stitch franchise: the films, Lilo & Stitch: The Series, Leroy & Stitch, the Stitch! anime and Stitch & Ai.

This project is not affiliated with, endorsed by, or connected to Disney. Lilo & Stitch and all characters belong to Disney.

## How it is laid out

Plain Markdown with headings and lists, made to read well with VoiceOver and other screen readers. There are no images and no tables.

- [INDEX.md](INDEX.md) lists every experiment by number, by series and by function.
- [ALPHABETICAL.md](ALPHABETICAL.md) lists the named experiments A to Z.
- The `experiments` folder has one page per experiment, from 000 to 629.
- The `series` folder groups them by Jumba's numbering series.
- The `categories` folder groups them by what they do.

Every page says how much is known about the experiment:
- well-documented: the experiment has its own wiki article, so the page covers appearance, powers, weaknesses, personality, one true place, appearances and trivia.
- partial: there's a short official description only.
- sparse: little canonical info. Many experiments are only a name in the Leroy & Stitch finale or credits, or come from the Stitch! anime. Nothing is made up to fill those gaps.

## How it is built

Like Drugopedia, the pages are generated. `tools/rows.json` and `tools/pages.json` hold the source data, and `python3 tools/render.py` writes all the Markdown.

## Sources and license

Text is condensed and adapted from the Disney Wiki at disney.fandom.com, mainly its "Experiments" list and the individual character articles. That wiki content is licensed CC BY-SA 3.0, so this repository is shared under the same CC BY-SA 3.0 license, with attribution to the Disney Wiki contributors.
