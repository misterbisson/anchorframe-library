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

```json
{
  "name": "Canon AE-1",
  "brand": "Canon",
  "mount": "canon-fd",
  "source": "https://en.wikipedia.org/wiki/Canon_AE-1"
}
```

`name`, `brand` and `source` are required on everything. A film says whether it
is `discontinued`; a fixed-lens body names its `lens` instead of a `mount`, and
never both. `note` carries a reason where one is needed. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the whole shape.

Rulings that no rule could settle — line names folded onto their companies, the
mount spellings, brands read out of an article's own prose — live in
[`tools/rulings.py`](tools/rulings.py), each with the evidence that decided it,
so they can be argued with rather than rediscovered.

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
```

CI runs exactly those three, with no credentials, so it passes for a pull
request from a fork.
