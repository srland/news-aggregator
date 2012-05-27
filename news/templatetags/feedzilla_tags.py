import random

from django import template
from django.utils.safestring import mark_safe

from tagging.models import Tag

from feedzilla.models import Feed, Post


register = template.Library()

@register.inclusion_tag('feedzilla/tag_cloud.html', takes_context=True)
def feedzilla_tag_cloud(context):
    """
    Show tag cloud for specified site.
    """

    tags = Tag.objects.cloud_for_model(Post, filters={'active': True})

    return {'tags': tags,
            }


@register.inclusion_tag('feedzilla/donor_list.html')
def feedzilla_donor_list():
    """
    Show aggregated feed.
    """

    donors = Feed.objects.all()

    return {'donors': donors,
            }


@register.inclusion_tag('feedzilla/feed_head.html')
def feedzilla_feed_head(feed_id, number=3):
    """
    Show last 'number' messages from feed.
    """

    try:
        feed = Feed.objects.get(pk=feed_id)
        messages = feed.posts.all().filter(active=True)[:number]
    except Feed.DoesNotExist:
        feed = None
        messages =  []

    return {'feed': feed,
            'messages': messages,
            }

@register.filter
def feedzilla_strong_spaces(text):
        return mark_safe(text.replace(u' ',u'&nbsp;'))


#---
MOMENT = 120    # duration in seconds within which the time difference 
                # will be rendered as 'a moment ago'
 
@register.filter
def naturalTimeDifference(value):
    """
    Finds the difference between the datetime value given and now()
    and returns appropriate humanize form
    I made two changes to improve your code, feel free to share with others. 
    First, if the filter is passed a datetime.timedelta object 
    it uses that instead of calculating datetime.now() - value. 
    Second, with one additional conditional it
    now says "1 hour ago" for (7200 > delta.seconds >= 3600) 
    and "N hours ago" for delta >= 7200. 
    Small changes for a grammatically correct result.
    """
 
    from datetime import datetime, timedelta
    
    if isinstance(value, timedelta):
        delta = value
    elif isinstance(value, datetime):
        delta = datetime.now() - value
    else:
        delta = None
        
    if delta:
        if delta.days > 6:
            return value.strftime("%B %d") + ' at ' + str.lower(value.strftime("%I:%M%p")) # May 15 at 10:16am
        if delta.days > 1:
            return value.strftime("%a") + ' at ' + str.lower(value.strftime("%I:%M%p")) # Wed at 10:16am
        elif delta.days == 1:
            return 'Yesterday at ' + str.lower(value.strftime("%I:%M%p"))  # Yesterday 07:13am
        elif delta.seconds >= 7200:
            return str(delta.seconds / 3600 ) + ' hours ago' # 3 hours ago
        elif delta.seconds >= 3600:
            return '1 hour ago'                              # 1 hour ago
        elif delta.seconds > MOMENT:
            return str(delta.seconds/60) + ' minutes ago'    # 29 minutes ago
        else:
            return 'a moment ago'                            # a moment ago if below a minute 
        return defaultfilters.date(value)
    else:
        return str(value)
    """
    if isinstance(value, datetime):
        delta = datetime.now() - value
        if delta.days > 6:
            return value.strftime("%b %d")                    # May 15
        if delta.days > 1:
            return value.strftime("%A")                       # Wednesday
        elif delta.days == 1:
            return 'Yesterday'                                # Yesterday
        elif delta.seconds > 3600:
            return str(delta.seconds / 3600 ) + ' hours ago'  # 3 hours ago
        elif delta.seconds >  MOMENT:
            return str(delta.seconds/60) + ' minutes ago'     # 29 minutes ago
        else:
            return 'a moment ago'                             # a moment ago
        return defaultfilters.date(value)
    else:
        return str(value)
    """    
#register.filter(naturalTimeDifference)
    