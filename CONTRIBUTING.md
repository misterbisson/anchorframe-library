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
data/<camera|film|lens>/<brand>/<model>.json
data/mount/<mount>.json
```

The path becomes the URL, so both segments are slugs: lowercase, ASCII,
hyphen-separated, **no dots** (see the README for why a dot breaks the router).

## What a file holds

| field | | |
| --- | --- | --- |
| `name` | required | What is written on the thing, as a person would type it. |
| `brand` | required | **Who sold it**, not who built it. See below. |
| `source` | required | An `https` URL that says this thing exists. |
| `mount` | | The slug of a record in `data/mount/`. |
| `lens` | | The fixed lens a body was built around. Never alongside `mount`. |
| `discontinued` | films | `true` or `false`. Required on a film, refused elsewhere. |
| `alternates` | | Other addresses that redirect here: `{"brand": …, "slug": …}`. |
| `note` | | Why, where a reader would otherwise ask. |

## The rules that get pull requests turned down

**Brand is who sold it.** Vivitar never ground a lens; a Vivitar lens is a
Vivitar. Hasselblad's V-system glass is Zeiss-built and files under Hasselblad,
with `zeiss` as an alternate. Minolta built the Leica CL, and it is a Leica.
This is the single thing most likely to be wrong in a well-meant pull request.

**A line is not a company.** Nikkor is Nikon, Zuiko is Olympus, Takumar is
Pentax, Fujinon is Fujifilm. The line name stays in `name` and becomes an
alternate; it is not a brand directory. The full list is in
[`tools/rulings.py`](tools/rulings.py).

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

## Adding a mount

A mount record carries a `name`, every `spelling` seen in the wild, and a
`brand` **only if one owns it**. M42 does not — it is a thread that Praktica,
Pentax, Zenit and Chinon all used — which is why mount URLs have no brand
segment. Two mounts may not claim the same spelling; that is what makes the join
between a body and its glass unambiguous.

## Licence of what you contribute

Data is CC BY-SA 4.0 and tools are MIT. Opening a pull request means you are
willing for your contribution to ship under those.
