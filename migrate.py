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
from jinja2 import Environment, FileSystemLoader

from db import db
from schema import TABLES

# template setup
# relative path is ok since this won't move
env = Environment(loader=FileSystemLoader('./templates'))

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

        posts = [convert(article, fields) for article in query]

        with open('./output/%s.xml' % name, 'w') as output:
            output.write(template.render().encode('utf-8'))


if __name__ == '__main__':
    main()