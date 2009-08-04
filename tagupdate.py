#!/usr/bin/python

##  Copyright (C) 2005 Nick Piper <nick-gtkpod at nickpiper co uk>
##  Part of the gtkpod project.
 
##  URL: http://www.gtkpod.org/
##  URL: http://gtkpod.sourceforge.net/

##  The code contained in this file is free software; you can redistribute
##  it and/or modify it under the terms of the GNU Lesser General Public
##  License as published by the Free Software Foundation; either version
##  2.1 of the License, or (at your option) any later version.

##  This file is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##  Lesser General Public License for more details.

##  You should have received a copy of the GNU Lesser General Public
##  License along with this code; if not, write to the Free Software
##  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

##  $Id: coverart_fetch.py 1662 2007-07-31 20:42:54Z tmzullinger $

import os, os.path
import gpod
import sys
import urllib
import gtk
import mutagen.mp3
import mutagen.mp4
from mutagen.id3 import ID3
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-m", "--mountpoint", dest="mountpoint",
                  default="/mnt/ipod",
                  help="use iPod at MOUNTPOINT", metavar="MOUNTPOINT")
(options, args) = parser.parse_args()

print "Mounting database..."
db = gpod.Database(options.mountpoint)

print "Processing database..."

images = {}

trackcount = 0

# Filetype is "AAC audio file" or "MPEG audio file" (mp3)

for track in db:
    trackcount += 1
    print "Track %d: " % trackcount,
    print "%(artist)s, %(album)s, %(title)s, %(filetype)s:" % track

    coverart = track.get_coverart()

    if coverart and coverart.thumbnails:
        #print " Already has artwork, skipping."
        # note we could remove it with track.set_coverart(None)
        print "  Already has artwork; skipping."
        continue

    image_data = None
    loader = gtk.gdk.PixbufLoader()

    filename = track.ipod_filename()
    
    if track['filetype'] == 'MPEG audio file': # MP3
        try:
            f = ID3(filename)
        except:
            print "  No ID3 tags; skipping."
            continue

        apicframes = f.getall("APIC")
        if len(apicframes) >= 1:
            frame = apicframes[0]
            image_data = frame.data
    elif track['filetype'] == 'AAC audio file': # m4a, aac, mp4
        try:
            f = mutagen.mp4.MP4(filename)
        except:
            print "  MP4 couldn't open track; skipping."
            continue

        if 'covr' in f.tags:
            covertag = f.tags['covr'][0]
            image_data = covertag
    else:
        print "  Unknown file format %s; skipping" % track['filetype']
        continue

    if not (image_data is None):
        try:
            loader.write(image_data)
        except:
            print "  Had cover, but in invalid format; skipping."
            continue
        try:
            loader.close()
        except:
            print "  Invalid image (zero-width?); skipping."
            continue

        pixbuf = loader.get_pixbuf()
        if (pixbuf.get_width() > 10 and pixbuf.get_height() > 10):
            try:
                track.set_coverart(pixbuf)
                print "  Added thumbnails"
            except KeyError:
                print "  No image available"
        else:
            print "  Image was too small to use."
    else:
        print "  Found no image data in file."


print "Saving database"
db.close()
print "Saved db"
