wikirc2text
===========

wikirc2text is a simple Python script to dump MediaWiki
RecentChanges as single text line. The script is able to
keep the state of the already seen lines avoiding to
output the same changes again.

The idea behind the script is to have a simple command-line
interface to dump Wiki RecentChanges feed into other program
like sendxmpp (http://sendxmpp.platon.sk/). As I didn't
want to flood the XMPP conference room with the same output,
I made wikirc2text to track the already seen lines.

Usage
-----

        Usage: wikirc2text.py url(s)

        Options:
          -h, --help            show this help message and exit
          -s, --state           keep state of existing rcline seen and don't output
                                them
          -c STATESEC, --cleanstate=STATESEC
                                expire states existing more than number of seconds
                                specified
          -t, --tail            tail-like operation by continuously appending new
                                changes (--state option is enable)

### Sample usage


    % python wikirc2text.py "http://en.ekopedia.org/w/index.php?title=Special:RecentChanges&feed=atom" --state | head -4
    Ekopedia  - Recent changes [en]
    http://en.ekopedia.org/w/index.php?title=Ecological_rucksack&diff=8004&oldid=prev by Wibil @ Sun, 09 Jan 2011 08:09:03 +0000
    http://en.ekopedia.org/w/index.php?title=User:Wibil/to_do_list&diff=8003&oldid=prev by Wibil @ Sun, 09 Jan 2011 06:31:28 +0000
    http://en.ekopedia.org/User:Social_Networking by Social Networking @ Sat, 08 Jan 2011 20:19:42 +0000

If you do a second request, just after. As there is no changes, there is no output.
If you don't use the --state option, you'll get all the latest changes without checking
the state cache.

    % python wikirc2text.py "http://en.ekopedia.org/w/index.php?title=Special:RecentChanges&feed=atom" --state

You can clear the state following an interval specified in seconds.
   
    % python wikirc2text.py -c 60
    29 states deleted

You can also use the tail-like interface to have a continuous update of the new recent changes.

    % python wikirc2text.py "http://en.ekopedia.org/w/index.php?title=Special:RecentChanges&feed=atom" --tail

### Usage with sendxmpp

    % python wikirc2text.py --state "http://www.hackerspace.lu/w/index.php?title=Special:RecentChanges&feed=atom" | head -5 |sendxmpp -u yourbotname -p yourbotpassword -r yourbotressource -j an.xmpp.server -t -c aconference@conference.somewhere

### Software required

* Python 2.4 and up
* Universal Feed Parser - http://www.feedparser.org/

