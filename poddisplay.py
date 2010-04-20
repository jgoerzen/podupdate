#!/usr/bin/python

##  Copyright (C) 2005 Nick Piper <nick-gtkpod at nickpiper co uk>
##  Part of the gtkpod project.

# Copyright (C) 2009 John Goerzen
 
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
import magic

from mutagen.id3 import ID3
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-m", "--mountpoint", dest="mountpoint",
                  default="/mnt/ipod",
                  help="use iPod at MOUNTPOINT", metavar="MOUNTPOINT")
(options, args) = parser.parse_args()

ms = magic.open(magic.MAGIC_MIME)
ms.load()

DRYRUN = options.dryrun

print "Mounting database..."
db = gpod.Database(options.mountpoint)

print "Processing database..."

images = {}

trackcount = 0

for track in db:
    trackcount += 1
    print "Track %d: " % trackcount,
    print "%(artist)s, %(album)s, %(title)s, %(genre)s, %(filetype)s, %(comment)s, %(description)s, %(composer)s, %(grouping)s, %(podcasturl)s, %(podcastrss)s, %(subtitle)s, %(tvshow)s, %(keywords)s:" % track

print "Saving database"
db.close()
print "Saved db"
