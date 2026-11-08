# GEMS GIS Handbook

How GEMS Taiwan learned QGIS in summer 2026 (ten classes with Dr. Daniel Bloom,
2 July to 6 August) and turned it into the ReLEAF
[Geospatial Analysis](https://2026.igem.wiki/gems-taiwan/geospatial-analysis) page.
For future students and teachers who want to pick up GIS where this team left off.

## Open it

Open `index.html` in a browser. No server, no build and no internet needed;
the pages switch between 繁體中文 and English with the button in the top bar.

| Page | What it holds |
|---|---|
| `index.html` | Learning route, why GIS, season plan, people |
| `course.html` | Every class: what was taught, links, homework, outputs |
| `skills.html` | Sixteen QGIS techniques with steps and traps |
| `data.html` | Every data source, the team's files and QGIS projects, team documents |
| `maps.html` | All maps the class posted, by assignment |
| `project.html` | Storyline, change of direction, wiki figures and where they came from |
| `archive.html` | The full Discord record and Google Doc snapshots |

## Folders

```
archive/discord/html/    each channel as a readable page
archive/discord/json/    each channel as JSON (DiscordChatExporter format)
archive/discord/media/   every attachment, avatar and emoji
archive/docs/            text snapshots of three team Google Docs
assets/thumbs/           thumbnails of maps and photos
assets/wiki/             figures copied from the live Geospatial Analysis page
src/                     page bodies, hand-written, bilingual
tools/build.py           wraps src/ in the shared nav and footer, builds the gallery and file tables
```

## Editing

Edit `src/<page>.html`, then run `python3 tools/build.py`. Every visible string
exists twice, as `<span lang="en">` and `<span lang="zh">`. Map gallery entries
live in the `GALLERY` list in `tools/build.py`.

## Source

Discord server "GIS + Data Phys" (1521456968080822402), pulled 8 November 2026
with DiscordChatExporter 2.47 and threads included. The four forums
#data-physicalization, #field-trip, #maps and #storylines had no posts.
