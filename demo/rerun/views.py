from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse
from models import Feed, FeedForm, Subscription, SubscriptionForm

def index(request):
    feed_list = Feed.objects.all()
    return render_to_response('rerun/index.html', {'feed_list': feed_list})

def feed(request, feed_id):
    f = get_object_or_404(Feed, id=feed_id)
    return render_to_response('rerun/feed.html', {'feed': f})

def entry(request, entry_id):
    e = get_object_or_404(Entry, id=entry_id)
    return render_to_response('rerun/entry.html', {'entry': e})

def add(request):
    if request.method == 'POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.initialize()
            return render_to_response('rerun/feed.html', {'feed': feed})
    else:
        form = FeedForm()
    return render_to_response('rerun/add.html', {'form': form}, context_instance=RequestContext(request))

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.initialize()
            return render_to_response('rerun/worked.html', {'subscription': sub})
    else:
        form = SubscriptionForm()
    return render_to_response('rerun/subscribe.html', {'form': form}, context_instance=RequestContext(request))

def deliver(request, subscription_id):
    s = Subscription.objects.get(id=subscription_id)
    s.deliver_entry()
    return xml(request, subscription_id)

def xml(request, subscription_id):
    s = Subscription.objects.get(id=subscription_id)
    xml_string = s.xml.read()
    return HttpResponse(xml_string, mimetype="application/atom+xml")

