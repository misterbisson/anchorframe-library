#!/bin/sh
# Everything CI runs, in the order CI runs it.
#
# This exists because a check verified against a different build than the one
# that ships is not a check, and that has now cost two red CI runs. The stub
# detector was written against unminified markup and CI builds with `--minify`;
# a deprecated config key logged an error that a local `--quiet` swallowed.
# Both passed locally and failed on push.
#
# So: no --quiet, no shortcuts, same flags as .github/workflows/check.yml.
set -eu
cd "$(dirname "$0")/.."

echo "── tests"
python3 -m unittest discover -s tools -p 'test_*.py' -t tools

echo "── corpus"
python3 tools/validate.py

echo "── sheets"
python3 tools/build.py

echo "── site"
# Remove the output first, because check_stubs.py reads this directory as
# though it were the build and Hugo leaves behind files it no longer generates.
# Renaming taxonomy terms left the old terms' pages in public/, so the page
# count was 19 too high and the link check reported links from pages that no
# longer exist.
#
# `--cleanDestinationDir` is the flag that sounds like it does this and does
# not: a page planted in public/ survives a build carrying it. CI never sees
# any of this because it checks out fresh, which is exactly why it only ever
# goes wrong on the machine where someone is deciding whether their change is
# finished.
rm -rf public
hugo --minify --panicOnWarning --destination public

echo "── build against manifest"
python3 tools/check_stubs.py
