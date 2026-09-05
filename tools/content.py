"""Reading the corpus: one leaf bundle per thing.

Every record is `content/<kind>/<brand>/<slug>/index.md` — a Hugo **leaf
bundle**, which is a directory even when it holds one file. That is deliberate
and it is not about storage: a directory sitting beside a record is an
invitation to drop a photograph into it, and a bare `<slug>.md` is not. Since
promotion from flat file to bundle would be as disruptive as the move to
markdown was, everything starts as a bundle.
"""

from __future__ import annotations

import os
import tomllib
import urllib.parse
from dataclasses import dataclass, field

KINDS = ("camera", "film", "lens")
FRONT = "+++"
IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".tif", ".tiff")


def url_prefix(root: str) -> str:
    """The path Hugo serves under, read from its own config.

    Hugo is the authority on what a URL is; everything here only asserts what it
    will produce. Hardcoding `/library` in the Python instead would be a second
    copy of a fact — and the kind that goes wrong quietly, since Hugo would
    follow a changed `baseURL` while the sheets and the redirect manifest kept
    emitting the old prefix.
    """
    with open(os.path.join(root, "hugo.toml"), "rb") as fh:
        base = tomllib.load(fh).get("baseURL", "")
    return urllib.parse.urlparse(base).path.rstrip("/")


@dataclass
class Record:
    kind: str
    brand_slug: str
    slug: str
    path: str                       # repo-relative, for error messages
    meta: dict
    body: str
    images: list[str] = field(default_factory=list)
    prefix: str = ""                # from hugo.toml's baseURL, never a literal

    @property
    def url(self) -> str:
        return f"{self.prefix}/{self.kind}/{self.brand_slug}/{self.slug}"

    @property
    def list_url(self) -> str:
        """Its row in the brand list — where it redirects while it has nothing to show."""
        # Trailing slash before the fragment, because that is what Hugo's own
        # `.Parent.Permalink` produces and Hugo is the authority on URLs here.
        return f"{self.prefix}/{self.kind}/{self.brand_slug}/#{self.slug}"

    @property
    def promoted(self) -> bool:
        """Whether this thing has earned a page of its own.

        Most records are a name, a brand and a link, and a page of that is a
        page that exists in order not to be a 404. A record crosses the line by
        having something to show — prose, a photograph, or a `note` — and the
        moment it does, its page appears at the address it always had. Nothing is
        renamed and no redirect has to be withdrawn by hand, because the
        threshold is computed from the content rather than recorded next to it.

        `note` counts because it is the only place a ruling is written down, and
        a ruling nobody can read is not documentation. The Agfa K-mount lens
        explains that it is a rebadged Chinon; without this that sentence existed
        and was unreachable.
        """
        return bool(self.body.strip()) or bool(self.images) or bool(self.meta.get("note"))


def parse_front_matter(text: str, path: str) -> tuple[dict, str]:
    if not text.startswith(FRONT):
        raise ValueError(f"{path}: no TOML front matter (a file starts with +++)")
    end = text.find("\n" + FRONT, len(FRONT))
    if end < 0:
        raise ValueError(f"{path}: front matter is never closed")
    head = text[len(FRONT):end]
    body = text[end + len(FRONT) + 1:]
    try:
        meta = tomllib.loads(head)
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"{path}: front matter is not valid TOML — {e}") from e
    return meta, body


def load_brands(root: str) -> tuple[dict[tuple[str, str], dict], list[str]]:
    """Every brand's own page: `content/<kind>/<brand>/_index.md`.

    A brand is a *shelf*, and a shelf can have had more than one name over the
    years — `Svema (Astrum)` is Svema film made by its successor company, and
    someone looking for either should land in the same place. Those other names
    live in the brand page's `aliases`, which is the same Hugo field a record
    uses, so Hugo builds the redirect and nothing here has to.
    """
    brands: dict[tuple[str, str], dict] = {}
    broken: list[str] = []
    for kind in KINDS:
        base = os.path.join(root, "content", kind)
        if not os.path.isdir(base):
            continue
        for brand_slug in sorted(os.listdir(base)):
            bdir = os.path.join(base, brand_slug)
            if not os.path.isdir(bdir):
                continue
            page = os.path.join(bdir, "_index.md")
            rel = f"content/{kind}/{brand_slug}/_index.md"
            if not os.path.isfile(page):
                broken.append(f"content/{kind}/{brand_slug}: no _index.md, so the "
                              f"brand has no page and no place to carry its other names")
                continue
            try:
                meta, _ = parse_front_matter(open(page, encoding="utf-8").read(), rel)
            except ValueError as e:
                broken.append(str(e))
                continue
            brands[(kind, brand_slug)] = meta
    return brands, broken


def load(root: str) -> tuple[list[Record], dict[str, dict], list[str]]:
    """Records, mount terms, and any file that could not be read at all."""
    records: list[Record] = []
    mounts: dict[str, dict] = {}
    broken: list[str] = []
    prefix = url_prefix(root)

    def read(path, rel):
        with open(path, encoding="utf-8") as fh:
            return parse_front_matter(fh.read(), rel)

    for kind in KINDS:
        base = os.path.join(root, "content", kind)
        if not os.path.isdir(base):
            broken.append(f"content/{kind}: missing")
            continue
        for brand_slug in sorted(os.listdir(base)):
            bdir = os.path.join(base, brand_slug)
            if not os.path.isdir(bdir):
                # `_index.md` for the kind itself is a list page, not a record.
                if brand_slug != "_index.md":
                    broken.append(f"content/{kind}/{brand_slug}: not a brand directory")
                continue
            for slug in sorted(os.listdir(bdir)):
                sdir = os.path.join(bdir, slug)
                rel = f"content/{kind}/{brand_slug}/{slug}"
                if not os.path.isdir(sdir):
                    if slug != "_index.md":
                        broken.append(f"{rel}: every record is a leaf bundle "
                                      f"(a directory holding index.md), never a bare file")
                    continue
                page = os.path.join(sdir, "index.md")
                if not os.path.isfile(page):
                    broken.append(f"{rel}: bundle has no index.md")
                    continue
                try:
                    meta, body = read(page, f"{rel}/index.md")
                except ValueError as e:
                    broken.append(str(e))
                    continue
                images = sorted(f for f in os.listdir(sdir)
                                if f.lower().endswith(IMAGE_SUFFIXES))
                records.append(Record(kind, brand_slug, slug, f"{rel}/index.md",
                                      meta, body, images, prefix))

    mdir = os.path.join(root, "content", "mount")
    for term in sorted(os.listdir(mdir)) if os.path.isdir(mdir) else []:
        tdir = os.path.join(mdir, term)
        if not os.path.isdir(tdir):
            continue
        page = os.path.join(tdir, "_index.md")
        rel = f"content/mount/{term}/_index.md"
        if not os.path.isfile(page):
            broken.append(f"content/mount/{term}: no _index.md")
            continue
        try:
            meta, _ = read(page, rel)
        except ValueError as e:
            broken.append(str(e))
            continue
        mounts[term] = meta
    return records, mounts, broken
