#!/usr/bin/env python3

# Move files in music collection to Traktor made shortcut paths


# Installation:
# Using fswatch to monitor changes in dir

# brew install fswatch
# fswatch -o ~/Desktop/test-dir | xargs -n1 -I{} ~/dev/migrate_traktor_aliases/migrate_traktor_aliases.py

# TODO run on background on boot
# TODO use fswatch passed path information with resolve_osx_alias to skip scanning
# TODO check for duplicates even before going through the "New Tunes" folder

import glob
import os

music_collection_dir = "/Users/jasalt/GDrive/Music"

# Log changes on file
import datetime
dt = datetime.datetime.now()
timestamp = dt.strftime('%y%m%d-%H%m')
f = open(music_collection_dir + '/migrated_traktor_aliases.txt', 'a')


# If file already exists in destination, dnd from Traktor makes an alias with text "alias" in the filename
from mac_alias import resolve_osx_alias
alias_filepaths = glob.glob(music_collection_dir + '/**/*.mp3 alias*', recursive=True)
# TODO when you see many alias in one file, delete the duplicates and keep orig.
for filepath in alias_filepaths:
    alias_path = resolve_osx_alias(filepath)
    
    os.remove(filepath)
    if os.path.isfile(alias_path):
        print("Removing duplicate source mp3 %s " % alias_path)
        os.remove(alias_path)
        f.write(timestamp + "; " + alias_path + "; " + 'removed as duplicate\n')


# Find all mp3 paths under music collection
filepaths = glob.glob(music_collection_dir + '/**/*.mp3', recursive=True)

# Separate them into aliases and mp3's
aliases = {}
mp3s = {}


for filepath in filepaths:
    if (os.stat(filepath).st_size < 5000):  # alias is under 5kb # stat st_size=11599045 vs st_size=920
        bname = os.path.basename(filepath)
        aliases[bname] = filepath
    else:
        bname = os.path.basename(filepath)
        mp3s[bname] = filepath



# Move all matching mp3 files to alias paths
for alias,alias_path in aliases.items():


    if alias in mp3s:
        mp3_path = mp3s[alias]
        print("Moving mp3 %s to alias path %s" % (mp3_path, alias_path))
        f.write(timestamp + "; " + mp3_path + "; " + alias_path + '\n')
        os.rename(mp3_path, alias_path)

f.close()
