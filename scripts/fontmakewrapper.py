#!/bin/env python3
#
# This wrapper works around fontmake's limitation (at the time of this writing)
# of not being able to specify the output directory for the generated font
# binaries. The Meson build system's custom target function expects those files
# to be on the same level in the build directory as the concerned meson.build
# file for the install command to work properly. Also, autohint the binaries
# while we're at it.

import os
import glob
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("fontmake", type=str, help="The path to fontmake.")
parser.add_argument("psautohint", type=str, help="The path to psautohint.")
parser.add_argument("font_source", help="The path to the font source.")
args = parser.parse_args()

fontname = os.path.basename(args.font_source).split(".")[0]

if not args.font_source.endswith(".glyphs"):
    raise(ValueError,
          "This script currently only handles Glyphs sources.")

subprocess.run([args.fontmake, "-g", args.font_source, "-i", "-o", "otf"])

font_binaries_glob = os.path.join(
    os.getcwd(), "instance_otf", fontname) + "*otf"
font_binaries = glob.glob(font_binaries_glob)

for font in font_binaries:
    moved_font = os.path.join(os.getcwd(), os.path.basename(font))
    os.rename(font, os.path.join(os.getcwd(), moved_font))
    subprocess.run([args.psautohint, moved_font])
