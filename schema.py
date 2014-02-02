"""
Define migration schemas in dictionaries here.
"""
import datetime
from decimal import Decimal

from dateutil.parser import parse
from slugify import slugify

from db import db, tags, issues

NOW = datetime.datetime.now()

# Mon, 09 Dec 2013 22:26:28 +0000
DATE_FORMAT = "%a, %b %d %Y %H:%M:%S +0000"

def get_tag(id):
    """
    Return a tag name using an id, coercing to Decimal if needed.
    """
    id = Decimal(id)
    return tags.get(id)


def get_tags(tag_str=None):
    """
    Return a list of tags from a tag string.
    """
    if tag_str:
        return [get_tag(t.strip()) for t in tag_str.split(',')]
    return []


def safe_type(obj, cast, default=None):
    """
    Cast object into a type, falling back to default.
    """
    try:
        return cast(obj)
    except:
        return default


TABLES = {

    'lst_site_page': {},
    
    'lst_news': {
        'template': 'foundation-posts.xml',
        'fields': {
            'id': 'id',
            'version': 'version',
            'pubDate': 'created_datetime',
            'creator': 'created_by',
            'title': 'Headline',
            'slug': lambda a: slugify(a['Headline']),
            'content': lambda a: a['Text'].decode('utf-8').strip(),
            'excerpt': lambda a: a['Teaser'].decode('utf-8'),
            'tags': lambda a: get_tags(a['Tags'] or ''),
            'post_date': 'created_datetime',
            'url': 'URL',
            'url_text': 'URL Text',
            'image': 'Teaser Image',
            'imported': lambda a: NOW.strftime('%Y-%m-%d'),
        },
    },
    
    'lst_niemans_news': {
        'template': 'foundation-posts.xml',
        'fields': {
            'id': 'id',
            'version': 'version',
            'pubDate': 'created_datetime',
            'post_date': 'created_datetime',
            'title': 'Headline',
            'slug': lambda a: slugify(a['Headline']),
            'content': lambda a: a['Text'].decode('utf-8').strip(),
            'excerpt': lambda a: a['Teaser'].decode('utf-8'),
            'url': 'URL',
            'url_text': 'URL Text',
            'image': 'Teaser Image',

            # taxonomies
            'tags': lambda a: get_tags(a['Tags'] or ''),
            'categories': lambda a: ['Niemans in the News']
        }
    },

    'lst_nieman_reports_articles': {
        'template': 'nieman-reports-article.xml',
        'chunks': 1000, # break this list chunks of this length
        'fields': {
            'id': 'id',
            'version': 'version',
            'title': lambda a: a['Title'].decode('utf-8'),
            'pubDate': 'created_datetime',
            'creator': 'created_by',
            'guid': 'id',
            'content': lambda a: a['Text'].decode('utf-8').strip(),
            'excerpt': lambda a: a['Teaser'].decode('utf-8'),
            'post_id': 'id',
            'post_date': 'created_datetime',
            'post_date_gmt': 'created_datetime',
            'post_name': lambda a: slugify(a['Title']),
            'subhead': lambda a: a['SubTitle'].decode('utf-8'),
            'pod_id': 'id',
            'pod_version': 'version',
            'pod_item_status': 'item_status',
            'imported': lambda a: NOW.strftime('%Y-%m-%d'),

            # taxonomies
            'authors': lambda a: [a['Author'].decode('utf-8')], # make it a list
            'issues': lambda a: [issues.get(safe_type(a['Issue - Theme'], Decimal))],
            'tags': lambda a: get_tags(a['Tags'] or ''),
        }
    },

    'lst_nieman_reports_onlineonly_articles': {
        'template': 'nieman-reports-article.xml',
        #'query': 'SELECT *, max(version) FROM lst_nieman_reports_onlineonly_articles GROUP BY id',
        'fields': {
            'id': 'id',
            'title': lambda a: a['Title'].decode('utf-8'),
            #'link'
            'pubDate': 'created_datetime',
            'creator': 'created_by',
            'guid': 'id',
            'content': lambda a: a['Text'].decode('utf-8').strip(),
            'excerpt': lambda a: a['Teaser'].decode('utf-8'),
            'post_id': 'id',
            'post_date': 'created_datetime',
            'post_date_gmt': 'created_datetime',
            'post_name': lambda a: slugify(a['Title']),
            'subhead': 'SubTitle',
            'pod_id': 'id',
            'pod_version': 'version',
            'pod_item_status': 'item_status',
            'imported': lambda a: NOW.strftime('%Y-%m-%d'),

            # taxonomies
            'authors': lambda a: [a['Author']], # make it a list
            'issues': lambda a: [issues.get(safe_type(a['Issue - Theme'], Decimal))],
        }
    },

    'lst_watchdog_articles': {
        'template': 'nieman-reports-article.xml',
        'fields': {
            'id': 'id',
            'version': 'version',
            'pubDate': 'created_datetime',
            'creator': 'created_by',
            'title': lambda a: a['Title'].decode('utf-8').strip(),
            'content': lambda a: a['Text'].decode('utf-8').strip(),
            'excerpt': lambda a: a['Summary'].decode('utf-8'),
            'post_date': 'created_datetime',
            'post_date_gmt': 'created_datetime',
            'subhead': 'SubTitle',
            'pod_id': 'id',
            'pod_version': 'version',
            'pod_item_status': 'item_status',
            'imported': lambda a: NOW.strftime('%Y-%m-%d'),

            # taxonomies
            'authors': lambda a: [a['Author']], # make it a list
            'categories': lambda a: ['Watchdog']
        }
    }
}