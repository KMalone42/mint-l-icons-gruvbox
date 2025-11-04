#!/usr/bin/env bash
# Usage, creates a barebones project with just the files needed to ship.
rsync -a --delete ./usr/share/icons/ ./mint-l-icons-gruvbox-dark/
rm -rf ./usr/ ./src/
