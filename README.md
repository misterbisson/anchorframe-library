# anchorframe-library

An open index of **film photography equipment** — camera bodies, lenses, film
stocks and lens mounts — one JSON file per thing, editable by pull request.

It is published at <https://anchorframe.app/library> and it is the source of the
name suggestions in [Anchorframe](https://github.com/misterbisson/anchorframe),
a macOS app for scanned film. Neither of those is a reason to be shy about
contributing: the data is CC BY-SA 4.0 and useful to anything that needs to know
what a camera is called.

| | records | brands |
| --- | --- | --- |
| cameras | 573 | 23 |
| lenses | 1,206 | 33 |
| films | 980 | 57 |
| mounts | 28 | — |

## The one idea the whole thing turns on

**A brand is who sold a thing, not who built it.**

Minolta manufactured the Leica CL. Zeiss ground the glass for Hasselblad's
V-system lenses, and Fuji built the H-system ones. Every Vivitar lens was made
by somebody else. `manufacturer` is a fact about a supply chain: often
unrecorded, sometimes contested, and *not* what is written on the front of the
thing you are holding.

This index is reached by typing what is written on the front. So a Hasselblad
lens is filed under Hasselblad —

```
/library/lens/hasselblad/zeiss-planar-t-80mm-f2-8-c
```

— with the maker still in the lens's own name, where a person reads it, and an
alternate under `zeiss` that redirects to it. Who made a camera and whose name
is on it are different questions, and this answers the second.

## URLs

```
/library/camera/canon/ae-1
/library/film/kodak/portra-400
/library/lens/nikon/nikkor-45mm-f2-8e-ed
/library/mount/canon-fd            ← no brand: M42 is a thread, not a product
```

The path is the address, and it comes straight from the file's own path in
`data/`. Two consequences worth knowing before you file a pull request:

- **The filename is the slug, and it is frozen.** Correcting a `name` does not
  move a URL. Deliberately moving one means adding the old address to
  `alternates`, which is also how renames are handled — every name a thing has
  ever had keeps working, and the ones that are not canonical redirect.
- **No dots in a slug.** The site is served from a private S3 bucket behind
  CloudFront, whose router decides "file or directory" by looking for a dot in
  the last path segment. `f/2.8` therefore becomes `f2-8`, not `f2.8`, and a
  slug with a dot would 404 rather than render.

## A record

Every thing is a Hugo **leaf bundle** — a directory holding `index.md`, plus any
images that belong to it.

```
content/camera/canon/ae-1/
  index.md
  ae-1-front.jpg        ← when someone contributes one
```

```toml
+++
title = "Canon AE-1"
brand = "Canon"
source = "https://en.wikipedia.org/wiki/Canon_AE-1"
mount = ["canon-fd"]
+++

Prose about the camera goes here, and it is optional.
```

**It is a directory even when it holds one file, and that is the point.** An
empty directory beside a record invites someone to drop a photograph into it; a
bare `<slug>.md` does not. Promoting a flat file to a bundle later would be as
disruptive as the move from JSON was, so everything is a bundle from the start.
The validator refuses a bare file.

Front matter is **TOML**, not YAML, for two reasons: `tomllib` is in Python's
standard library from 3.11, so the validator needs nothing installed and a fork's
pull request gets the same green tick as anyone else's; and YAML would silently
retype a corpus this full of terse model codes — `NO`, `ON`, `Y` and anything
version-shaped.

`title`, `brand` and `source` are required. A film says whether it is
`discontinued`; a fixed-lens body names its `fixed_lens` instead of a `mount`,
and never both. See [CONTRIBUTING.md](CONTRIBUTING.md) for the whole shape.

## How a record earns a page

Most records are a name, a brand and a link, and a page of that is a page that
exists in order not to be a 404. So an item's URL **redirects to its row in the
brand list** until the record has something to show — prose in the body, or an
image in the bundle. Then the page appears, at the address it always had.

The threshold is computed on every build rather than recorded anywhere, so
promotion happens the moment a contribution lands and nothing has to be
withdrawn by hand. Nothing moves either way: the path was always the address, so
promoting a record is *deleting* a redirect.

`dist/redirects.json` carries both kinds, and they have different lifetimes — an
alternate name is permanent, and a thin record's redirect lasts exactly as long
as it has nothing to show.

Rulings that no rule could settle travel with the thing they rule: a `note` on
the record, so `content/camera/minolta/leitz-minolta-cl/` explains its own joint
badge and `content/mount/m42/` explains why it has no brand. The rules that
shaped the whole corpus — line names folded onto their companies, one spelling
per company, who counts as the seller — are in
[`docs/rulings.md`](docs/rulings.md), each with the evidence that decided it, so
they can be argued with rather than rediscovered.

## Where it came from, and what that means for licensing

The seed corpus was extracted from English Wikipedia by
[`tools/vocabulary-build`](https://github.com/misterbisson/anchorframe/tree/main/tools/vocabulary-build)
in the app repository. Every record still carries the article and section it was
read from.

That extraction was **not** pure code — it took judgement at every turn, and
reproducing it would take more. So the files in `data/` are the source of truth
here rather than an output, and nothing regenerates them. A contributor edits
the data; [`tools/validate.py`](tools/validate.py) is what makes that safe to
accept by reading a diff instead of the whole corpus.

The data is **CC BY-SA 4.0** ([LICENSE-DATA](LICENSE-DATA)), inherited from
Wikipedia and extended to contributions here. The tools are **MIT**
([LICENSE-TOOLS](LICENSE-TOOLS)). Names on their own are facts and thin on
copyright; the selection and arrangement is not, and CC BY-SA 4.0 grants sui
generis database rights along with everything else — so rather than argue the
corpus out from under the licence it came with, it keeps it. **Share-alike
applies**: build on this and say so, under the same terms.

## What this is not right now

Named because a documented gap is a decision and an undocumented one is a trap.

- **No images.** The plan is per-image credit next to each picture — 174 of the
  201 camera photographs on Wikipedia require attribution by name, so a single
  "images from Wikimedia Commons" line would not satisfy the licence. Film and
  lens photographs have no usable source at all: searching Commons by name
  returns pictures taken *with* a stock, not *of* it.
- **No film detail.** Manufacturer, ISO, process, type and colour were all
  extracted and then cut, because nothing read them. A published reference is a
  reader, so they can come back — that is a re-run of the extraction, not a
  ruling.
- **The Hasselblad V lenses are incomplete.** The source distinguishes barrel
  versions — C, CF, CFi, CFE, F, FE, CB — in a column the extraction never read.
  Four names collided and were resolved from the source; several products the
  table lists are still missing entirely. The H-system lenses are absent for a
  different reason: the article does not enumerate them.
- **Two mounts enumerate no lenses.** Contax G and M42 have no list article to
  read. That is a fact about Wikipedia, not a bug here.
- **The camera list is film-only by construction.** The app fills its Camera
  field from any digital body that has written EXIF into the user's own library,
  so what a shipped list is *for* is the bodies no EXIF can supply.

## Working on it

```bash
python3 -m unittest discover -s tools -p 'test_*.py' -t tools
python3 tools/validate.py
python3 tools/build.py          # -> dist/, which is not committed
hugo server                     # the site, at localhost:1313
```

CI runs those, plus `hugo --panicOnWarning`, with no credentials — so it passes
for a pull request from a fork.

**Hugo builds; Python judges.** Hugo will happily render a page with a missing
brand, a mount nothing defines, or a slug that has nothing to do with its title;
it has no opinion about any of that. `tools/validate.py` does, and every rule in
it is mutation-tested.
