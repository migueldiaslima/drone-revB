#!/bin/bash
# make_overleaf.sh - build self-contained Overleaf zips for both reports in report/dist/
# Usage (from the repo root): bash report/make_overleaf.sh
set -e
cd "$(dirname "$0")"
for r in extensive compact; do
  tmp=$(mktemp -d)
  mkdir -p "$tmp/$r/figures" "$tmp/common"
  cp -r "$r"/. "$tmp/$r/"
  cp common/* "$tmp/common/"
  cp figures/* "$tmp/$r/figures/" 2>/dev/null || true
  # Overleaf compiles main.tex at the project root: flatten paths
  ( cd "$tmp/$r" && sed -i 's#\.\./common/#common/#g' main.tex && mv ../common . )
  rm -f "dist/${r}_overleaf.zip"
  ( cd "$tmp/$r" && zip -qr "$OLDPWD/dist/${r}_overleaf.zip" . -x '*.aux' '*.log' '*.out' '*.toc' '*.pdf' )
  rm -rf "$tmp"
  echo "dist/${r}_overleaf.zip"
done
