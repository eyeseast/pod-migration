"""
Define migration schemas in dictionaries here.
"""
import datetime
from decimal import Decimal

from dateutil.parser import parse
from slugify import slugify

from db import db, tags

def get_tag(id):
    """
    Return a tag name using an id, coercing to Decimal if needed.
    """
    id = Decimal(id)
    return tags.get(id)


def get_tags(tag_str):
    """
    Return a list of tags from a tag string.
    """
    return [get_tag(t.strip()) for t in tag_str.split(',')]


TABLES = {
    'lst_nieman_reports_articles': {},

    'lst_site_page': {},
    
    'lst_nieman_reports_issue_themes': {},
    
    'lst_news': {},
    
    'lst_niemans_news': {},

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
            'content': lambda a: a['Text'].decode('utf-8'),
            'excerpt': lambda a: a['Teaser'].decode('utf-8'),
            'post_id': 'id',
            'post_date': 'created_datetime',
            'post_date_gmt': 'created_datetime',
            'post_name': lambda a: slugify(a['Title']),
            'authors': lambda a: [a['Author']], # make it a list
            #'category:reports-issues': lambda a: [],
            #'category:post_tag': lambda a: get_tags(a['Tags'] or ''),
            'subhead': 'SubTitle',
            'pod_id': 'id',
            'pod_version': 'version',
            'pod_item_status': 'item_status',
            'imported': lambda a: datetime.datetime.now()
        }
    },

    'lst_watchdog_articles': {}
}