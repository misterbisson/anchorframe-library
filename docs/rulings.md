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

## An edition is not part of a name

`New FD` looked like a stray word and is not: it names Canon's second-generation
FD mount of 1979, which locks by bayonet where the original locks by breech. 14
lenses have a matching non-`New` record with the same optical spec, so the word
carries product identity and cannot simply go.

But **nothing on either barrel says `New`.** Canon's literature does; the lens
says `FD`. So it is the *edition's* name rather than the lens's, and as a prefix
it also put the two halves of each pair 60 rows apart in the brand list.

That is the same shape as the Hasselblad barrel codes — C, CF, CFi, CFE, F, FE,
CB — which had been welded into titles here as an admitted stopgap. Both now use
a `variant` field:

```toml
title = "FD 100mm f/2.8"
variant = "New FD"
```

**The test for adding a field was whether it was standalone, and it is not.** It
covers 55 Canon lenses and 8 Hasselblad ones today, across two makers and two
unrelated edition systems, and the Hasselblad re-extraction this file already
owes will need somewhere to put the barrel codes it recovers — the source lists
four 50 mm f/4 Distagons where this carries two.

Two consequences worth knowing. Two records can now **share a title**, so the
slug carries the variant or they would share an address; the validator refuses a
variant that the slug does not carry. And the sorting fixed itself: with the
edition out of the front of the name, each pair sorts adjacent, so no template
needed a special case for the word "New".

**What stays in the title.** `S.S.C.` and `S.C.` on Canon lenses, and Rikenon's
`XR Version`, are how the source names those products and they cause neither
ambiguity nor mis-sorting. The line is pragmatic rather than principled, and it
can move: a marker becomes a `variant` when it distinguishes editions of one
name, and stays in the title when it is simply how the thing was sold.

## A disambiguator is the encyclopaedia's problem, not the product's

Four records carried a word no product ever wore:

| was | is |
| --- | --- |
| `Canon EF camera` | `Canon EF` |
| `Canon EF-M camera` | `Canon EF-M` |
| `Kodak Vigilant camera` | `Kodak Vigilant` |
| `Polaroid 20×24 camera` | `Polaroid 20×24` |

Wikipedia cannot title two articles `Canon EF`, because the EF **lens mount**
has the same name as the 1973 body, so it appends a descriptor. That is a
property of an encyclopaedia with one flat namespace. This corpus has four —
`/library/camera/canon/ef` and `/library/mount/canon-ef` cannot collide — so it
inherits the collision's solution while having no collision, which is how the
word ended up on a badge that does not carry it.

**The tell is the capital letter, and it is Wikipedia's own convention rather
than our taste.** An appended disambiguator is lowercase; a word belonging to
the name is capitalised. `Polaroid Land Camera` and `Kodak Stereo Camera` keep
theirs on exactly that evidence — those cameras are badged that way.

This is the same rule as [the section heading was the factory](#the-section-heading-was-the-factory-not-the-badge):
the source is organised for the source's purposes, and what it needs for its own
structure is not a fact about the thing.

**`Canon New F-1` is not an instance of this and did not change.** It reads like
the `New FD` case above, but the article is explicit that the New F-1 *replaced*
the F-1n rather than re-barrelling it. A successor model keeps its own title; an
edition of one product gets a `variant`. The word "New" does not decide it — what
the word is doing decides it.

All four old addresses are public, so each is an alias and answers with a 301.

## The barrel version was a column nobody read

Zeiss made most Hasselblad V-system lenses in more than one barrel — C (1957),
F (1978), CF (1982), then CB, CFi, CFE, FE and the ZV reissue — and the source
puts that in a **Series** column of its own. The original extraction read the
name and the specification and never read that column, so it kept one row per
distinct name and silently discarded the rest.

Measured against the wikitext: the article carries **65 rows across 37
products**; this repository carried **42 records**. No product was missing
altogether, which is why it had gone unnoticed — every lens was here, most of
them once, and the 23 absent records were editions rather than lenses.

Those 23 now exist, and the 13 records that had arrived without a barrel carry
the one the source gives them. Each row is a record; `variant` holds the Series
cell verbatim, including the rows the source itself groups (`CF, CFE` is one row
because it was one optical design in two barrels, and splitting it would invent
a distinction the source does not make).

**`T*` is a coating, not an identity.** The article is inconsistent about it —
the 30 mm F-Distagon carries `T*` on its C row and omits it on CF and CFi, and
elsewhere the marker is parenthesised. So it cannot distinguish products, and
one title covers every barrel of a lens: where a product's rows disagree, the
`T*` spelling wins, because the later barrels all had it. That inconsistency was
also the only signal telling which barrel an undifferentiated record came from,
and exactly one product needed it — the 30 mm F-Distagon had two records whose
titles differed by nothing else, and pairing them by table order would have put
each under the other's barrel.

**Teleconverters are not in this list.** The article's V-system table also
carries the Mutar 1.4×, 1.7× and 2×. They have no focal length or aperture of
their own, and a photograph taken through one was taken with the lens in front
of it. Recording the converter instead would name the wrong thing.

Every renamed record keeps its old address as an alias, so nothing that was
linkable stops answering.

## The film tables had eleven columns and the corpus kept two

The 980 film records came from two Wikipedia list articles, and those articles
are tables of eleven columns. The extraction that seeded this repository read
Make and Name. ISO, Process, Type and Formats were in the source the whole time
— the same debt as the barrel version above, an order of magnitude wider.

Four of the eleven are now recorded. The other seven are refused for reasons
worth keeping, because each will be proposed again:

- **`Base`** is a column of `T` and `P`, and **the article never defines the
  letters.** Triacetate and polyester is the obvious reading and it is still a
  guess, which is not a thing to publish under a source link that does not
  support it.
- **`Dates`** has 688 of 1058 cells reading a question mark, a decade, or prose.
  `discontinued` already carries the part that is reliable.
- **`Origin`** describes the factory rather than the emulsion, and needs a
  hand-made mapping of 71 spellings. `GDR`, `USSR` and `Czechoslovakia` are
  correct for their films and must not be modernised, which makes it a curation
  job rather than a normalisation one.
- **`Details`** is prose, and prose is a body. Writing it would promote several
  hundred records to pages of their own, which is a decision about the shape of
  the site rather than about data.
- **`Replaced by`** is a relation between two records, and nothing in the schema
  expresses one.

**`Nothing` is a placeholder, not a value.** These tables use the word
deliberately and often where a cell is empty. It is the reason `Replaced by`
measures 94% full and is really 36% full — and any future measurement of this
source that does not know this will be wrong in the same direction.

**A name in two rows usually means two products.** `Agfa` Vista 400 is
`AP 70 / C-41`; `AGFA PHOTO` Vista 400 is `C-41`. Same name, different company,
either side of a bankruptcy. Fifty-nine records have a source that disagrees
with itself like this, and in each the disputed field is **left absent** rather
than set from whichever row was reached first. A record that says nothing is
honest; a record that says one era's answer is indistinguishable from one that
knows.

**ISO is a number, so it can be sorted, which costs about one film in fifty.**
Roughly 2% of cells carry two ratings — `40/50`, different markets or a change
mid-life. Those are absent rather than flattened to one number or stored as a
string that will not order. One cell reads `0`, whose own Details column says
"ASA 0, expired 9/1960" — an editor writing *nobody knows*. The validator
refused it before anything rendered it as the fastest film in the library.

**`types` rather than `type`, because Hugo owns the singular.** Setting it in
front matter picks a layout, so `type = "Print"` sends every print film looking
for `layouts/Print/`, and the failure would be a missing template rather than
anything mentioning film.

The facts render on the brand list rows, where speed and process are what tell
two films on a shelf apart. `formats` renders only on a record's own page: a
film was sold in up to eight, and eight more tokens on every line of a 102-film
list buries the names the list exists to show.

## Every metadata term is a taxonomy term

`mount` was a taxonomy and nothing else was, and the reason recorded in
`hugo.toml` was that a mount *"cuts across the other three"* and that its term
page **is** its record. Both are true of a mount and neither is the test. Being
able to ask for every C-41 film, or everything ever sold in 120, is worth a page
whether or not the term has anything else to say about itself. So `formats`,
`process`, `iso` and `types` are taxonomies too.

Making a field browsable is not free, and three things had to change first.

**A slash in a term is a path separator.** `CN-16 / C-41` slugs to
`cn-16-/-c-41`, which Hugo builds two directories deep. `process` is now a list,
which is also the truer reading: CN-16 *is* C-41 under Fujifilm's name, and
someone browsing either should find the film. Splitting the fourteen values that
carried a slash moved C-41 from 200 records to 315. The validator refuses a
slash in a `process` or a `formats` entry for this reason.

**An exposure count is not a format.** 453 records said `135` and 207 said
`135-36`, so asking for 35 mm film found two thirds of it. A 36-exposure roll
and a 24-exposure roll are the same film in the same cartridge; `135-*`
collapses to `135`, which now gathers 785. The five cells that mechanical rules
mangled — `17/30.5m` became `17` — are ruled by hand in the tool rather than by
a regex general enough to break something else.

**`types`, plural, not `film_type`.** Hugo owns the singular `type` in front
matter and uses it to choose a layout. The plural is not reserved, is what Hugo
wants as a taxonomy key anyway, and keeps the workaround out of a public URL:
`/types/slide/` rather than `/film_type/slide/`. `[permalinks.term]` can move a
term page but leaves its list page behind, and a `url` in the list page's front
matter detaches it from its own taxonomy — both were tried before the rename.

**`variant` is not one, and the values say why.** An edition name means
something only against its own product line. Every one of the thirteen belongs
to exactly one brand — `New FD` is Canon's and all eleven barrel codes are
Hasselblad's — so there is no shared vocabulary for a term page to gather. It
would be thirteen pages each duplicating a slice of one brand's list, under
labels like `C` and `F` that mean nothing away from the lens they qualify. A
taxonomy is for a word two makers both use.

Three more fields are deliberately not taxonomies, and each would be a decision
rather than a config line. **`brand`** is a section: it already has pages, and as
a taxonomy it would cut across kinds — one page for everything Kodak sold, which
is genuinely worth having and is not a rename. **`fixed_lens`** has 20 distinct
values across 26 records, so nearly every term would be a page linking to one
camera. **`discontinued`** is a boolean, and `/discontinued/true/` is not a page
anyone wants; the useful version of it is a word, not a flag.

The link into each taxonomy is computed from what a kind's records actually
carry, so film offers speeds and cameras do not, and adding a field does not
mean remembering to add a link.
