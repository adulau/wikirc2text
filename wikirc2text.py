# -*- coding: utf-8 -*-
#
#    wikirc2text - dump MediaWiki RecentChanges into text line while keeping
#                  the state of the already seen lines.
#
#    Copyright (C) 2011 Alexandre Dulaunoy (a AT foo.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import feedparser
import sys
from optparse import OptionParser
import time
import datetime

feedparser.USER_AGENT = "wikirc2text - https://github.com/adulau/wikirc2text"
usage = "usage: %s url(s)" % sys.argv[0]
parser = OptionParser(usage)

parser.add_option("-s", "--state", action="store_true" ,dest="state", help="keep state of existing rcline seen and don't output them", default=False)
parser.add_option("-c", "--cleanstate", dest="statesec", help="expire states existing more than number of seconds specified")
parser.add_option("-t", "--tail", action="store_true", dest="tail", help="tail-like operation by continuously appending new changes (--state option is enable)", default=False)
parser.add_option("-w", "--wait", dest="wait", help="number of seconds to wait before refreshing (default is 60)", default=60)
(options, args) = parser.parse_args()

if (options.tail):
    options.state = True

if (options.state):
    import shelve
    import hashlib
    s = shelve.open("wikircstate.shelve")

if len(args) < 1 and not options.statesec:
    print usage
    exit()

def core ():

    if (options.tail):
        r = sys.maxint
    else:
        r = 1

    for x in xrange(r):

        for url in args:
            d = feedparser.parse(url)
            if x == 0:
                print d.feed.title
            for e in d['entries']:
                nicedate = time.strftime("%a, %d %b %Y %H:%M:%S +0000", e.updated_parsed)
                rcline = e.links[0]['href'] + " by " +e.author_detail['name'] +" @ "+ nicedate
                if (options.state):
                    sh = hashlib.md5()
                    sh.update(rcline.encode('utf-8'))
                    sh.digest()
                    shkey = sh.hexdigest()
                    if not (s.has_key(shkey)):
                        s[shkey] =  time.mktime(datetime.datetime.now().timetuple())
                        print rcline.encode('utf-8')
                else:
                    print rcline.encode('utf-8')
        if x > 1:
            time.sleep(float(options.wait))
            if options.statesec is not None:
                expirecache(options.statesec)

    if (options.state):
        s.close()

def expirecache (seconds):
    import shelve
    s = shelve.open("wikircstate.shelve")
    sdeleted = 0
    for k,v in s.iteritems():
        cepoch = time.mktime(datetime.datetime.now().timetuple())
        timedelta = cepoch-v
        if timedelta > float(seconds):
            del s[k]
            sdeleted=sdeleted+1

    s.close()
    log = "%s states deleted" % str(sdeleted)
    sys.stderr.write(log)

core()
