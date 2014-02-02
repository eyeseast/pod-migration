#!/usr/bin/env python
"""
Migrate the Nieman Reports database from Pod to WordPress XML.

Tables are mapped from Pod fields to WordPress fields.
This assumes a mysql database running locally called "nieman" that has been
prepopulated with Pod data.
"""

import dataset
import os

from decimal import Decimal
from itertools import groupby, izip_longest
from jinja2 import Environment, FileSystemLoader
from slugify import slugify

from db import db
from schema import TABLES, DATE_FORMAT

# template setup
# relative path is ok since this won't move
env = Environment(loader=FileSystemLoader('./templates'))

# add filters
def decode(s):
    """
    Make sure we have a utf-8 string.
    """
    if isinstance(s, unicode):
        return s
    return s.decode('utf-8')


def dateformat(s, format=DATE_FORMAT):
    """
    Return a date to string as format.
    """
    return s.strftime(format)

# register filters and globals
env.filters['slugify'] = slugify
env.filters['decode'] = decode
env.filters['dateformat'] = dateformat
env.globals['DATE_FORMAT'] = DATE_FORMAT


def convert(article, schema):
    """
    Map article fields to WP types according to schema.
    """
    # keep everything, then add or overwrite what we need
    data = dict(article)
    for wp, pod in schema.iteritems():
        if callable(pod):
            data[wp] = pod(article)
        else:
            data[wp] = article[pod]

    return data


def get_most_recent(posts):
    """
    Group posts by id and yield the highest version number.
    """
    # consume any iterable before we do anything else
    # then group by id
    posts = groupby(list(posts), lambda p: p['id'])
    for id, group in posts:
        post = sorted(group, key=lambda p: p['version'])[-1]
        yield post


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)


def render(template, posts, name, **kwargs):
    """
    Render an XML file for posts
    Extra kwargs are passed to template.render
    """
    # bail early if None or [] is passed in
    if not posts:
        return

    page = kwargs.get('page')

    if page:
        filename = "./output/%s-%i.xml" % (name, page)
    else:
        filename = "./output/%s.xml" % name

    # render with posts
    xml = template.render(posts=posts, **kwargs)

    with open(filename, 'w') as output:
        output.write(xml.encode('utf-8'))


def main():
    """
    For each table,
    loop through rows
    convert field names
    render a template
    write to output folder.
    """
    for name, schema in TABLES.iteritems():

        if not schema:
            continue
        
        template = env.get_template(schema['template'])
        fields = schema['fields']
        table = db.load_table(name) # fail if the name is wrong

        if "query" in schema:
            query = db.query(schema['query'])
        else:
            query = table.all()

        if "version" in table.columns:
            query = get_most_recent(query)

        posts = [convert(article, fields) for article in query]

        if "chunks" in schema:
            for page, chunk in enumerate(grouper(posts, schema['chunks']), 1):
                render(template, chunk, name=name, page=page)

        else:
            render(template, posts, name=name)


if __name__ == '__main__':
    main()