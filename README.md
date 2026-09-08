# anchorframe-library

An open index of **film photography equipment** — camera bodies, lenses, film
stocks and lens mounts — one file per thing, editable by pull request.

It is published at <https://anchorframe.app/library> and it is the source of the
name suggestions in [Anchorframe](https://github.com/misterbisson/anchorframe),
a macOS app for scanned film. Neither of those is a reason to be shy about
contributing: the data is CC BY-SA 4.0 and useful to anything that needs to know
what a camera is called.

<!-- counts:start -->
| | records | brands | with a photograph |
| --- | --- | --- | --- |
| cameras | 571 | 23 | 190 |
| lenses | 1,239 | 72 | 107 |
| films | 987 | 52 | 241 |
| mounts | 30 | — | — |

Of the 987 films, **299 are still in production**.
What the two source articles say about them: speed on 896, process on
939, format on 907, and print-or-slide on 980 —
each one a term you can browse by.
<!-- counts:end -->

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

— with an alternate under `zeiss` that redirects to it. Who made a thing and
who sold it are different questions, and this answers the second.

Zeiss is in that name because **Hasselblad marketed those lenses under the
Zeiss name**, not because Zeiss made them. Angénieux designed several Nikkors
and appears in none of their titles, because Nikon sold them as Nikkor — were
a title a record of who built a thing, those would say Angénieux. A maker's
name in a title is part of what the thing was sold as; who built it is a fact
for the record's body. Six lenses badged `Schneider-Kreuznach` sit under
Samsung on the same rule — Samsung sold them and marketed them under a name it
had licensed.

**The brand is in the name as well as the path**, because a name is used away
from the path: read as a flat list, `FD 100mm f/2` names no shelf and `Nikkor`
is not a company anyone bought from. All 1,229 lens names carry their brand.
The last 109 that did not were lenses filed under Pentax that Pentax never
sold — third-party glass listed on the `Pentax K-mount` page, which took the
mount for the seller. They are on 38 new shelves now, and a lens name that
cannot carry its brand turns out to be a record whose brand is wrong.

## URLs

```
/library/camera/canon/ae-1
/library/film/kodak/portra-400
/library/lens/nikon/nikkor-45mm-f2-8e-ed
/library/mount/canon-fd            ← no brand: M42 is a thread, not a product
```

The path is the address, and it comes straight from the file's own path in
`content/`. Two consequences worth knowing before you file a pull request:

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
and never both. Other names a thing was sold under go in `aliases`, which is
Hugo's own field — so Hugo generates the redirect page and nothing here has to.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the whole shape.

## How a record earns a page

Most records are a name, a brand and a link, and a page of that is a page that
exists in order not to be a 404. So an item's URL **redirects to its row in the
brand list** until the record has something to show — prose in the body, or an
image in the bundle. Then the page appears, at the address it always had.

The threshold is computed on every build rather than recorded anywhere, so
promotion happens the moment a contribution lands and nothing has to be
withdrawn by hand. Nothing moves either way: the path was always the address, so
promoting a record is *deleting* a redirect.

Both redirects are **instant meta refreshes, not 301s**, and for the provisional
one that is the honest verb rather than a compromise: a 301 is permanent, this
redirect is designed to be revoked, and browsers cache permanent redirects hard.
An alternate name genuinely is permanent and would justify a 301 eventually;
`dist/redirects.json` keeps the two apart so that can be bought later without
rework, sized at ~3,260 keys against CloudFront KeyValueStore's 5 MB.

The cost, named: a stub answers **200**, so a link checker records a page rather
than a redirect, and anything that is not a browser will not follow it. Nothing
here is one — the app holds no network entitlement and would open a browser — but
it is true.

A brand has a page of its own too, and it carries the other names that shelf has
been known by — `Svema` answers at `/film/astrum/` as well, because Astrum is the
successor company making Svema film. Same `aliases` field, same free redirect.

Rulings that no rule could settle travel with the thing they rule: a `note` on
the record, so `content/camera/minolta/leitz-minolta-cl/` explains its own joint
badge and `content/mount/m42/` explains why it has no brand. The rules that
shaped the whole corpus — line names folded onto their companies, one spelling
per company, who counts as the seller — are in
[`docs/rulings.md`](docs/rulings.md), each with the evidence that decided it, so
they can be argued with rather than rediscovered.

## A section of another site, and the links that say so

This is published under a **prefix of `anchorframe.app`**, not on a host of its
own — `misterbisson/anchorframe-site` owns the bucket and the distribution, and
its IAM policy permits this repository exactly one prefix, `library/`. That is
the boundary; there is no licensing reason for a separate origin, because CC
BY-SA attaches to works rather than to hosts.

Sharing a hostname is not the same as being reachable from it, and for months it
was not: `baseURL` here is this section's root, so every page linked back only to
`/library/`, and nothing on the site linked in. Two halves of one hostname that
could not reach each other. Nothing 404s when that is true and no build goes red,
which is why it lasted — the cost is a reader who arrives on a camera from a
search engine and has no path to the app this index feeds, and these are the
pages a search engine has any reason to return.

So the masthead's wordmark is **two links**: `Anchorframe` leaves for the apex,
`equipment library` returns to this root. The breadcrumbs start one level higher
for the same reason, and the footer says what the index is for. The apex is
`params.app` in `hugo.toml`, written once.

**`tools/test_library_masthead.py` pins the literal, and the other repository
pins the same one** in its `tools/test_library_link.py`, which also asserts the
inbound half — `Library` in that site's nav and footer. Neither repository can
read the other; both assert the same string; either one drifting turns its own
side red. Exactly the arrangement already used for the OIDC subject in
[`tools/test_deploy_subject.py`](tools/test_deploy_subject.py).

What no test here can do is prove the apex answers. `tools/check_stubs.py` checks
links into *this* site and skips absolute URLs by construction, which is right —
a link checker that fetched the wider web would go red on somebody else's outage.
What does cover it is `deploy.yml`, which already curls `/privacy` and `/support`
on every publish because this job shares a distribution with them.

## Where it came from, and what that means for licensing

The seed corpus was extracted from English Wikipedia by
[`tools/vocabulary-build`](https://github.com/misterbisson/anchorframe/tree/main/tools/vocabulary-build)
in the app repository. Every record still carries the article and section it was
read from.

That extraction was **not** pure code — it took judgement at every turn, and
reproducing it would take more. So the files in `content/` are the source of truth
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

- **Photographs are mostly of cameras.** The table above says how many of each
  kind carry one. That ceiling is Wikipedia's rather than ours: measured on
  2026-09-04, 341 cameras had an article of their own, 201 of those a lead
  image, and 11 of *those* are refused — 8 name no author, so the licence
  cannot be satisfied, 2 are local en.wiki uploads rather than Commons files,
  and 1 states no licence.

  Film and lens photographs have no usable source **on Commons**. Searching by
  name returns pictures taken **with** a stock or a lens, not **of** it —
  measured at 16% and 13% of names returning anything, and most of those wrong.
  `Holga 400` returns a photograph of a fountain.

  For film the shortage is structural rather than a gap someone could fill. A
  box is a graphic work and it is the whole subject of a picture of one, so a
  photograph of a box has two copyright holders — whoever pressed the shutter
  and whoever drew the box — and a contributor can only license their half. The
  free-licensed snapshot is the *unsafe* one; the manufacturer's own product
  shot, where one owner holds both halves, is not. The films that carry one are counted above, each marked
  `fair-use`, which is a use and not a licence and so does not travel to anyone
  reusing this data. [`tools/film-boxes`](https://github.com/misterbisson/anchorframe/tree/main/tools/film-boxes) in the app repository says
  where each brand's own catalogue is and which brands have none — it is not
  here for the same reason `tools/vocabulary-build` is not: a public index
  should not also ship the thing that fetches from vendors under its name.
  Most of the films here are discontinued, and a discontinued stock has nobody
  left to ask.
- **Four of the source's eleven columns, not all of them.** Speed, process,
  format and print-or-slide are recorded and browsable; the counts are in the
  table above. Five columns are refused for reasons in
  [docs/rulings.md](docs/rulings.md), and the short version is that each would
  mean publishing something the source does not support: `Base` is a column of
  `T` and `P` the article never defines, `Dates` is mostly a question mark or a
  decade, `Origin` describes the factory rather than the emulsion, and `Details`
  and `Replaced by` are prose and a relation that would change the shape of the
  site.
- **One of the source's six Hasselblad lens sections is deliberately unread.**
  The V-system, Aerial, 1600F/1000F, H-system and XPan lenses are all here; the
  X-system ones are refused because that system is digital and no X body exists
  in a library of film equipment. The V-system barrel versions — C, CF, CFi,
  CFE, F, FE, CB — went unread until the column was measured against the source
  and 23 editions were missing.
- **Only 9 of the 30 mounts actually join a body to its glass.** Sixteen have
  bodies and no lenses — Canon FL, Contax G and RF, Konica AR and KM, M42, both
  Mamiya mounts, Minolta A and SR, Nikon S, Pentax 645 and K-F, Rollei QBM,
  Ricoh RK and Tenax — because the camera side names more mounts than the lens
  sources enumerate. An earlier version of this file said "two mounts enumerate
  no lenses"; that was the count of lens sources that came back empty, not the
  count of mounts with nothing on the other side, and it understated the gap by
  eight times. The mount index says so on every row now rather than leaving it
  here.

  Five go the other way, and all five are the same defect rather than a
  shortage: `Hasselblad V`, `1600F`, `H` and `XPan`, and `Fuji GX680` have
  lenses *and* bodies, but those bodies were read from articles listing many
  cameras rather than from articles of their own, so there was no infobox to
  name a mount. **Of the 231 cameras established to take interchangeable
  lenses, 148 — 64% — say which mount.** The rest is measured in
  [docs/rulings.md](docs/rulings.md).
- **The camera list is film-only by construction.** The app fills its Camera
  field from any digital body that has written EXIF into the user's own library,
  so what a shipped list is *for* is the bodies no EXIF can supply.

## Working on it

```bash
tools/check.sh                  # everything CI runs, in the order CI runs it
hugo server                     # the site, at localhost:1313
```

Run `tools/check.sh` rather than its parts. Twice a check passed locally and
failed on push because the local command differed by a flag: the stub detector
was written against unminified markup where the publish builds with `--minify`,
and a deprecated config key logged an error that a local `--quiet` swallowed. A
check verified against a different build than the one that ships is not a check.

CI runs exactly that script's contents with no credentials, so it passes for a
pull request from a fork.

**Hugo builds; Python judges.** Hugo will happily render a page with a missing
brand, a mount nothing defines, or a slug that has nothing to do with its title;
it has no opinion about any of that. `tools/validate.py` does, and every rule in
it is mutation-tested.
