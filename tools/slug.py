"""URL slugs, and the one constraint that is not a matter of taste.

A slug becomes a path segment on <https://anchorframe.app/library>, which is
served from a private S3 bucket behind CloudFront. The router there decides
"file or directory" with `uri.lastIndexOf('.') <= uri.lastIndexOf('/')`, so a
slug containing a dot reads as a file with an extension, never has
`/index.html` appended, and 404s. **No dots.** That is why `f/2.8` becomes
`f2-8` rather than the more readable `f2.8`.
"""

import re
import unicodedata

# `f/2.8`, `f2.8`, `F2.8` and `f/2,8` all appear in the sources and all mean the
# same aperture. The slash is dropped before slugging so one notation cannot
# produce three slugs, and `f/4` becomes `f4` rather than `f-4` for the same
# reason: the separator is punctuation in the notation, not a word break. The
# comma form is a European decimal separator, not a list.
_APERTURE = re.compile(r"\bf\s*/\s*(\d+)(?:[.,](\d+))?", re.IGNORECASE)
_DECIMAL_COMMA = re.compile(r"(\d),(\d)")


def slugify(name: str) -> str:
    """Lowercase, ASCII-folded, hyphen-separated. Stable enough to be an address."""
    s = _APERTURE.sub(
        lambda m: f"f{m.group(1)}-{m.group(2)}" if m.group(2) else f"f{m.group(1)}", name)
    s = _DECIMAL_COMMA.sub(r"\1.\2", s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("ø", "o").replace("Ø", "O").replace("ß", "ss")
    s = s.replace("æ", "ae").replace("Æ", "AE").replace("&", " and ")
    s = s.lower()
    # An apostrophe closes up rather than separating: `Soldier's` -> `soldiers`,
    # not `soldier-s`.
    s = re.sub(r"[’'`´]", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


# Segments the site already answers on. A brand may not take one of these.
RESERVED = frozenset({"privacy", "support", "library", "index", "404", "style", "assets"})

VALID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
