# this should be done when a feed is entered (check first that it doesn't exist in the database)
from models import Entry

import feedparser

import urllib2
def sanitize_url(url):
    return urllib2.quote(url, '')
    # the second argument to quote here is a list of "safe" characters that should not be escaped... in this case, none.

# max_entries = 1000
max_entries = 10 # no point in testing with the real max_entries...

# feedparser.USER_AGENT = "MyApp/1.0 +http://example.com/"

def fetch_old_entries(feed):
    # example url: http://www.google.com/reader/public/atom/feed/http://feeds.feedburner.com/thesimpledollar?n=1000
    feed_url = 'http://feeds.feedburner.com/thesimpledollar'
    google_url = 'http://www.google.com/reader/public/atom/feed/' + sanitize_url(feed_url) + '?n=' + str(max_entries)

    # print "Fetching feed from", feed_url, "..."
    f = feedparser.parse(google_url)
    # print "Fetched", len(f.entries), "entries of", f.feed.title

    # print "Creating new feed..."
    for i in f.entries:
        e = Entry(title=i.title, link=i.link, description=i.description,   date=i.updated_parsed)
        e.feed = feed
        e.save()

