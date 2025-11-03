#!/usr/bin/python3
import os

# This script uses green.svg and generates the following files from it:
#
# aqua.svg
# blue.svg
# brown.svg
# grey.svg
# orange.svg
# pink.svg
# purple.svg
# red.svg
# sand.svg
# teal.svg

# It uses the following color table to do so:
COLORS = {}
COLORS["bg235"]     = "282828"
COLORS["red124"]    = "cc241d"
COLORS["green106"]  = "98971a"
COLORS["yellow172"] = "d79921"
COLORS["blue66"]    = "458588"
COLORS["purple132"] = "b16286"
COLORS["aqua72"]    = "689d6a"
COLORS["gray246"]   = "a89984"
COLORS["gray245"]   = "928374"
COLORS["red167"]    = "fb4934"
COLORS["green142"]  = "b8bb26"
COLORS["yellow214"] = "fadb2f"
COLORS["blue109"]   = "83a598"
COLORS["purple175"] = "d3869b"
COLORS["fg223"]     = "ebdbb2"
COLORS["orange166"] = "d65d0e"
COLORS["orange208"] = "fe8019"


GREEN_COLOR = "8bb158"

for color in COLORS:
    value = COLORS[color]
    os.system("sed 's/%s/%s/g' green.svg > %s.svg" % (GREEN_COLOR, value, color))
