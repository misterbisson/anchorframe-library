"""Decisions a person made, kept where they can be argued with.

Nothing here is derived. Each entry is a judgement that the sources could not
settle, recorded so a re-run cannot quietly reverse it and a contributor can
disagree with it in a pull request rather than in an email.

**The distinction this file turns on: a brand is who a thing was *sold under*,
not who manufactured it.** Minolta built the CL for Leica, so `manufacturer`
is right about the CL and still wrong for an index someone reaches by typing
what is written on the front. Who made a camera and whose name is on it are
different questions, and this answers the second.
"""

# A product line is not a company. `Nikkor` is what Nikon writes on its glass;
# nobody bought a lens from a company called Nikkor. Each of these is the badge
# on the item mapped to the company that sold it, and each becomes an alternate
# brand that redirects.
LINE_BRANDS = {
    "Canonet": "Canon",
    "Fujinon": "Fujifilm",
    "Hexanon": "Konica",
    "Instax": "Fujifilm",
    "Leitz": "Leica",
    "Nikkor": "Nikon",
    "Nippon Kogaku": "Nikon",
    "Rolleicord": "Rollei",
    "Rolleiflex": "Rollei",
    "Rokkor": "Minolta",
    "Takumar": "Pentax",
    "Zuiko": "Olympus",
}

# One company, one spelling. `Fuji` and `Fujifilm` are the same firm, and the
# film sheets already say `Fujifilm`; letting both stand would split the
# namespace down the middle of one maker.
BRAND_ALIASES = {
    "Fuji": "Fujifilm",
    "FUJIFILM": "Fujifilm",
    "Carl Zeiss": "Zeiss",
    "Schneider": "Schneider Kreuznach",
}

# Names whose brand no rule reaches, each with the evidence that settled it.
# Read from the article's own text, not from a guess about the name.
BRAND_RULINGS = {
    # "manufactured by Wirgin" — and sold as an Edixa.
    "Edixa Reflex": "Edixa",
    # "manufactured by Fujifilm of Japan". The name says Fuji; the company is
    # the one the film sheets already name.
    "Fuji GS645": "Fujifilm",
    "Fuji GX680": "Fujifilm",
    "Fuji GX680II": "Fujifilm",
    "Fuji GX680III": "Fujifilm",
    "Fuji GX680IIIS": "Fujifilm",
    # Kilfitt designed it; Metz put its name on it, which is the section of the
    # `Mecaflex` article this camera comes from.
    "Metz Mecaflex": "Metz",
    # The same body was badged by three firms. Each badge is its own record.
    "Sinar Hy6": "Sinar",
    # Infobox `manufacturer = Polaroid Corporation`. A Spice Girls tie-in, sold
    # as a Polaroid.
    "Spice Cam": "Polaroid",
    # "a 24x24 mm fixed lens camera by Zeiss Ikon".
    "Tenax I": "Zeiss Ikon",
    "Tenax II": "Zeiss Ikon",
    # Kodak sold a run whose official name puts the maker last. The name is left
    # as the source writes it; the brand is Kodak wherever the word sits, which
    # is the question the *name* ruling could not answer.
    "Vest Pocket Kodak": "Kodak",
    "Vest Pocket Kodak Model B": "Kodak",
    "Vest Pocket Kodak Series III": "Kodak",
    "Vest Pocket Autographic Kodak": "Kodak",
    # Sold in Japan under a joint Leitz/Minolta badge. Wikipedia redirects the
    # name to `Leica CL` and treats them as one camera; this index keeps two
    # records, because two badges is two things a person types. Filed under the
    # firm that built and sold this one.
    "Leitz Minolta CL": "Minolta",
}

# A name that is another record's name. The source lists both; they are one
# product, so one is the address and the other redirects to it.
ALTERNATE_OF = {
    # Wikipedia redirects `Nippon Kogaku F5` to the 50th anniversary edition,
    # which this index already carries under the name Nikon used at the time.
    ("camera", "Nippon Kogaku F5"): ("camera", "Nikon F5 50th anniversary edition"),
}

# Every mount string either sheet uses, folded onto one record each.
#
# **This is the join that did not exist.** The camera sheet wrote 34 spellings
# and the lens sheet 12, and only `Canon EF`, `Canon FD` and `Pentax K` appeared
# in both — a Nikon F body said `Nikon F-mount` where its 285 lenses said
# `Nikon F`, so nothing connected a body to its glass. A mount is a record here
# for exactly that reason.
#
# `brand` is absent where a mount has no owner. M42 is the case that settles the
# URL shape: it is a thread, not a product, and inventing a maker to fill a path
# segment would be the manufactured-by mistake in a new place.
MOUNTS = {
    "nikon-f": {"name": "Nikon F", "brand": "Nikon",
                "spellings": ["Nikon F", "Nikon F-mount", "Nikon F lens mount"]},
    "nikon-s": {"name": "Nikon S", "brand": "Nikon",
                "spellings": ["Nikon 'S' bayonet mount"]},
    "leica-m": {"name": "Leica M", "brand": "Leica",
                "spellings": ["Leica M", "Leica M-mount"]},
    "leica-r": {"name": "Leica R", "brand": "Leica",
                "spellings": ["Leica R", "Leica R mount", "R mount"]},
    "leica-m39": {"name": "Leica screw mount (M39)", "brand": "Leica",
                  "spellings": ["Leica screwmount", "Leica screw mount",
                                "Leica M39 Screw Mount", "M39 lens mount"]},
    "leica-s": {"name": "Leica S", "brand": "Leica", "spellings": ["Leica S"]},
    "canon-fd": {"name": "Canon FD", "brand": "Canon",
                 "spellings": ["Canon FD", "Canon FD lens mount"]},
    "canon-fl": {"name": "Canon FL", "brand": "Canon",
                 "spellings": ["Canon FL", "Canon FL lens mount"]},
    "canon-ef": {"name": "Canon EF", "brand": "Canon", "spellings": ["Canon EF"]},
    "minolta-sr": {"name": "Minolta SR", "brand": "Minolta",
                   "spellings": ["Minolta SR mount"]},
    "minolta-a": {"name": "Minolta A", "brand": "Minolta",
                  "spellings": ["Minolta A-mount"]},
    "olympus-om": {"name": "Olympus OM", "brand": "Olympus",
                   "spellings": ["Olympus OM", "Olympus OM mount"]},
    "olympus-pen-f": {"name": "Olympus Pen F", "brand": "Olympus",
                      "spellings": ["Olympus Pen F", "Olympus Pen F mount"]},
    "pentax-k": {"name": "Pentax K", "brand": "Pentax",
                 "spellings": ["Pentax K", "Pentax K bayonet mount", "K mount"]},
    "pentax-kf": {"name": "Pentax K-F", "brand": "Pentax",
                  "spellings": ["Pentax K-F mount"],
                  "note": "Kept apart from `pentax-k` because nothing here "
                          "establishes whether the source means a distinct mount "
                          "or a spelling of the K. One spelling, one body: a "
                          "record with a question on it rather than a silent "
                          "fold into its neighbour."},
    "pentax-645": {"name": "Pentax 645", "brand": "Pentax",
                   "spellings": ["Pentax 645 A mount"]},
    "konica-ar": {"name": "Konica AR", "brand": "Konica", "spellings": ["Konica AR"]},
    "konica-km": {"name": "Konica KM", "brand": "Konica", "spellings": ["Konica KM-mount"]},
    "contax-g": {"name": "Contax G", "brand": "Contax", "spellings": ["Contax G-mount"]},
    "contax-rf": {"name": "Contax rangefinder bayonet", "brand": "Contax",
                  "spellings": ["Contax bayonet"],
                  "note": "The source says only `Contax bayonet`, which names "
                          "the rangefinder mount and the SLR mount equally well. "
                          "Filed as the rangefinder one on the strength of the "
                          "bodies carrying it; a correction is a pull request."},
    "qbm": {"name": "Rollei QBM", "brand": "Rollei", "spellings": ["QBM"]},
    "mamiya-breech-lock": {"name": "Mamiya breech-lock bayonet", "brand": "Mamiya",
                           "spellings": ["Custom Mamiya breech-lock bayonet mount"]},
    "mamiya-press": {"name": "Mamiya Press bayonet", "brand": "Mamiya",
                     "spellings": ["Mamiya Press bayonet mount"]},
    "ricoh-rk": {"name": "Ricoh System RK", "brand": "Ricoh",
                 "spellings": ["Ricoh System RK mount"]},
    "tenax-bayonet": {"name": "Tenax bayonet", "brand": "Zeiss Ikon",
                      "spellings": ["Tenax bayonet"]},
    "hasselblad-v": {"name": "Hasselblad V", "brand": "Hasselblad",
                     "spellings": ["Hasselblad V"]},
    "fuji-gx680": {"name": "Fuji GX680", "brand": "Fujifilm",
                   "spellings": ["Fuji GX680"]},
    "m42": {"name": "M42", "spellings": ["M42 screw mount", "Screw"],
            "note": "A thread, not a product: Praktica, Pentax, Zenit, Chinon "
                    "and others all used it, and no one of them owns it. That is "
                    "why a mount has no brand segment in its URL. The bare "
                    "spelling `Screw` is ruled here rather than under "
                    "`leica-m39`: it comes from the Edixa Reflex, a West German "
                    "SLR built by Wirgin on the M42 thread."},
}


# A name the source leaves ambiguous, corrected from the source itself.
#
# `List of lenses for Hasselblad cameras` distinguishes its lenses by a **barrel
# version** column — C, CF, CFi, CFE, F, FE, CB — that the extraction never
# read, composing a name from focal length, aperture, maker and family only. Two
# genuinely different lenses therefore arrived under one name, and the `(T*)`
# that some rows carry is the article being inconsistent about coating rather
# than a product difference: the parenthesised row is always the C barrel.
# Appending the version is what the source already says, and it is the only
# thing that makes these addressable.
#
# **The Hasselblad V section is known to be incomplete for the same reason.**
# The table gives four 50 mm f/4 Distagons (C, CF, CFi, ZV) and five 80 mm f/2.8
# Planars (C, F, CF/CFE, FE, CB) where this index carries two of each. Reading
# that column properly is a change to the extraction, not a ruling.
NAME_RULINGS = {
    "Zeiss Distagon (T*) 40mm f/4": "Zeiss Distagon (T*) 40mm f/4 C",
    "Zeiss Distagon T* 40mm f/4": "Zeiss Distagon T* 40mm f/4 CF",
    "Zeiss Distagon (T*) 50mm f/4": "Zeiss Distagon (T*) 50mm f/4 C",
    "Zeiss Distagon T* 50mm f/4": "Zeiss Distagon T* 50mm f/4 CF",
    "Zeiss Planar (T*) 80mm f/2.8": "Zeiss Planar (T*) 80mm f/2.8 C",
    "Zeiss Planar T* 80mm f/2.8": "Zeiss Planar T* 80mm f/2.8 F",
    "Zeiss Sonnar (T*) 150mm f/4": "Zeiss Sonnar (T*) 150mm f/4 C",
    "Zeiss Sonnar T* 150mm f/4": "Zeiss Sonnar T* 150mm f/4 CF",
}


# An article whose subject sold everything it lists, whoever ground the glass.
#
# Hasselblad's V-system lenses were built by Zeiss, and a few by Schneider and
# Rodenstock, and every one of them was sold by Hasselblad. Filing them under
# their makers put 44 lenses in the wrong shop — the same manufactured-by
# mistake this file exists to avoid, arrived at from the other direction,
# because the *name* carries the maker where the source's structure does not.
#
# The maker stays in the lens's own name, which is where a person reads it
# (`hasselblad/zeiss-planar-t-80mm-f2-8-c`), and the automatic badge alternate
# means someone who looks for it under Zeiss still finds it.
#
# Checked against every other multi-maker source before being written as a rule:
# the Canon FD, Leica, Olympus OM and Pen F lists already resolve correctly,
# because there the name and the seller agree.
SOLD_BY_ARTICLE = {
    "List of lenses for Hasselblad cameras": "Hasselblad",
}
