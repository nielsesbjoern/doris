#!/usr/bin/env sh
# Run full build and fail if generated files differ from git (CI + pre-commit).
set -eu
cd "$(dirname "$0")/.."
python3 scripts/test_seo.py
python3 scripts/test_site.py
python3 scripts/check_links.py
python3 scripts/build.py
git diff --exit-code || {
  echo "Build produced uncommitted changes. Run 'python3 scripts/build.py' and commit."
  git diff --stat
  exit 1
}
