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
hugo --minify --panicOnWarning --destination public

echo "── build against manifest"
python3 tools/check_stubs.py
