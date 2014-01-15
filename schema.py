"""
Define migration schemas in dictionaries here.
"""
import datetime
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
	    'fields': {
		    'title': 'Title',
		    #'link'
		    'pubDate': 'created_datetime',
		    'creator': 'created_by',
		    'guid': 'id',
		    'content:encoded': 'Text',
		    'excerpt:encoded': 'Teaser',
		    'wp:post_id': 'id',
		    'wp:post_date': 'created_datetime',
		    'wp:post_date_gmt': 'created_datetime',
		    'wp:post_name': lambda a: lambda a: slugify(a['Title']),
		    'category:authors': 'Author',
		    #'category:reports-issues': lambda a: [],
		    'category:post_tag': lambda a: get_tags(a['Tag']),
		    'subhead': 'SubTitle',
		    'pod_id': 'id',
		    'pod_version': 'version',
		    'pod_item_status': 'item_status',
		    'imported': datetime.datetime.now()
	    }
	},
	'lst_watchdog_articles': {}
}