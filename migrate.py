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

        with open('./output/%s.xml' % name, 'w') as output:
            output.write(template.render().encode('utf-8'))


if __name__ == '__main__':
    main()