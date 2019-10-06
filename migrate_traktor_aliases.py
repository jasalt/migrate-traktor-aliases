#!/usr/bin/env python3

# Move files in music collection to Traktor made shortcut paths


# Installation:
# Using fswatch to monitor changes in dir

# brew install fswatch
# fswatch -o ~/Desktop/test-dir | xargs -n1 -I{} ~/Desktop/test-dir/migrate_traktor_aliases.py

# TODO run on background on boot

import glob
import os

music_collection_dir = "/Users/jasalt/Desktop/test-dir"

# All find mp3 paths under music collection
filepaths = glob.glob(music_collection_dir + '/**/*.mp3', recursive=True)

# Separate them into aliases and mp3's
aliases = {}
mp3s = {}

for filepath in filepaths:
    if (os.stat(filepath).st_size < 5000):  # alias is under 2kb # stat st_size=11599045 vs st_size=920
        bname = os.path.basename(filepath)
        aliases[bname] = filepath
    else:
        bname = os.path.basename(filepath)
        mp3s[bname] = filepath
 

# Log changes on file
import datetime
dt = datetime.datetime.now()
timestamp = dt.strftime('%y%m%d-%H%m')
f = open(music_collection_dir + '/migrated_traktor_aliases.txt', 'a')

# Move all matching mp3 files to alias paths
for alias,alias_path in aliases.items():
    if alias in mp3s:
        mp3_path = mp3s[alias]
        print("Moving mp3 %s to alias path %s" % (mp3_path, alias_path))
        f.write(timestamp + "; " + mp3_path + "; " + alias_path + '\n')
        os.rename(mp3_path, alias_path)

f.close()