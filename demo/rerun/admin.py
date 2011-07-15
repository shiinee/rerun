from models import Feed, Entry, Subscription
from django.contrib import admin

# admin.site.register(Entry)

class EntryInline(admin.StackedInline):
    model = Entry
    extra = 1

class FeedAdmin(admin.ModelAdmin):
    fields = ['title', 'link', 'author', 'description']
    inlines = [EntryInline]
    list_display = ('title', 'link')

admin.site.register(Feed, FeedAdmin)

admin.site.register(Subscription)
