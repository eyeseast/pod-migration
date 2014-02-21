"""
Define migration schemas in dictionaries here.
"""
import datetime
from decimal import Decimal

from dateutil.parser import parse
from slugify import slugify

from db import db, tags, issues, themes

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

def set_issue_theme(article):
    """
    Cheating a bit here. This gets an issue and sets a theme in the process.
    """
    theme = themes.get(article['Issue - Theme'])

    # in a few articles, there's no theme, and therefore no issue
    if theme:
        issue = issues.get(theme['Issue'])

        # set both here
        article['themes'] = [theme]
        article['issues'] = [issue]

        return [issue]

    else:
        print "No theme for article: %s" % article['Title']
        article['themes'] = []
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

            # pod_url: http://nieman.harvard.edu/newsitem.aspx?id=100248
            'pod_url': lambda a: 'http://nieman.harvard.edu/newsitem.aspx?id={0}'.format(a['id']),
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
            'categories': lambda a: ['Niemans in the News'],

            # pod_url: http://nieman.harvard.edu/inthenewsitem.aspx?id=100358
            'pod_url': lambda a: 'http://nieman.harvard.edu/inthenewsitem.aspx?id={0}'.format(a['id'])
        }
    },

    'lst_nieman_reports_articles': {
        'template': 'nieman-reports-article.xml',
        'chunks': 500, # break this list chunks of this length
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
            #'issues': lambda a: [issues.get(safe_type(a['Issue - Theme'], Decimal))],
            'tags': lambda a: get_tags(a['Tags'] or ''),
            'issues': set_issue_theme,

            # url: http://www.nieman.harvard.edu/reports/article/103050/Urban-Ruins-and-the-New-Unconscious.aspx
            'pod_url': lambda a: 'http://www.nieman.harvard.edu/reports/article/{id}/{slug}.aspx'.format(
                id=a['id'],
                slug=slugify(a['Title'])
            )
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

            # pod_url: http://www.nieman.harvard.edu/reports/article-online-exclusive/100008/A-Reporters-Toolbag-Reduced-to-TwoFlip-Camera-and-iPhone.aspx
            'pod_url': lambda a: 'http://www.nieman.harvard.edu/reports/article-online-exclusive/{id}/{slug}.aspx'.format(
                id=a['id'], slug=slugify(a['Title']))
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
            'categories': lambda a: ['Watchdog'],

            # pod_url: http://www.nieman.harvard.edu/reports/watchdogarticle/100022/The-Too-Many-Prisoners-Dilemma.aspx
            'pod_url': lambda a: 'http://www.nieman.harvard.edu/reports/watchdogarticle/{id}/{slug}.aspx'.format(
                id=a['id'], slug=slugify(a['Title'])),
        }
    }
}