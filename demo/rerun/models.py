from django.db import models
from django.forms import ModelForm
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import feedparser
from django.utils import feedgenerator
from urllib2 import quote
from time import mktime
from datetime import datetime

class Feed(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100, blank=True)

    def initialize(self):
        f = feedparser.parse(self.get_reader_link())

        self.title = f.feed.get('title', 'No title') + ' Rerun'
        self.author = f.feed.get('author', 'No author')
        self.description = f.feed.get('description', '')
        self.save()

        for i in f.entries:
            e = Entry(title=i.title, link=i.link, content=i.description)
            e.date = datetime.fromtimestamp(mktime(i.updated_parsed))
            e.feed = self
            e.save()

    def get_reader_link(self):
        max_entries = 10
        return 'http://www.google.com/reader/public/atom/feed/' + quote(self.link, '') + '?n=' + str(max_entries)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('rerun.views.detail', [str(self.id)])
    
class Entry(models.Model):
    feed = models.ForeignKey(Feed)
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    link = models.URLField()
    summary = models.TextField(blank=True)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'entries'

#class User(models.Model):
#    pass

class Subscription(models.Model):
#    user = models.ForeignKey(User)
    feed = models.ForeignKey(Feed)
    current_entry = models.ForeignKey(Entry, related_name='+')
    prev_date = models.DateTimeField()
    delivery_rate = models.IntegerField()
    final_entry = models.ForeignKey(Entry, related_name='+')
    xml = models.FileField(upload_to='xml')

    def initialize(self):
        self.prev_date = datetime.now()
        self.current_entry = self.feed.entry_set.all().order_by('date')[0]
        self.final_entry = self.feed.entry_set.all().order_by('-date')[0]
        self.save()
        self.deliver_entry()
        self.write_xml()

    def deliver_entry(self):
        d = EntryDate(entry=self.current_entry, subscription=self, date=datetime.now())
        d.save()
        if self.current_entry == self.final_entry:
            goodbye()
        else:
            self.current_entry = self.feed.entry_set.filter(date__gt=self.current_entry.date).order_by('date')[0]
        self.save()
        self.write_xml()

    def goodbye(self):
        pass

    def write_xml(self):
        xml = feedgenerator.Atom1Feed(
                title=self.feed.title, 
                link=self.feed.link, 
                feed_url=self.feed.get_reader_link(), 
                description=self.feed.description, 
                author_name=self.feed.author)
        for d in self.entrydate_set.all().order_by('-date'):
            e = d.entry
            xml.add_item(
                    title=e.title, 
                    link=e.link, 
                    pubdate=d.date, 
                    description=e.content)
        xml_string = xml.writeString('UTF-8')
        filename = str(self.id) + '.xml'
        self.xml.save(filename, ContentFile(xml_string))

    def __unicode__(self):
        return 'Subscription to ' + self.feed.title

class EntryDate(models.Model):
    subscription = models.ForeignKey(Subscription)
    entry = models.ForeignKey(Entry)
    date = models.DateTimeField()

class FeedForm(ModelForm):
    class Meta:
        model = Feed
        fields = ('link',)

class SubscriptionForm(ModelForm):
    class Meta: 
        model = Subscription
        fields = ('feed', 'delivery_rate')


