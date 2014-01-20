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
from itertools import groupby
from jinja2 import Environment, FileSystemLoader
from slugify import slugify

from db import db
from schema import TABLES

# template setup
# relative path is ok since this won't move
env = Environment(loader=FileSystemLoader('./templates'))

# add filters
env.filters['slugify'] = slugify

def convert(article, schema):
    """
    Map article fields to WP types according to schema.
    """
    data = {}
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

        # render with posts
        xml = template.render(posts=posts)

        with open('./output/%s.xml' % name, 'w') as output:
            output.write(xml.encode('utf-8'))


if __name__ == '__main__':
    main()