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
