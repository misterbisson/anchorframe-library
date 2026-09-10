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
Vivitar never ground a lens. This index is reached by typing what is on the
front, so it answers the second question.

**A maker's name in a title is there because the seller marketed it that way,
not because the maker made it.** `Hasselblad Zeiss Planar T* 80mm f/2.8 C`
carries Zeiss because **Hasselblad marketed the V-system lenses under the Zeiss
name**, not because Zeiss ground the glass. Fuji built the H-system lenses and
Hasselblad did not sell them under Fuji's name, so a Fuji-carrying title would
be wrong — though nothing here demonstrates that, because all 67 Hasselblad
lenses in this corpus are V-system and there is not one H-system lens to check
against. That gap is [issue #44](https://github.com/misterbisson/anchorframe-library/issues/44).

The case that proves it is Angénieux. Angénieux designed the Nikkor 200mm
f/2.8 DEM ED and its neighbours, and **no Angénieux name appears in any of
those titles**, because Nikon sold them as Nikkor. Were the title a record of
who made a thing, it would say Angénieux; it says Nikon Nikkor, which is how
the lens was sold. The Angénieux detail belongs in a record's body, where an
interesting fact about a thing goes.

So a title may carry a second company's name, and when it does that name is
part of what the thing was sold as — never a claim about the factory.

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

## A lens name carries its brand, because a list has no directory

The brand is the path here, so `FD 100mm f/2` under `/lens/canon/` says Canon
without repeating it, and for two hundred pull requests that was enough. It is
not enough anywhere the path is gone. Read as a flat list — a suggestion field,
an export, a search result — Nikon's 275 lenses said `Nikkor` and never `Nikon`,
and 741 of 1,229 names did not name the shelf they came off.

So a lens title carries its brand. 605 titles gained one across nine brands, and
**no slug moved**: `validate.py` already accepted a title whose slug drops a
repeated brand prefix, which is what made this a rename of names rather than of
addresses. The cost, named: on `/lens/canon/` every row now begins with the word
Canon, under a heading that says Canon. That is the price of the name being true
away from the page, and away from the page is where a name is used.

The rule is **the brand's words appear in the title**, not *at the front of* it.
`SMC Pentax 500mm f/8` and `Carl Zeiss 100mm f2 Makro-Planar` already say who
sold them; prefixing on position alone would have written `Pentax SMC Pentax`
and `Zeiss Carl Zeiss`, and `Schneider-Kreuznach D-Xenogon` — one brand spelled
with a hyphen — would have gained a second copy of itself. 515 titles were left
alone by that test.

**Nine brands took it; Pentax did not, and that is a defect rather than a
style.** 109 lenses filed under Pentax came off `Pentax K-mount`, an article
that lists the **third-party** glass fitting K: Kiron, Revuenon, Porst, Sun,
Laowa, Irix, and the whole Zenit line — Zenitar, Helios, Mir, Peleng, Volna.
Their brand is the mount's brand because the article they were read from is the
mount's. `Pentax Kiron 28–70mm f4 Macro` is a lens that never existed, and
writing it would turn a filing error into a claim.

This is the same mechanism as [the section heading was the
factory](#the-section-heading-was-the-factory-not-the-badge) and the reason
`Canon P` once arrived as `Leica Canon P`: **the article's own organising
principle is not a fact about the thing.** The difference is that here it was
caught before the name was written rather than after. Two of the 109 are
genuinely Pentax — `Takumar 135mm f2.5` and `Takumar A 28–80mm` — and the rest
want a person establishing who sold each one.

`test_a_lens_name_says_whose_shelf_it_came_off` counts the held set rather than
describing it, so the number may only go down, and only deliberately.

## A licensed name is not the seller either

Six lenses sat on the Schneider Kreuznach shelf — half of everything on it —
and Schneider Kreuznach neither sold them nor made them. The source says so
outright, in the section the records were read from:

> All these lenses had been **marketed by Samsung** […] They **license their
> name to Samsung** […] All the Schneider branded glass from Samsung is
> **manufactured by Pentax**

So the badge reads Schneider-Kreuznach, the glass is Pentax's, and the company
that sold them is Samsung. The brand is who sold it, which makes these
`Samsung`, and the corpus had no Samsung shelf at all until now. The licensed
name stays in the title the way `Hasselblad Rodenstock Apo-Grandagon` keeps
Rodenstock: the brand says who sold it, and the name says what the seller
marketed it as, which here is a name Samsung licensed rather than one it
owned.

This is the same defect as [the 109 K-mount lenses filed under
Pentax](https://github.com/misterbisson/anchorframe-library/issues/42) arriving
by a different route, and it is worth separating the two. Those took the brand
from the **article** they were read from. These took it from their own **title**
— which is why they slipped through the rename in #41 that had to hold the other
109: `Schneider-Kreuznach` is one word with a hyphen and two words to a slug, so
a title already carrying both of the brand's words looked finished.

Each keeps its `/lens/schneider-kreuznach/…` address as an alias, and the
earlier `/lens/schneider/…` alias with it, so neither move costs a URL.

## The mount was never the seller

109 lenses were filed under Pentax and Pentax sold none of them. They came off
`Pentax K-mount`, an article enumerating the **third-party** glass that fits K,
so the extraction took the article's own subject as the brand — the same
mechanism that once produced `Leica Canon P` and that filed six Samsung lenses
under a name Samsung had only licensed.

They are now on the shelf of whoever sold each one: **38 new brands**, from
Kiron and Kiron's rebadger Lester A. Dine to Revuenon, Porst, Zenitar and
Venus Optics. Every one keeps its `/lens/pentax/…` address as an alias.

**The section heading was the answer**, which is worth stating because the
opposite ruling exists two sections up. There, `Ferrania` headed films whose
boxes said 3M — the heading named the plant. Here the headings name what is
written on the lens, and twenty shelves in this corpus were already built from
them: `access`, `beroflex`, `kalimar`, `makinon`, `miranda`, `soligor`,
`spiratone` all came from sections of this same article. The 109 are the ones
whose maker had no shelf yet, so they fell through to the mount. **A heading is
neither trustworthy nor suspect on principle; what it names has to be checked.**

Several are house brands rather than manufacturers — Revuenon and Revue are
Foto-Quelle's, Porst is Photo Porst's, Focal was Kmart's, Quantaray was Ritz's,
JC Penney sold under its own name. A house brand is the right answer, not a
defect: it is exactly what "who sold it" asks.

Three exceptions, each on an existing rule.

**`Special lenses` is not a brand.** Two records sat under an optical category;
both titles say Zenitar and both went there.

**Takumar is Pentax's own line, and a product line is not a company.** The two
Takumars were the only members of the held set that really were Pentax. They
keep their address and gained only a name: `Pentax Takumar 135mm f2.5 prime`.

**One importer, two spellings.** Eight titles read `Tou/Five Star` and one read
`Toyo/Five Star`; the section heading says Tou, so that is the spelling kept.

With this the naming rule from #41 loses its exception list. **1,229 of 1,229
lens names carry their brand**, and the test that held 109 slugs now asserts
the empty set — a lens that cannot satisfy it has a `brand` that is wrong,
which is what all 109 turned out to be.

## A digital-only system is out of scope

This is a library of film equipment, so a body that never took film does not
belong in it and neither does glass made only for one. Hasselblad's X system —
the X1D and its XCD lenses — is the case that asked the question, and the
answer is no: there is no X-system body anywhere in this corpus and there
should not be.

When the ruling was written nothing had to be removed to establish it: four of
the six Hasselblad lens sections were never imported at all, so the X system was
already absent. **The Leica S was not.** Sixteen S-system lenses and their
`leica-s` mount were in the corpus, and the article's own first sentence settles
them: *the Leica S-System is a medium format **digital** single lens reflex
camera system*. Every body it names — S1, S2, S, S3 — is digital. They are
removed.

That is the first deletion of published URLs here, so the cost is worth naming.
None of the sixteen had earned a page: each was a provisional redirect to its
row on the Leica shelf, the kind this README already calls *designed to be
revoked*. What breaks is sixteen redirects, not sixteen pages. A redirect to the
Leica shelf instead would have been worse than a 404 — it would keep asserting
that Leica sells this as film glass. The other three sections — 1600F / 1000F,
H system and XPan — stay in scope, because this corpus already holds those
bodies.

**A system that took film and later went digital is in.** The H1 and H2 accept
film magazines, so H-system lenses are film lenses that happen to have outlived
film. The test is whether a body ever took film, not whether its maker still
sells one.

Checked rather than assumed: the corpus was searched for the digital-only lines
most likely to have arrived by accident — Canon EOS R, Nikon Z, Sony E, Leica
M8 through SL, Micro Four Thirds, the Fujifilm X bodies, the Pentax K digital
range — and holds none of them. The three records that matched on a word are
`Lomography Peacock X-Pro`, which is a cross-processing film, and the film
`Canon EOS-1` and `Minolta Maxxum 4`, whose bodies mention their digital
successors.

## Four sections of one article, and only two were read

`List of lenses for Hasselblad cameras` has six lens sections. The first pass
took two — V system and Aerial — so the library held the 1600F, the 1000F, the
XPan and four H bodies and listed no glass for any of them. Nobody noticed for
forty pull requests, because a gap looks exactly like a subject with nothing to
say. It surfaced only when a ruling here claimed something about H-system
lenses and there was not one in the corpus to check it against.

**26 lenses now come from the three film sections.** The X system is not among
them, on the ruling above.

These tables needed their own reader, which is the part worth recording.
`wikitable.py` was written for the film lists, where `!` marks a header and `|`
marks data. **Here a data row leads with `!` cells** — the focal length and
aperture are styled as headings — so that parser files half of every row as a
column name and yields nothing at all.

`{{f/|3.5|22}}` had to survive too. `wikitable.clean` drops every template,
which is right for the film tables and would have silently deleted the aperture
from every row here, leaving 26 lenses with no maximum aperture and no error.

**The 1600F section carries `variant = "1600F"` throughout.** The V system
reissued several of those Zeiss designs and the corpus already tells its C, CF
and CFi editions apart that way; two of the eleven collide by title alone, the
Biogon 38mm f/4.5 and the Sonnar 250mm f/5.6. Setting the variant only on the
two that collide would make a record depend on what else happened to be in the
corpus that day.

**The teleconverter is not a lens.** `H 1.7X Converter` sits in the H table and
no converter is a record anywhere in this corpus, so it is refused by its focal
length column failing to be a focal length — with a test saying so, rather than
leaving it to a regex nobody reads.

Three mounts are new: `hasselblad-1600f`, `hasselblad-h`, `hasselblad-xpan`.

## A mount marker that does not look like a mount name

113 lens photographs arrived and six were the wrong lens. Every one was a modern
mirrorless barrel standing in for its film-era namesake: `NIKKOR Z 85mm f/1.8 S`
against the F-mount `Nikkor 85mm f/1.8`, `Sigma 28-70mm DG DN` against the
K-mount `EX DF ASP`. Thirty years and one incompatible mount apart, and
identical on the two facts a lens name is made of.

**A lens name is a focal length, an aperture and a pile of mount letters nobody
spells the same way**, so matching runs on the numbers. The numbers were right.
The importer did check mounts — and that check compares mount *names*, which
cannot see a bare `Z` sitting between the brand and the focal length, or a `DN`
at the end. A mount marker that does not look like a mount name is invisible to
a matcher that is looking for mount names.

So the vocabulary is explicit, and the refusal is on **asymmetry**: a file whose
own name claims a digital-only generation the record does not. Presence alone
would be wrong — `Sigma 30mm f/1.4 EX DC` is a real record here whose photograph
is correctly a DC lens, and nine more like it would have been thrown away.

Two refinements the corpus itself forced.

**`RF` on its own is too cheap.** `Hexar_rf-1-weba.jpg` is a Konica film
rangefinder, and the first draft refused it as a Canon RF-mount lens. Canon's
mount is named beside a focal length, so the pattern says so.

**Leica writes its mount as a suffix.** `APO-Summicron-SL` never says
`Leica SL`, so a rule keyed on the brand-plus-mount form would miss the whole
L-mount range.

This lives in `validate.py` rather than in the importer that made the mistake,
and that is the more useful half of the ruling. **The importer was never
committed** — 113 files landed in this repository from a tool that exists in
neither, so there was no importer to fix. A rule in the validator holds for any
image, from any tool, from anybody, including the next person doing this by
hand.

Its near relative is [the Polaroid Impulse](#a-format-is-what-joins-a-body-to-a-stock),
whose `type` reads `3-element 116mm f/9.4 plastic lens` and where 116 is a real
film format. Both are a matcher finding the right numbers on the wrong object.

## The caption was bad alt text and good evidence

`fetch_images.py` wrote `alt` from the Commons description, truncated to 160
characters. That is not alt text; it is whatever the uploader happened to say.
Of 190 camera images, **fifteen were in the first person** — `My photo of my
camera taken by me free image`, `Bought by my mother in c1980 - her favorite
camera` — nineteen ran past 140 characters into serial numbers and advice about
buying on eBay, and several were in Danish, German or Hebrew on an
English-language site. A reader who cannot see the photograph was handed a
stranger's reminiscence.

**Thirty-seven were replaced, not all 190.** The rest describe the photograph
well enough to do the job, and the film captions written by hand here — *A 35 mm
cassette of ADOX CHS 100 II, leader out, orange label with the ADOX
double-circle mark* — are better alt text than any template. A first draft of
this change overwrote all 382 images in the corpus with a uniform sentence,
which would have thrown those away to fix a different problem.

The old text is kept as `caption`, and that is the part worth recording,
because **it is the best evidence in the corpus.** Reading it found nine
photographs of the wrong camera:

*Three belong to records that already exist here.* The `Fuji GX680` image is a
body plated `GX680 III`; the `Leica M6` image is captioned `Leica M6 TTL front`;
the `Olympus OM-4` image is a champagne top plate reading `OM-4 T`, which is the
name that body was sold under in the United States and `Olympus OM-4ti`
everywhere else. All three were moved to the record they depict.

The third was nearly lost. The first pass deleted it with the others, because
the search for a home was run against record titles and `OM-4T` is not a string
in this corpus — `OM-4ti` is. **A camera sold under two names in two markets has
two names**, and looking for only one of them is how a photograph gets thrown
away next to the record it belonged on.

That deletion pass was too quick, and five of the six went back. **Deleting a
photograph is a claim too** — that nothing in the corpus is what it shows — and
it needs the same evidence as keeping one.

*Four are the record's own family.* `Nikon F90` and `Leica III` had their
article's **own lead image** removed: `Nikon F90X` redirects to `Nikon F90`, and
that article's infobox names `Nikon F90x.jpg`; the `Leica III` article names
`Leica IIIf 50mm f1.5.jpg`. Deleting those substituted a reading of the caption
for what the source itself says the camera looks like. `Minolta 16` and `Konica
Autoreflex` are family records whose sub-models — the 16 II, the Autoreflex TC —
have no article and so can never be records here. All four are back, with the
caption naming which member is in the frame.

*One was a camera missing from the corpus.* `Canon EOS-1V` has its own article
and is a 35 mm SLR, so the photograph was right and the record was absent. It
exists now, and the photograph is on it.

*One stayed out.* `Contax RTS` had a file named `Contax RTS III` whose caption
says `Contax RX` — two different cameras, neither of which has an article. The
evidence contradicts itself and nothing here can settle it, which is the only
honest reason to leave a photograph out. `Canon EOS-1` carried a body
badged `EOS-1 V`. `Contax RTS` carried what its own caption calls a Contax RX —
a moulded grip and an AE switch, where the 1975 RTS is flat-topped and has
neither. Then `Leica III` holding a IIIf, `Minolta 16` a 16 II, `Nikon F90` an
F90x, `Konica Autoreflex` an Autoreflex TC. Titles, aliases and paths were all
searched for each.

**The cause is not the one that produced the six wrong lenses.** Those came from
matching a name against a pool of candidate files. These came from an article's
lead image, and the article is about a *family* — so the picture is whichever
member somebody photographed. Both are the same shape of error and neither rule
would have caught the other.

Two were left alone. `Nikon F80` says only `Nikon F80`, and `Minolta 35` says
`second version`, which is a version of the right camera rather than a different
one. Removing a photograph on a caption's say-so is the same trust the six wrong
lenses were given, pointed the other way.

## The evidence the importers threw away, fetched back

Three importers wrote images into this corpus and all three discarded the
source's own description of the file. The camera one pasted it into `alt`,
where it was bad alt text; the lens and film ones dropped it entirely. So the
field that found nine photographs of the wrong camera did not exist for 318 of
the 357 images here.

**316 descriptions were fetched from Commons and written as `caption`.** Two
files have none of their own. Nothing was invented: this is the source's text,
capped at 400 characters, on the file each record already cites.

**The audit it enables found nothing new**, and that is the result worth
recording rather than the ones that would have been more interesting. Three
tests over the new captions:

*Does the description name a model the record does not?* Twelve matched and all
twelve are noise or known — `135` and `20` are formats on a film box, `35` is a
frame size, `AI` is a Nikon lens generation that is still F-mount and still
film-era, and the Konica Autoreflex TC and Minolta 16 II were already settled.

*Does it name a digital-only mount or image circle?* One, and it is a warning
rather than a finding.

*Is a lens photograph actually of a camera?* None.

So the lens importer's own guards worked. The one class that escaped them —
a mount marker that does not look like a mount name — was caught by reading
filenames, and the descriptions would not have added to it.

**The guard reads the filename and must keep doing so.** `Yashica Electro 35`
carries the caption `Yashica, electro, 35, rangefinder, 1964, yashinon, dx`: a
1964 rangefinder whose lens is a Yashinon DX. Extending the digital-generation
test to captions would refuse it. A caption is prose and these markers are two
letters; a filename is a name somebody chose for one file, which is a far
narrower thing to read.

## What is still unsettled, and visible

- `content/mount/pentax-kf/` — one spelling, one body, and nothing establishes
  whether the source means a distinct mount or a spelling of the K. Kept apart
  rather than silently folded into its neighbour.
- `content/mount/contax-rf/` — the source says only `Contax bayonet`, which
  names the rangefinder mount and the SLR mount equally well.
- Five camera titles say `Fuji` where the shelf says `Fujifilm` — `Fuji GS645`,
  and four GX680 bodies. Wikipedia titles them that way and the company has used
  both names. That is a question about the brand's spelling, not about name
  ordering, and folding it into the maker-first rule would answer the wrong one.
- `Leitz Minolta CL` sits on the Minolta shelf and begins with Leitz. Both made
  it, which is the whole point of the camera, so neither prefixing it nor moving
  it is obviously right.
- The 37 Hasselblad bodies that cite a section of one article get no format,
  and 36 of them are 120. A ruling could name them; what stopped it is that the
  37th is the XPan, which is 35 mm, and a rule that has to list its own
  exception is a list rather than a rule.
- **196 Olympus cameras cite one list article that names no format they could
  take.** Six of its 211 description cells state one. Its 19 series headings do
  — the OM, PEN, Trip and XA series are all 135, the Six and Flex series are
  120, the Newpic series is APS — but that is nineteen assertions of outside
  knowledge, not a fact read from the source, and it should be labelled as one
  if it is ever made.
- `List of Olympus products` names exactly one format, `135`, so nothing stops
  a future format category on it from reaching all 196 records including the
  120 and APS ones. Nothing in the tooling would notice.
- **Every lens carries a mount and only 25% of cameras do**, so six mounts hold
  glass that fits nothing here: `hasselblad-v` with 67 lenses and no body,
  `fuji-gx680` with 17, `leica-s` with 16, and the three added above. All 37
  Hasselblad bodies are among the cameras with no mount. The lens tables name
  the cameras they are for in their own headings, so this is readable rather
  than guessable.
- **Mir lenses are filed two ways, because the source files them two ways.**
  `Mir-20K` came from a section headed `Mir` and `Mir-47K` from one headed
  `VOMZ`, the plant that built it, so they now sit on different shelves. The
  same is true of `Volna`, which arrived under `LOMO`. Nothing in the source
  says which Soviet plant sold which line under its own name, and inventing a
  plant shelf for lenses that were bought as `Mir` would answer a question
  nobody asked. Eight records: five Laowa under Venus Optics, two Volna under
  LOMO, one Mir under VOMZ.

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

**Two names in one cell are two terms, never a combined one.** The sources
use three separators to write one process under several names — `CN-16 / C-41`
is Fujifilm's and the standard it matches, `Agfacolor, C-22` uses a comma, and
`E-6 (C-41)` uses brackets. Each is two processes, each gets its own term in the
same taxonomy, and no term ever stands for both. Doing this moved C-41 from 200
records to 317 and B&W to 380, which is the whole point: a combined term is a
page nobody browses to, holding films that are missing from the pages they
belong on.

The slash is the one that breaks the site rather than only the data, because a
term slugs into a URL: `cn-16-/-c-41` is a page Hugo builds two directories
deep. The other two just fragment the taxonomy quietly. The validator refuses
all of them in a `process` or a `formats` entry.

**A fragment can lose its family in the split.** `ORWO 5160 / 5165` is two ORWO
processes, and taking the parts literally leaves a term called `5165` sitting on
its own among the ORWO ones. A bare number inherits the prefix of the part
before it; a named one — `AP 41 / ORWO 9165` — does not.

**An exposure count is not a format.** 453 records said `135` and 207 said
`135-36`, so asking for 35 mm film found two thirds of it. A 36-exposure roll
and a 24-exposure roll are the same film in the same cartridge; `135-*`
collapses to `135`, which now gathers 785. The five cells that mechanical rules
mangled — `17/30.5m` became `17` — are ruled by hand in the tool rather than by
a regex general enough to break something else.

**A bulk length is not a format either, and that took a second pass to see.**
The ruling above fixed `17/30.5m` becoming `17` and left `17m` and `30.5m`
standing as terms, which treated the problem as a parsing bug when it was a
category error. `/formats/100-ft/`, `/formats/17m/`, `/formats/30.5m/` and
`/formats/50m/` were four term pages, and the first and third are one length
written in two units. The field's own rule settles it: a format is the fact a
body and a stock share, the thing that says a camera can take a film, and the
answer for a 100-foot roll of Tri-X is `135` — the same camera, the same
cartridge width, a different amount of film in the box.

22 records lost a term. Two of them, FOTON's two microfilms, lose `formats`
altogether: their Formats cell was `17m` and `17m, 30.5m, 50m` and nothing else,
so the column never said what the format was. An absent optional field is the
honest version of that. The article's description column calls one of them a
35 mm film, and mining the description column is a separate ruling nobody has
made.

`validate.py` refuses it now, so the corpus cannot drift back if the reader
changes. **The pattern is metres and feet, never `mm`:** `16mm` and `35mm` are
cine gauges, a gauge is a width, and a width is exactly what decides whether a
camera can take the film. They are the two values in this column that most look
like the thing being refused, and `\d+\s*mm?` would have taken both.

**A measurement is not a name.** The instant films recorded their frame instead
of their format: Instax Mini arrived as `46 mm x 62 mm`, Instax Square as
`62 mm x 62 mm`, Instax Wide as `99 mm x 62 mm`, Spectra as `103x 101mm`. The
film lists carry the measurement and
[List of photographic film formats](https://en.wikipedia.org/wiki/List_of_photographic_film_formats)
carries the designation, and for three of them the measurement is the join —
Instax Mini's row gives its image size as 46 × 62 mm exactly.

**One cell named three formats,** which is why this ruling is keyed by record
and not by cell. `polaroid/600-film`, `polaroid/sx-70-film` and
`polaroid/i-type-film` all read `107x 88mm`, and the format list keeps them
apart: `SX-70, Type 600` is one row and `I-Type`, from Impossible in 2016, is
another. An i-Type pack carries no battery, so it will not run an SX-70 or a 600
camera — which is precisely the question this field exists to answer, and the
answer differs.

**Two of them were left as measurements-turned-inches on purpose,** and it is
the same test seen from the other side. `polaroid/8x10-film` becomes `8x10` and
the two Fujifilm FP-100 films keep `4x5`, because Polaroid 8×10 goes in an 8×10
back and Fujifilm's 4×5 peel-apart goes in a 4×5 back, beside the sheet film
already filed under those terms. `4x5` looked at first like one term doing
double duty for sheet film and pack film; it is not, because both go in the same
camera. The source agrees with the narrower reading too — its cell reads
`325x 215mm (8x10")`, and the parenthetical is the name.

So `4x5`, `5x7`, `8x10` and `3.25x4.25` stay. For those the dimension really is
the name, they are inches rather than millimetres, and `validate.py` refuses a
measurement only when it is two numbers ending in `mm` — which leaves `16mm` and
`35mm` alone as well.

**A format term page is a format's record.** `/formats/120/` listed 462 films
and said nothing about 120 — not when it arrived, not who made it, not how big
the frame is. `content/mount/canon-ef/_index.md` had already answered the shape
question: a taxonomy term can have a page of its own, and then the term page is
the record. So every format the corpus names now has
`content/formats/<slug>/_index.md`, read out of
[List of photographic film formats](https://en.wikipedia.org/wiki/List_of_photographic_film_formats)
by `film_formats.py` in the app repository.

**A page is written even for the terms the article never mentions,** and that is
most of what fixes `/formats/`. Hugo title-cases a taxonomy term that has no
page: `sheet film` rendered as `Sheet Film`, and `46 mm x 62 mm` as
`46 Mm X 62 Mm`. Twelve terms — the sheet sizes, the cine gauges, the two
single-use-camera entries — get a title and nothing else, and the title alone is
the fix.

**`carrier`, because Hugo owns `type` and the corpus already spent `types`.**
The article's column is `Type` and its values are `roll film`, `cartridge`,
`film pack`. The singular picks a Hugo layout and the plural is a film's
print-or-slide, so the third name says what the column means.

**`discontinued` is a year on a format and a boolean on a record,** and that is
not a collision to tidy away. A record answers whether the film is still made; a
format answers when it stopped. A format still in production carries no key at
all, because the article writes "still made" four ways — `Present`, a hyphen, an
em dash, an empty cell — and a page reading `discontinued = "–"` is worse than
one that omits the field. `validate.py` refuses a boolean here.

**Millimetres, not inches.** The article gives image size in both columns and
the inches one is `{{frac}}` templates, which the wikitext parser drops — the
cell arrives as `× in`. 26 of 26 roll formats have millimetres and 14 have
inches, so only the millimetre column is read, and a cell with no digit left in
it is refused rather than published as half a measurement.

**Two rows naming one designation is refused.** `110` is an 1898 roll film and a
1972 cartridge, and the article says in as many words: "No relation to the later
110 cartridge format." Same for `126`. Their term pages carry a title and
nothing else rather than one row's facts chosen quietly. Every one of the 77
records under those two terms is the cartridge — checked, not assumed — so
nothing in the corpus is currently mis-filed; the term is ambiguous as a *name*,
and that is what stops it having a page.

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

## The Mounts link 404'd for two days on every page

The masthead pointed at `/mount/` while the pages were at `/library/mount/`.
The three links beside it were built with `(site.GetPage "/camera").RelPermalink`
and were right; the fourth used `{{ "/mount/" | relURL }}`, and **`relURL` does
not prepend the `baseURL` path.** It looks like the function for exactly this
and it is not, which is why one line out of four was wrong and read fine.

Two things follow, and the second matters more.

**Ask Hugo for a URL rather than constructing one.** `url_prefix()` in
`content.py` already says this for the Python side — *"Hugo is the authority on
what a URL is"* — and the templates had an exception nobody had noticed. There
is now no hand-built internal link in `layouts/`.

**Nothing checked links, which is why it lived.** `tools/check_stubs.py` walked
every built page to reconcile it against the manifest and never looked at what
those pages linked to. It does now: every internal href ending in `/` has to be
a page that was built. Putting the old line back turns the check red, on 500-odd
pages at once.

That check immediately found a second thing. **Hugo leaves behind output it no
longer generates**, and `check_stubs.py` reads `public/` as though it were the
build — so renamed taxonomy terms were still sitting there, the page count was
19 too high, and the link check reported links from pages that no longer exist.
`--cleanDestinationDir` is the flag that sounds like it fixes this and does not:
a page planted in `public/` survives a build carrying it. `check.sh` removes the
directory instead.

CI never saw any of it, because CI checks out fresh. That is exactly what makes
it worth fixing: the wrong answer only ever appeared on the machine where
someone was deciding whether their change was done.


## A name that does not begin with its maker, and the three reasons it might not

The maker-first ruling landed for `Girl Scout Kodak` and `Soldier's Kodak` and
stopped there. Nineteen camera titles did not begin with their brand, and
looking at all nineteen at once showed they were four problems rather than one.

**Two were the same camera twice.** `Nikkor F` and `Nikon F` were separate
records, and `Nikkor F` is a *redirect* to `Nikon F` on Wikipedia. `Kodak Vest
Pocket` and `Vest Pocket Kodak` were likewise one camera under two names, and
every one of the five Vest Pocket sources — including Model B, Series III and
Autographic — resolves to the single article `Vest Pocket Kodak`. The models are
real and distinct, described there as first and second generation; the two bare
records were not. Both merged into the record that had something to show, each
keeping the other's address as an alias.

**Checking the source article resolves this, and checking the title does not.**
A source URL that is a redirect is invisible from the record, from the diff, and
from the rendered page. Two of 573 cameras were duplicates and nothing had
looked.

**Nine had the maker inside the official name** — `Vest Pocket Kodak Model B`,
`Semi Olympus`. These follow the precedent already recorded for `Soldier's
Kodak`: keep the official name whole and put the maker in front of it, giving
`Kodak Vest Pocket Kodak Model B`. It reads oddly and it is right, because both
words are doing work — the first says who sold it and the rest is what the thing
was called.

**Four had no maker at all** — `Tenax I`, `Tenax II`, `Spice Cam`, `Instax Mini
11` — and those simply take the prefix.

Every slug is unchanged, because the validator already allows a slug to drop a
brand prefix its title repeats. No URL moved and no alias was needed for the
renames; the only new aliases are the two merges.

## A format is what joins a body to a stock

Films recorded the format they were sold in and cameras did not, so the two
halves of the library did not meet: someone holding a 120 body had no way to ask
what 120 film exists. Cameras now carry the **same `formats` field with the same
vocabulary**, which is the same reason `mount` is not lens-only — a fact shared
by two kinds belongs to both or it connects nothing.

**There is no format field on a camera to read.** Films had a Formats column in
a table; the camera sources have nothing of the kind. What there is: the
categories a person put the article in, which use the same numbers the film
tables do, and the infobox `type`. Between them, 213 of 571 — 37%, or 63% of the
cameras that have an article of their own.

Three refusals, and each is a wrong answer avoided rather than a gap left open.

**The format has to be the first thing `type` says.** A rule matching one
anywhere in that field also matches the Polaroid Impulse, whose `type` reads
`3-element 116mm f/9.4 plastic lens`. **116 is a real film format**, so the wrong
answer would look exactly like a right one and nothing downstream could tell.

**A source naming a section of a shared article is read only where the article
names one format**, because a category describes an article. 37 Hasselblad
bodies cite `Hasselblad#V_System` and its neighbours, and that article's
`120 film cameras` reached the XPan, which is a 35 mm camera. That article names
120, 220 and 35 mm, so none of the 37 is read. The rule that first shipped here
refused every fragment outright; what replaced it is below.

**Instant cameras get nothing.** That was because the films recorded their
format as physical dimensions — Polaroid 600 film read `107x 88mm` — so an
`instant` term would have joined nothing to anything. The dimensions are gone
now: the record reads `Type 600`, and the reason has to be restated rather than
left standing. It is still nothing, because the camera sources say `instant`
and nothing finer, and `instant` is not a format by the test above — an Instax
Wide pack and a Polaroid 600 pack do not go in the same camera.

**Mount is deliberately not used to infer a format.** A Canon FD body takes
35 mm film and every photographer knows it, and no source here says so. That is
the inference that is right until the day it files a Hasselblad V mount as
35 mm.

Terms are links now, on every record that has one. Printing `135` as text on the
page that has it is a dead end when a page gathering every 135 camera and every
135 film is one click away, and the taxonomies existed for two releases without
anything linking into them from a record.

## The guard was on the front door and the fact came in the back

Refusing a source with a `#` in it was the right idea checked in the wrong
place. **A Wikipedia redirect can carry a fragment the source URL does not
show.** `Kodak_Instamatic_Reflex` has no `#` in it; it resolves to
`Kodak Retina Reflex#Instamatic Reflex`, whose infobox says `35mm SLR camera`.
So `Kodak Instamatic Reflex` shipped as `135`, and the Instamatic Reflex takes
126 — which that same article says in as many words, four paragraphs down.

**56 cameras got their format through that door**, while 37 Hasselblads were
turned away at the front for exactly the risk it let through.

What replaced the URL test is a test on the article: **a record that reaches an
article through a fragment is read only when the article names a single film
format.** Two formats in one article and nothing says which one is this
record's; one format and there is nothing to be wrong about.

Three alternatives were measured and rejected.

*Refusing every fragment, now including redirects.* It removes the one false
record by removing 55 others, 46 of which reach an article that names exactly
one format.

*Reading the section the fragment points at, rather than the article.* This is
the obvious answer and it does not work: **3 of 87 sections state a format at
all.** A section says what is different about a variant, and the format is what
is the same.

*Testing only the article's lead.* `Kodak Retina Reflex` leads with `35mm SLR
camera` and names 126 further down. A lead-only test misses the single case this
exists for.

The cost is **10 records, 9 of them correct** — the Retina Reflex family, three
Fuji GX680 bodies and two Pentax 645 bodies, whose articles mention a second
format in passing. That is a 9-to-1 trade, and worth stating plainly rather than
rounding off: what is bought is not one deletion but 46 claims that were right
by luck becoming 46 claims that are right by rule.

The test is necessary and not sufficient, and one case shows the gap.
`List of Olympus products` is the source for 196 cameras and names only `135`,
so it passes — while its table lists the Newpic series, which is APS, and the
Six and Flex series, which are 120, describing both without ever naming a
format. It is harmless only because that article has no format category and no
infobox, so there is nothing to read from it either way.

## The bare spelling that two mounts answered to

The `Canon Canonflex` was filed under `leica-r`. Its infobox says
`lens_mount = [[R mount]]`, and `content/mount/leica-r/` claimed the spelling
`R mount` alongside `Leica R` and `Leica R mount`. So the join was a *correct*
reading of a wrong claim, which is why nothing downstream complained: the record
validated, rendered, and sat a 1959 Canon breech-lock body on a shelf of Leica
glass that will not fit it by any adapter.

Three things about it are worth keeping.

**`[[R mount]]` is a redlink.** It reaches no article on Wikipedia. Canon's is
`Canon R lens mount` and Leica's is written `Leica R` everywhere. The one string
that would settle it is the one string nobody wrote.

**`Wikipedia:Lens mount` could not have caught this.** Its list of 118 mounts
does not include the Canon R at all. The audit that found it was not against the
authority; it was the corpus checked against itself — a body whose brand is not
its mount's — and the authority's silence is the reason that check had to exist.

**The fix is a withdrawal, not a reassignment.** `R mount` is now claimed by
neither record. Giving it to `canon-r` would have been the same bet with the
other side of the coin up, and `validate.py` already refuses two mounts one
spelling — that rule is what surfaced the collision the moment `canon-r` was
written. An importer that meets `R mount` now gets no answer, which is the
answer: it has to go and look.

`test_a_body_wears_another_maker_s_mount_only_on_the_record` names the six real
cases — Leitz Minolta CL, Minolta CLE, three Canon LTM rangefinders, Ricoh
XR-1 — and fails on a seventh. It is deliberately bodies-only: 423 lenses here
carry another maker's mount, because that is what third-party glass is.

## A label is not a link target

`Pentax ME Super` carried `mount = ["pentax-kf"]`. Its infobox says

    | lens_mount = [[Pentax K mount|Pentax K-F mount]]

which is a link to the **K** mount wearing the **K-F**'s label. An importer
reading what the page displays gets `Pentax K-F mount`; one reading where the
page points gets `Pentax K mount`. Only the second is a claim the encyclopaedia
is making.

`Pentax K-mount` settles it three separate times: "Bodies equipped with the
original K-mount include the K series, the M series *except the ME F*"; "Only
one camera and one lens ever used this mount, the Pentax ME F and the SMC
Pentax-AF 35-70/2.8"; and its own body table lists the ME Super under *K*. The
`Pentax ME Super` article's prose agrees with all three — "the lenses are
interchangeable with the K bayonet mount" — and it is categorised under
`Pentax K-mount cameras`.

So the infobox is the only thing on the page that says K-F, and it says it in
the half of a piped link that carries no claim.

This also closed the open question `content/mount/pentax-kf/` was carrying.
That record used to say nothing here established whether the source meant a
distinct mount or a spelling of the K. It is distinct: the K plus five
electrical contacts, Pentax's first autofocus attempt, one body and one lens.
Both facts arrived together — what the mount is, and that only the ME F has it.

## The authority is coarser in one place and finer in another

`Wikipedia:Lens mount` lists 118 mounts with flange focal distance, throat
diameter, thread pitch, type and frame size. It is the best single reference
for this and it cannot be taken as the only one.

**It is coarser than this corpus on Hasselblad.** One row: `Hasselblad`,
74.9 mm, 6×6, bayonet. Four records here — `hasselblad-1600f`, `-v`, `-h`,
`-xpan`. The row can only be describing the V. Copying it across all four would
print three false facts, and each would look like the others.

**It is finer than this corpus on Mamiya.** Two rows, `Mamiya RB67` at 112 mm
and `Mamiya RZ67` at 105 mm. Both bodies here sit on one record,
`mamiya-breech-lock`, because both articles use the identical phrase "Custom
Mamiya breech-lock bayonet mount" — the corpus is faithful to its source and
its source joined them.

**And it contradicts Wikipedia.** The list gives the RB67 112 mm and calls the
mount a bayonet. `Mamiya RB67` gives "The flange distance is 110 mm" and calls
it a breech-lock. Two pages of one encyclopaedia, disagreeing on both the number
and the kind of thing.

The rule that follows: **a fact from the list may be written only where nothing
here already says otherwise, and a disagreement is recorded rather than
resolved.** An importer that overwrites is an importer that turns the finest
thing this corpus has — a body-level reading of the body's own article — into
the coarsest.

## What the list is not, by its own column

39% of the 118 rows are not film photography: 14 digital, 14 cinematography,
5 video, 4 microscope, 2 machine vision, plus mixed. The discriminator is in
the table — a `Primary use` column reading `Photography`, `Photography
(Digital)`, `Cinematography` — so this one does not need inferring, which is
unusual here and worth saying. `Photography` with no parenthesis is the film
set: 72 rows.

Of those 72, this corpus holds 25. The other 47 are not a backlog. A mount
exists here because something in the corpus carries it, and importing 47 empty
ones would be importing a taxonomy nothing uses. What the list *is* good for is
the reverse lookup: **423 of 572 cameras here name no mount**, and among them
are the Pentax 6×7 and Auto 110, the Mamiya 6, 7 and 645, the Konica F and the
Contax RTS — all of them bodies whose mount this list names and whose own
articles were read from lists that had no infobox to read.

## Two sources for one number, and neither is the authority

A mount now carries what it measures — `type`, `flange`, `throat`, `pitch`,
`tabs` — and a `[measured]` table saying, per figure, which page it came from
and how directly. 27 of the 32 mounts have figures. Five have no source that
names one: `fuji-gx680`, `hasselblad-1600f`, `hasselblad-h`, `mamiya-press`,
`tenax-bayonet`.

The provenance is not decoration. Two Wikipedia pages state these numbers and
they disagree, and the disagreements are not rounding:

| mount | the summary table | the mount's own page | kept |
| --- | --- | --- | --- |
| Mamiya RB67 | 112 mm, bayonet | 110 mm, breech-lock | 110 mm, breech-lock |
| M42 | 45.46 mm | 45.5 mm | 45.5 mm |
| Rollei QBM | 44.46 mm | 44.5 mm | 44.5 mm |
| Minolta SR | Bayonet (54°) | Bayonet | Bayonet |
| Nikon S | Bayonet, throat 34 mm | internal *and* external bayonet, 36.5 and 49 mm | the pair, and no throat |

The rule Casey set is the one implemented: **trust the page about the specific
thing, and record the disagreement rather than resolve it.** Seven conflicts
are reported by `mount_facts.py` on every run and none is resolved by it.

Three details of that turned out to matter more than the rule.

**A number the better source cannot state is not a licence to use a worse
one.** `Nikon S-mount` gives its throat as "36.5 mm (internal bayonet) and
49 mm (external bayonet)". That is two numbers, so it is not a throat, and the
summary table's 34 mm is a third. Filling the field in tier order takes 34
because it is the only float in sight. The record gets no throat.

**Which infobox field holds the throat is not consistent.** The Canon EF's
`external_diameter` is 65 mm and its `inner_diameter` 54 — the list says 54.
The Nikon F and Leica M put 44 mm, which their own prose calls a throat, in
`external_diameter` and leave the inner blank. So neither field *is* the
throat, and choosing by field name is a guess. What is not a guess is a figure
both sources give: where the table's throat equals some infobox diameter, that
is two independent statements of one measurement. Where they name different
numbers, the record gets none.

**A pitch keeps the unit it was written in.** That column holds `26 TPI`,
`1 mm` and `0.75mm`. 26 threads per inch is 0.977 mm, so stored as floats under
one field name the Leica screw mount's thread would read as the coarsest in the
corpus instead of nearly the finest. It is a string.

And the `derived` tier exists for three records that inherit rather than state.
`pentax-kf` and `ricoh-rk` are the Pentax K plus five contacts and one pin;
`canon-r` shares the FD's flange because `Canon R lens mount` says the lugs,
flange focal distance and breech-lock ring are mutually compatible. No page
states 45.46 mm of the K-F. The mount page says so in words — "which describes
the mount this one is a variant of and not this one" — and
`test_a_derived_figure_equals_the_mount_it_was_derived_from` fails if a child
stops matching its parent, which is what a corrected parent nobody propagated
looks like.

## The prose said 20 mm and meant a different mount

The hand-transcribed figures in `PROSE` are hand-transcribed because the
obvious alternative fails on the second article it meets.

`Canon FD lens mount` says "The 42mm flange focal distance of the FD mount is
shorter than that of most other lens mounts." It also says, of a digital body
three paragraphs later, "It has a flange focal distance of only 20mm and a 2×
crop factor." A regex taking the number nearest the word takes 20.

`M42 lens mount` is worse: it names the flange distance of six other mounts
before it is done with its own, because an article about a mount is mostly
sentences about what else that number lets you adapt. And `Pentax K-mount`
leaves its infobox `flange` empty, so its only statement of 45.46 mm is inside
a sentence about mounting M42 lenses.

So each entry carries the sentence it came from, in the file, next to the
number. It is 11 entries. A regex would have been shorter and would have
written 20 mm as the Canon FD's flange, which is the kind of wrong that
validates, renders, and sits there.

## The mount split that the flange distances justified

`mamiya-breech-lock` held the RB67 and the RZ67 together, and faithfully: both
camera articles use the identical phrase "Custom Mamiya breech-lock bayonet
mount". The summary table splits them, at 112 mm and 105 mm.

Following the table alone would have been following the source that is wrong
about the RB67 — its own page says 110 mm. But the two pages agree on the thing
that matters: **110 and 105 are different numbers**, stated on each body's own
article, so the shared phrase names a family and not a mount. Split into
`mamiya-rb67` and `mamiya-rz67`, with the retired slug aliased to the RB
because the RB came first.

The evidence and the conclusion are the same fact here, which is unusual and
worth a guard: `test_the_two_mamiya_67_mounts_are_what_the_split_claimed`
asserts the two flange distances differ and are 110 and 105. If they ever
agree, the split has no basis left.

## The designation was reused, and one of the two is what people mean

`110` is two rows of the article and `126` is two more: an 1898 roll film and a
1972 cartridge, a 1906 roll film and a 1963 one. The article is explicit that
the pairs are unrelated — "No relation to the later 110 cartridge format" — so
there is no averaging them, and the first reader refused both terms and left
them with a title and no facts.

A refusal is the right default and was the wrong answer here. **Every record
that sends somebody to one of those pages means the cartridge**: 45 records name
`110` and 32 name `126`, and reading every title says so — the Pentax Auto 110,
the Minolta 110 Zoom SLR, Lomography's current stocks, Kodacolor VR. A page
describing the roll film would have been wrong about all 77.

So the later row is taken, and the earlier one becomes a sentence at the end of
the note: "Kodak used the designation 110 earlier, for an unrelated film made
from 1898 to 1929." Choosing is the ruling; choosing silently is what is still
refused. That sentence is built from the displaced row rather than written out,
so it stays true if the article is corrected — and the displaced row's own
comment is not carried over, because "No relation to the later 110 cartridge
format" printed on the cartridge's page points at itself.

**The year decides, and nothing else.** Not which one survived: 126 ended in
2008 and is still the 126 anybody means. Not which row has more fields: the
1898 roll film has a `discontinued` year the cartridge lacks, and would win on
completeness. Where a year cannot decide — two rows of one year, or a row that
gives none — the refusal stands, because an undated row is not an early one.

### The spool names went with the number, not the film

Writing the page is what exposed this. The cross-reference table that gives
`120` its other makers' names — Agfa B2-6, Ansco 4A — is a table of **spools**;
its own last column is `Spool length (in)`. Its `126` row is the 1906 roll film,
4.898 inches of it, and it handed `Ansco 19A` and `Vulcan 252` to an Instamatic
cartridge that has no spool at all.

All 23 numbers in that table are `roll film` rows and `126` is the only one any
other format shares, so the fix costs nothing measurable: a spool's name is
offered only to a row carried on a spool. It was invisible while `126` was
refused, which is the shape of a bug that a fix uncovers rather than causes.

## A single-use camera is a camera

`SUC-27` and `SUC-39` had term pages under `/library/formats/`, and the source
that put them there defines the abbreviation itself, in the key above the film
tables: "SUC-27/39 – Single use camera with 27/39 exposures."

So the cell names a camera and an exposure count, and this corpus had already
ruled that neither is a format — `135-36` collapses to `135` because the count
is packaging, and `100 ft` went because no length says whether a camera can
take the film. A single-use camera fails that test hardest of all: **nobody
loads one.** There is no body here a `SUC-27` term could join a stock to, which
is the only job the field has.

Four records carried it. Three keep their real formats and lose only the term.

**The fourth needed a second look, and the first answer here was wrong.**
`kodak/ultramax-800` had `formats = ["SUC-27", "SUC-39"]` and nothing else,
because its row says that since 2008 it is sold only inside those cameras.
Removing the term left it naming no format at all, and that was recorded as the
true answer with a note saying the film inside is 35 mm but no source says so.

That reads the row as if it began in 2008. It does not: **"since 2008" is a
statement that before 2008 it was sold some other way**, and the corpus
documents what a thing was as readily as what it is. Two neighbouring rows say
which way. `List of discontinued photographic films` carries `Max Zoom 800`,
c2002–2007, format `135`, whose own Replaced-by column names UltraMax 800; and
`UltraMax 400`, the sibling launched the same year off the same Gold line, is
`135`. The film had a year on the shelf as a roll you could buy, and the record
says `135` again.

Three sourced rows read together is not the same as inferring a format from a
mount, which is refused [above](#a-format-is-what-joins-a-body-to-a-stock).
The difference is that every step here is a sentence in a source; there, the
sentence does not exist and the format is guessed from a lens fitting. The
ruling lives in `film_facts.FORMATS_ELSEWHERE`, keyed by record, with the three
rows named beside it — so a regeneration reproduces it rather than dropping it
back to nothing.

The note has a side effect worth naming: it earns UltraMax 800 a page of its
own, where before it redirected to the Kodak list. A record whose most
interesting fact is the shape of its own sourcing is exactly a record worth a
page.

`validate.py` refuses the term now, so it cannot come back the way it arrived.
The pattern is the whole term and case-insensitive — the source is a table
people hand-edit, `Suc-27` is an ordinary typo, and a format that merely begins
with those three letters must survive.


## An absent mount was two different facts written the same way

572 cameras; 149 named a mount and 26 named a fixed lens, and the other 397
said nothing. That silence covered a camera whose mount nobody had looked up
and a camera that has no mount to look up, and the corpus wrote both the same
way. A reader could not separate them, a test could not assert about either,
and the number that would have measured the gap could not be computed.

Both halves are now written from one field. `{{Infobox camera}}` states the
mount in `lens_mount` on modern articles and `lens_system` on older ones, and
the same field says `fixed`, `fixed lens` or `integrated` where there is none.

**The vocabulary is the corpus, not a table in the importer.** Mount records
carry `spellings`, and `validate.py` already refuses to let two mounts answer
to one — so the library is a lookup table that is checked on every build, and
adding a spelling to a record teaches the importer without anyone editing it.

That mattered immediately. One camera infobox reads `[[R mount]]`, which is
the redlink that put the Canonflex under `leica-r` and cost two records their
claim to the spelling. Because neither mount answers to it now, the importer
gets no answer instead of a confident wrong one — and a hardcoded table would
have had to be told about that separately, afterwards, by somebody who
remembered why.

## An infobox describes its article, not the section a redirect landed in

`camera_formats.py` reads a record that reaches a section of a shared article
where the article names exactly one film format, on the grounds that there is
then nothing to be wrong about. The same rule applied to mounts would be wrong,
and the Konica Hexar says why in one line.

Nine Hexar records — Classic, Gold, Rhodium, Silver, Titanium, 72, RF, RF
Limited and the base model — redirect to one article. Its infobox reads
`lens_mount = fixed 35mm f2 lens`, which is true of the Hexar AF the article
leads with. **The Hexar RF is a Leica M-mount rangefinder.** Taking the
article's word would file an interchangeable-lens M-mount body as a fixed-lens
compact, and it would look exactly like the eight correct ones beside it.

A format can be a property of an article because an article about many cameras
is usually about many cameras taking one film. A mount cannot: it is the fact
that most often distinguishes the variants a shared article exists to hold. So
a camera reached through a section gets nothing, and 275 of the 397 are refused
on that ground alone — 196 of them from `List of Olympus products` and 37 from
`Hasselblad`.

This is the ceiling on the infobox as a source, and it is worth stating
plainly: the remaining gap is not behind the infobox. It is behind the fact
that two thirds of these cameras have never had an article of their own.

## Two mounts the corpus does not hold, and did not invent

Eleven cameras name a mount with no record here: ten point at Deckel's
`DKL-mount` — the Retina Reflex bodies and the Voigtländer Vitessa T — and one
at a `Mamiya 645 bayonet`. Both are film mounts and both would be legitimate
records under the rule that a mount exists if something carries it.

Neither was created. A mount record is a claim about geometry, and this pass
had one field of one infobox to go on, which names the mount and says nothing
about it. Writing `dkl` with a title and nothing else would have put a record
in the corpus whose only content is that a camera pointed at it — and the
five mounts that already carry no figures at least say why on their own pages.
These are recorded here instead, where they can be picked up by someone with a
source in front of them.

**One value was refused for saying two things at once.** The Vitessa's field
reads `fixed or [[DKL-mount]] (Vitessa T)`: most Vitessas have a fixed lens and
the T takes Deckel glass, in one field, describing two cameras. It is neither
answer, and a reader that took the first word would have written a fixed lens
onto a camera that has a mount.

## `sheet film` is a carrier, and it stays anyway

158 records name it — more than any format term except `135` and `120` — and its
page carried a title and nothing else, which reads as a fact nobody had got
round to sourcing. It is not. `List of photographic film formats` has no row for
`sheet film` because it is not that kind of word: it is a **carrier**, the same
kind as `roll film`, `cartridge` and `film pack` in the article's own Type
column. By the test this field exists to answer it is barely a format at all —
a 4×5 sheet does not go in an 8×10 camera, so knowing a film came in sheets
does not tell you whether your camera can take it.

The obvious alternative was to replace the term with the sizes, and **the source
will not support it**. Across the film lists, `Sheet` appears bare in almost
every row that has it and spells out `4x5", 5x7", 8x10"` in two. So the choice
was a coarse term or no term, and dropping it would lose 158 records' only
statement that the film was sold in sheets — while `4x5`, `5x7`, `8x10` and
`3.25x4.25` already exist as their own terms for the records whose sources do
say.

So the term stays and the page says which kind of word it is. **The sizes are a
separate question, deliberately left open** rather than answered by guessing per
record.

The page is a note and no fields, which the first draft got wrong twice over.
`carrier = "sheet film"` renders as "Carried as sheet film" beneath a heading
reading `sheet film`; and any fact at all opens the facts list, where the
template answers an absent `discontinued` with "Availability: Still made". That
happens to be true of sheet film, and it is not something this page went and
found out — a term page should not put its name to a sentence that arrived as a
template default.

`glass plates` is the same kind of word and has one record. It still carries a
title and nothing else, which is a smaller version of the same gap, named here
so it is a decision rather than an oversight.

## The `35mm` that meant `135`, and the two numbers that did not

Counting every format term by how many records name it is a cheap audit and it
found one wrong answer in 41. **976 records spell 35 mm film `135`. One spelled
it `35mm`** — `catlabs/x-film-100-color`, whose source cell reads
`35mm*, 120, 4x5"`. So somebody asking what 35 mm film exists found 976 of the
977, and the odd one out had a term page of its own to itself.

The record says `135` now and the `35mm` term page is gone.

**This first shipped as a ruling on the one record, on the grounds that `35mm`
was also a cine gauge and 35 mm movie film does not go in a still camera. That
is false**, and the sources say so plainly. `135 film` opens "more popularly
referred to as 35 mm film or 35 mm"; it gives 135 "the same dimensions and
perforation pitch as 35 mm movie print film"; it captions the Leica I as "the
first successful camera worldwide for 35 cine film". And this corpus's own film
list says CineStill "converts Eastman Kodak motion picture stock into 135 and
120 still camera formats" — and three of the five CineStill records here carry
`135`, which *is* motion picture stock in a still camera.

So 35 mm and 135 are one format under two names. What separates a cine roll from
a cassette is how much film is on it and what it is wound on, and a length has
already been ruled not to be a format
[above](#a-format-is-what-joins-a-body-to-a-stock) — the format of a 100-foot
roll of Tri-X is 135. The reader maps `35mm` to `135` wherever it appears, which
is a rule rather than a ruling because the reasoning does not depend on which
record it lands on.

**`16mm` and `Double 8` are untouched, and the reason is width, not
movie-versus-still.** Neither goes in a 35 mm camera at all. Both sit on
`fpp/the-mummy-400` beside `135`, which is one film sold for two kinds of
camera — and that record is the reason to get this distinction right rather
than draw it in the wrong place.

There is a small guard as well: no record names `35mm` now, so no page exists
for it, and `validate.py` refuses a format term with no term page. A hand-edited
record spelling it that way fails in CI rather than quietly splitting the
taxonomy again.

**The asterisk is a footnote into the row's own description**, where CatLABS say
"35mm coming soon". The record notes it, because a format the source hedges on
is worth flagging even when the maker's product page — the one this record's
photograph comes from — shows the 35 mm box.

### The two numbers that looked wrong and were not

`935` on 23 records and `635` on 26 look like typos for `135` and they are
neither. Both are in the article: **Comecon designations for 35 mm film on a
daylight loading spool**, 1960s to 1990s, 24 × 36 mm, 36 exposures, cited to a
1982 Prague reference book. They turn up together on Foma, Foton, dekopan and
Agfa stocks, which is exactly the geography that should be expected. Their term
pages already carry those facts, and they are recorded here so the next audit
does not have to re-derive that they are real.

## An integrated lens is a fact; the glass is a detail that may be missing

`fixed_lens` held two things and could state only one of them. It said what the
glass is, and a camera could say its lens does not come off *only* by naming
that glass — so a body whose article states the first and not the second was
written nowhere, and its blank was identical to the blank on a camera nobody
had looked up.

That is the defect this corpus had just spent two changes fixing one level up,
appearing one level down inside the field that fixed it. `Canonet G-III QL17`
is the case in one line: its infobox reads `lens_mount = integrated`, and no
source here names its lens.

So there are two keys. **`integrated = true` is the fact that the lens does not
come off. `fixed_lens` is what that lens is, and it may be absent.** It is the
same shape as a mount and its `[measured]` block — something that can stand
alone, and detail that can go missing without taking it along.

Four rules hold the pair together, and each one exists because the alternative
is a record that reads as an answer:

- **A body claims a mount or an integrated lens, never both.** This replaces
  the older rule about a mount and a `fixed_lens`, which could not see a body
  that claimed a mount and an integrated lens whose glass went unnamed.
- **`fixed_lens` without `integrated` is refused.** Naming the glass does not
  say the glass is fixed there, and a reader asking which bodies take no
  interchangeable lens would miss every such record. The 26 records that
  carried `fixed_lens` before this were backfilled rather than grandfathered.
- **`integrated = false` is refused.** A lens that comes off is a mount, and a
  second way to write what an absent key already says is how a corpus begins
  disagreeing with itself.
- **An empty `fixed_lens` is refused.** A camera whose glass no source names
  carries `integrated` alone; an empty string would be a third spelling of
  "unknown" beside the two that already exist.

**The count that motivated this is still mostly unanswered, and deliberately.**
31 cameras now say their lens is built in, 26 of them naming it. The ~190
Olympus compacts that dominate the remaining silence have no source that
answers either question: `List of Olympus products` has no lens column and no
mount column, 156 of its 211 rows have an empty description, and of the 202
silent Olympus records only 11 have any article of their own. Wikipedia does
not hold this. Nothing here guesses it, and this paragraph exists so that the
next person to look does not have to measure it again to find that out.

## A refinement is not a disagreement, and an unreadable value is neither

`mount_facts.py --check` reported nine conflicts. One of them was a conflict.

Both comparisons behind that report were equality, and equality is the wrong
test for two of the three ways these two sources differ.

**One measurement written to two precisions.** The list gives the M42 flange as
`45.46 mm` and `M42 lens mount` gives `45.5 mm`. Those are not two claims:
45.46 rounded to the precision the article states *is* 45.5. Compared for
equality they differ by 0.04 and read as a disagreement; compared at the
coarser of the two precisions they agree exactly, which is what anybody looking
at the pair would say. The finer figure is kept and the tier follows the
value — the extra digit came from the list, and the record credits the list.
QBM is the same pair at 44.46 and 44.5.

The rounding has to be to the **coarser** of the two. Rounding to the finer
puts 45.5 and 45.46 back into conflict; rounding both to nothing would make the
Mamiya RB67's 110 and 112 the same number, which is the one case here where the
sources really do contradict each other.

**One source saying more than the other.** `Breech-lock bayonet` and `Bayonet`
are not two answers; the first is the second plus the part that distinguishes
it. The case that matters runs the other way, though, and nobody was watching
it: `Minolta SR-mount`'s infobox says `Bayonet` and **only the list says
`Bayonet (54°)`**. Preferring the better source was throwing away the one fact
that told this bayonet from every other one in the corpus.

So the more specific value wins regardless of tier. That is not a reversal of
the tier order — **the tiers rank sources for whether to believe them, and
these two agree; one of them just says more.** The test is word containment
rather than string length, so `Screw` and `Bayonet` share nothing and stay a
disagreement.

**A source that cannot be read has not disagreed.** `konica-km`'s flange column
reads `28 mm (27.80 mm?)`, question mark and all, and `Nikon S-mount` states
its throat twice because it has two bayonets. Those ask for a better source,
not for a decision, and they are listed apart now. So is a third kind — a
record that already answers differently, which asks somebody to check which is
right.

What survives is one conflict, and it is the one that always mattered: 110 mm
on the camera's own page against 112 mm in the list.

**A page named one source where two had been read.** The provenance line said
"Measured from *QBM*" on a record whose throat, and now flange, came from the
list — a different page. Twelve mounts mix tiers that way, and a reader sent to
check a figure would not have found it. The line names both pages now, and says
that the second does not always agree with the first.

One existing test had been asserting the old behaviour and passing for the
wrong reason: it used the QBM's `44.5` against the list's `44.46` as its
example of a disagreement worth keeping. It was pinning a false alarm.

## Two mounts the cameras named, and what naming them cost

Eleven camera records pointed at a mount this corpus did not hold: ten at
Deckel's DKL and one at the Mamiya 645 bayonet. Both are film mounts, both are
carried by something here, and the rule is that a mount exists if something
carries it. They were left out of the earlier pass because a mount record is a
claim about geometry and that pass had one field of one infobox to go on. Both
have a source now.

**`mamiya-645` comes entirely from the list.** 63.3 mm flange, 62 mm throat,
bayonet, and the row's own `Primary use` column says photography. It is the
fourth Mamiya mount here and unrelated to the other three.

**`dkl` has no article at all.** `DKL-mount` is a redirect, and not to a mount:
it lands on `Friedrich Deckel`, the company that made Compur shutters. One
section of that page is the only source there is, and it gives the flange as
44.7 mm, shared with Exakta, and the type as a bayonet introduced in 1956.

**That section also says the mount is seven mounts.** Makers "introduced
variations in the mounting lug profiles and inclusion of an aperture control
ring to physically prevent the attachment of lenses from other DKL-mount
systems" — Retina lenses need their lugs filed to fit a Voigtländer. So the
record says out loud that it is a family: 44.7 mm is the distance every variant
shares and not a promise that a lens will mount. The corpus splits a mount when
its flange distances differ, which is what separated the Mamiya RB67 from the
RZ67. No source states a per-variant geometry for these seven, so there is
nothing to split on yet.

### The mount's own article can answer what the camera's does not

Five Kodak Retina records give their mount as `model specific: Retina
convertible or DKL-mount`, which names two and settles neither. The Deckel
section settles two of them from the other side: it names `Kodak Retina IIIS`
and `Kodak Retina Reflex S`, by those names, among the bodies the bayonet was
built for. Those two carry `dkl` and a note saying where the answer came from.
The other three Retina Reflex records are not in that sentence and keep no
mount.

Nothing was extended to the Voigtländer Bessamatic variants on the same
grounds. The article names "Voigtländer Bessamatic"; the corpus holds
Bessamatic CS, deLuxe and m, and treating a line's name as covering its
variants is the inference the Konica Hexar rule exists to refuse.

### What a missing mount had been hiding

A mount the corpus lacked was making three bad readings look like good
refusals, and creating it turned them live.

- `fixed or [[DKL-mount]] (Vitessa T)` holds exactly one link, so following
  links answers `dkl` — for the plain Vitessa, most of which have a fixed lens.
- `Konica KM-mount (the same as or similar to the [[Leica M-mount]])` is worse
  and older. The camera has the KM mount, which this corpus holds; the only
  link points at the mount it is being *compared to*. Three Konica bodies would
  have been filed under `leica-m`, and the reason nobody saw it is that all
  three were recorded by hand and the never-overwrite rule declined to touch
  them. A latent wrong answer is not a right one.
- The five Kodak records above, which say `model specific:` outright.

**A field with `or` in it has not answered**, and is reported rather than read.
