# Contributing

Adding a camera, lens or film stock is **one new file**. Correcting one is a
one-line diff. Both are welcome, and neither needs you to run anything —
CI will tell you if something is off — though running the validator locally is
faster than waiting for it.

```bash
python3 tools/validate.py
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
| `note` | | Why, where a reader would otherwise ask. |

## Prose and pictures are the most useful thing you can add

A record with only front matter has no page of its own — its URL redirects to
its row in the brand list, because a page carrying a name and a link is a page
that exists in order not to be a 404.

Write a paragraph in the body, or drop an image into the bundle, and the page
appears by itself on the next build. Nothing is renamed and no redirect has to
be removed by hand.

An image needs its own credit, because most of the photographs worth using are
licensed on that condition — a single site-wide "images from Wikimedia Commons"
line does not satisfy CC BY. Put the file in the bundle beside `index.md` and
give it a `credit`, a `license` and a `sourcePage`.

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
