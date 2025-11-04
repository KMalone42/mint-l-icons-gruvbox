#!/usr/bin/env bash
rsync -a --delete ./usr/share/icons/ ./mint-l-icons-gruvbox-dark/
rm -rf ./usr/ ./src/
