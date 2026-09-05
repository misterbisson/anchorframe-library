# Contributing

Adding a camera, lens or film stock is **one new file**. Correcting one is a
one-line diff. Both are welcome, and neither needs you to run anything —
CI will tell you if something is off — though running the validator locally is
faster than waiting for it.

```bash
python3 tools/validate.py       # the corpus alone, and fast
tools/check.sh                  # everything CI runs, including the site build
```

## Where a file goes

```
content/<camera|film|lens>/<brand>/<model>/index.md      ← plus its images
content/mount/<mount>/_index.md
```

A record is always a **directory** holding `index.md`, never a bare `.md` file,
so there is somewhere obvious to put a photograph. The path becomes the URL, so
every segment is a slug: lowercase, ASCII, hyphen-separated, **no dots** (see
the README for why a dot breaks the router).

## What a file holds

Front matter is TOML, between `+++` fences. Anything after it is the page body,
and it is optional.

```toml
+++
title = "Canon AE-1"
brand = "Canon"
source = "https://en.wikipedia.org/wiki/Canon_AE-1"
mount = ["canon-fd"]
+++
```

| field | | |
| --- | --- | --- |
| `title` | required | What is written on the thing, as a person would type it. |
| `brand` | required | **Who sold it**, not who built it. See below. |
| `source` | required | An `https` URL that says this thing exists. |
| `mount` | | A list, holding the slug of a term in `content/mount/`. |
| `fixed_lens` | | The lens a body was built around. Never alongside `mount`. |
| `discontinued` | films | `true` or `false`. Required on a film, refused elsewhere. |
| `aliases` | | Other addresses that redirect here, as `["/lens/zeiss/planar-t-80mm-f2-8-c/"]`. Hugo's own field, so it builds the redirect. No `/library` prefix: Hugo adds it. |
| `variant` | | An edition of this title — `New FD`, `CF`. See below. |
| `note` | | Why, where a reader would otherwise ask. |

## Editions of one product

Canon's 1979 FD lenses say only `FD` on the barrel; `New FD` is Canon's word for
the edition. Hasselblad's C/CF/CFi/CFE barrels are the same. When a marker
distinguishes editions of one name rather than naming the thing itself, it goes
in `variant`:

```toml
title = "FD 100mm f/2.8"
variant = "New FD"
```

Two records may then share a title, so the **slug has to carry the variant** —
`fd-100mm-f2-8-new-fd` — or the two editions would want one address. The
validator refuses a slug that does not.

Leave a marker in the title when it is simply how the thing was sold: Canon's
`S.S.C.` coating and Rikenon's `XR Version` are part of those names.

## Prose and pictures are the most useful thing you can add

A record with only front matter has no page of its own — its URL redirects to
its row in the brand list, because a page carrying a name and a link is a page
that exists in order not to be a 404.

Write a paragraph in the body, or drop an image into the bundle, and the page
appears by itself on the next build. Nothing is renamed and no redirect has to
be removed by hand.

## Adding a photograph

Put the file in the bundle beside `index.md`, and declare it. **A photograph
with no credit fails the build** — this is the one thing here that can put
someone in breach of a licence, so it is checked rather than trusted.

```toml
[[resources]]
src = "ae-1.jpg"
[resources.params]
credit = "Charles Lanteigne"
license = "CC BY-SA 3.0"
licenseUrl = "https://creativecommons.org/licenses/by-sa/3.0/"
alt = "A silver and black Canon AE-1, front three-quarter view"
sourcePage = "https://commons.wikimedia.org/wiki/File:Canon_AE-1_..."
verified = "2026-09-04"
```

All five are required. `credit` because most of these licences ask for
attribution **by name**, and a single site-wide "images from Wikimedia Commons"
line does not satisfy CC BY — the credit renders beside the photograph.
`sourcePage` is the *file's* page, not the article: that is where the licence and
the author are stated and what a reuser has to be able to reach. `alt` is what
the photograph shows, for a reader who cannot see it.

`verified` is the day someone last opened that `sourcePage` and confirmed it
still says what the credit says. Every other field describes the day the file
arrived; this is the only one that can stop being true without a commit. A
Commons file can be deleted — routinely, and for the licensing reasons this
whole scheme is about — and a vendor's product page can move, leaving a
photograph here whose credit has been withdrawn at the source and nothing
saying so. Claims left unconfirmed for more than 550 days fail the build. The
answer is to re-check them and move the dates, not to raise the number.

**The licence has to be one this repository can redistribute.** Public domain,
CC0, CC BY, CC BY-SA, GFDL and a few others; anything else is refused by name.

**`CC BY-NC` is not `CC BY`**, however much it reads like it, and it is refused.
These pages support a paid application, so a picture licensed for
non-commercial use only does not belong on them — that would be our breach as
publisher, not a later contributor's.

**`CC BY-ND` is accepted, but do not edit one.** Serving it is fine: the resize
that renders it is a technical modification the licence expressly allows, and
`.Fit` scales rather than crops. Cropping or retouching it is not fine, and
unlike the share-alike case there is no note you can add that makes it so. If a
photograph needs an edit to be useful, find a differently-licensed one.

**Except a film box, where no free photograph can exist.** The box is a graphic
work and it is the whole subject, so a photograph of one has two owners and a
contributor can only license their half — a CC BY-SA snapshot of a Portra box is
a licence to half the frame. The manufacturer's own product shot has one owner,
so that is what to use, marked `fair-use`:

```toml
[[resources]]
src = "fujichrome-velvia-50-box.png"
[resources.params]
credit = "FUJIFILM Corporation"
license = "fair-use"
copyright = "FUJIFILM Corporation"
alt = "Boxes of FUJICHROME Velvia 50 in 135 and 120"
sourcePage = "https://www.fujifilm.com/us/en/business/professional-photography/film/velvia-50"
verified = "2026-09-04"
```

`fair-use` takes a `copyright` and no `licenseUrl`, because there are no terms to
link to — and it is a *use*, not a licence: it cannot be passed on, the corpus's
CC BY-SA 4.0 does not cover it, and a reuser of this data does not inherit it.
Use it only for the maker's own photograph of their own product, never for
someone else's picture of it.

[`tools/film-boxes`](https://github.com/misterbisson/anchorframe/tree/main/tools/film-boxes) in the app repository finds those, the same way
`tools/vocabulary-build` built the seed corpus: it runs on a person's machine and
its output is committed here. It reports what each maker's own catalogue offers
and which record it matches, and writes nothing on its own — matching a shop's
product name to a record is a judgement, and it belongs in a diff someone reads.

It lives there rather than here because a public index should not also ship a
thing that fetches from eleven vendors' sites under this repository's name. The
goodwill of those vendors is what the `fair-use` position rests on.

**Take files from Wikimedia Commons, not from English Wikipedia.** Wikipedia
also stores files locally, and local is where non-free *fair-use* uploads live —
from the article side they look identical. Two of the 201 camera images are
local, and nothing about the article tells you which. **Check that the file page
you are citing is on `commons.wikimedia.org`** — that is the whole test, and the
one thing about an image a reviewer cannot verify for you from the article alone.

[`tools/vocabulary-build`](https://github.com/misterbisson/anchorframe/tree/main/tools/vocabulary-build)
in the app repository holds the fetcher that took the first 190 of these, beside
the extractor that produced the names, and it is there for the same reason
`tools/film-boxes` is: it runs on a person's machine and its output is committed
here.

A crop or any other edit makes a derivative, which CC BY-SA carries its
share-alike into. Say so in the record's `note` if you edit one.

## The rules that get pull requests turned down

**Brand is who sold it.** Vivitar never ground a lens; a Vivitar lens is a
Vivitar. Hasselblad's V-system glass is Zeiss-built and files under Hasselblad,
with `zeiss` as an alternate. Minolta built the Leica CL, and it is a Leica.
This is the single thing most likely to be wrong in a well-meant pull request.

**A line is not a company.** Nikkor is Nikon, Zuiko is Olympus, Takumar is
Pentax, Fujinon is Fujifilm. The line name stays in `name` and becomes an
alternate; it is not a brand directory. The full list is in
[`docs/rulings.md`](docs/rulings.md).

**Everything cites something.** Wikipedia is where the seed corpus came from,
but it is not a requirement — a manufacturer's page, a manual, a catalogue scan
all work. What is refused is a record with nothing behind it. If your source is
not on the web, say so in `note` and link the closest thing.

**A slug is frozen once published.** If a name was wrong, fix `name` and leave
the filename alone. If the address itself must change, move the file and add the
old `brand`/`slug` pair to `alternates` so the old URL keeps answering.

**A rebadge is two records, not one.** The Leica CL and the Leitz Minolta CL are
one camera sold under two names in two markets, so they are two records — two
things a person types. An *alternate* is for one product with two names under
**the same** brand.

**The camera list is film only.** Digital bodies are covered elsewhere and are
removed on sight.

## A brand can have other names

A brand is a shelf, and `content/<kind>/<brand>/_index.md` is its page. It
carries a `title` that must slug to its own directory, and `aliases` for every
other name the shelf has been known by:

```toml
+++
title = "Svema"
aliases = ["/film/svema-astrum/", "/film/astrum/"]
+++
```

Use one when a name is **the same shelf**: a corporate rename, a successor
company, a spelling nobody agrees on. Do not use one to merge two shelves —
Harman, Ilford and Kentmere are one company and three things people buy by name,
so they stay three brands. Collapsing a brand is safe after publishing precisely
because the old address becomes an alias and keeps answering.

## Adding a mount

A mount record carries a `name`, every `spelling` seen in the wild, and a
`brand` **only if one owns it**. M42 does not — it is a thread that Praktica,
Pentax, Zenit and Chinon all used — which is why mount URLs have no brand
segment. Two mounts may not claim the same spelling; that is what makes the join
between a body and its glass unambiguous.

## Licence of what you contribute

Data is CC BY-SA 4.0 and tools are MIT. Opening a pull request means you are
willing for your contribution to ship under those.
