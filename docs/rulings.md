# Rulings

Decisions a person made, where the sources could not settle it.

**Where they live now.** A ruling about one thing is a `note` on that thing —
`content/camera/minolta/leitz-minolta-cl/index.md` explains its own joint badge,
and `content/mount/m42/_index.md` explains why it has no brand. This file carries
only the rules that shaped the whole corpus, because there is nowhere else to
attach them.

`tools/rulings.py` used to hold all of this as Python, and was deleted when the
corpus became Hugo content: the mount records were duplicated between it and
`content/mount/`, and a second source of truth that nothing reads is worse than
no record at all — someone would have edited it and watched nothing happen.

## A brand is who sold a thing, not who built it

The one idea the whole schema turns on, and the one thing most likely to be
wrong in a well-meant pull request.

`manufacturer` is a fact about a supply chain: often unrecorded, sometimes
contested, and not what is written on the front. Minolta built the Leica CL.
Vivitar never ground a lens. Zeiss made Hasselblad's V-system glass and Fuji
made its H-system glass, and neither got a badge. This index is reached by
typing what is on the front, so it answers the second question.

## A product line is not a company

`Nikkor` is what Nikon writes on its glass; nobody bought a lens from a company
called Nikkor. Each of these was folded onto the company that sold it, and the
line name became an alternate address that redirects:

| line | company |
| --- | --- |
| Canonet, Nikkor → | Canon, Nikon |
| Fujinon, Instax | Fujifilm |
| Hexanon | Konica |
| Leitz | Leica |
| Nippon Kogaku | Nikon |
| Rokkor | Minolta |
| Rolleicord, Rolleiflex | Rollei |
| Takumar | Pentax |
| Zuiko | Olympus |

## One company, one spelling

`Fuji` and `Fujifilm` are the same firm, and the film sheets already said
`Fujifilm`; letting both stand would have split the namespace down the middle of
one maker. Likewise `Carl Zeiss` → `Zeiss` and `Schneider` →
`Schneider Kreuznach`. The unused spelling redirects.

## An article whose subject sold everything it lists

Only one source needed this: `List of lenses for Hasselblad cameras`. There the
*name* carries the maker where the source's structure does not, so 44 lenses
resolved to Zeiss, Schneider and Rodenstock and had to be moved.

Every other multi-maker source was checked before this became a rule — the Canon
FD, Leica, Olympus OM and Pen F lists all resolve correctly on their own,
because there the name and the seller agree.

## What is still unsettled, and visible

- `content/mount/pentax-kf/` — one spelling, one body, and nothing establishes
  whether the source means a distinct mount or a spelling of the K. Kept apart
  rather than silently folded into its neighbour.
- `content/mount/contax-rf/` — the source says only `Contax bayonet`, which
  names the rangefinder mount and the SLR mount equally well.
- The Hasselblad V lenses are incomplete: the source lists four 50 mm f/4
  Distagons and five 80 mm f/2.8 Planars where this carries two of each. That
  is a re-extraction, not a ruling.

## A brand is a shelf, and a shelf can have more than one name

Two different problems arrived looking like one.

**Corporate lineage is not a shelf.** `List of photographic films` heads its
sections with whichever legal entity made a stock, so one badge arrived as
several brands: `Agfa`, `AGFA PHOTO`, `AgfaPhoto` and `Agfa-Gevaert`; `ADOX` and
`ADOX (Fotoimpex)`; `Ilford` and `Ilford Imaging (Europe)`; `Polaroid` and
`Polaroid B.V.`; `Ferrania` and `FILM Ferrania`.

The records themselves settle it. Every one of those titles already reads
`Ilford Ilfochrome 100`, `Polaroid Originals Spectra film`, `Agfa Photo APX
400`. Nobody's box says *Ilford Imaging (Europe)* — that name existed only in a
section heading. So the name on the box stays in `title`, and `brand` is the
shelf you look on.

**Every collapsed name still answers.** The old brand address is an alias on the
surviving brand's page, and each moved record keeps its old address too. A brand
alias is not only for old URLs, though: `Svema (Astrum)` became `Svema` with
both `/film/svema-astrum/` and `/film/astrum/` pointing at it, because Astrum is
the successor company making Svema-branded film and someone looking for either
name wants the same shelf.

**What was deliberately not collapsed.** `Harman`, `Ilford` and `Kentmere` are
one company and three shelves — Harman Phoenix, HP5 and Kentmere 100 are
different things a person buys by name. `Gevaert` predates the Agfa merger and
sold its own film. `Original Wolfen` and `ORWO` share a lineage and are both
sold today under their own names.

## The section heading was the factory, not the badge

`3M` was missing entirely, and the reason is the sharpest example of the
sold-under rule failing at its source: 3M owned Ferrania's plant, so
Wikipedia filed 43 films under **Ferrania** whose boxes said 3M, Scotch or
Imation.

Sorted by what is on the box: **28 to `3M`** (with `/film/scotch/` as a brand
alias, since Scotch is a 3M line and a line is not a company), **6 to
`Imation`**, and **7 left under Ferrania** because they are genuinely co-badged
— `3M Ferrania CR50`, `Ferrania / 3M P30`. Three sold first as 3M and later as
Imation are addressed under 3M with an Imation alias.

Each moved record keeps its `/film/ferrania/…` address.

## What looked wrong and was not

**`New FD` is Canon's own designation**, not a stray word. It names the
second-generation FD mount of 1979, which locks by bayonet where the original
locks by breech. 61 lenses carry it, and **14 of them have a matching non-`New`
record with the same optical spec** — strip the word and those 14 collide, which
is exactly the evidence that it carries product identity.
