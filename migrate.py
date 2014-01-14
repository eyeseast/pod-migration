#!/usr/bin/env python
"""
Migrate the Nieman Reports database from Pod to WordPress XML.

Tables are mapped from Pod fields to WordPress fields.
This assumes a mysql database running locally called "nieman" that has been
prepopulated with Pod data.
"""

import dataset
from decimal import Decimal
from schema import TABLES

db = dataset.connect('mysql://root@localhost/nieman')

# get tags once and store in a dictionary
# we probably only need id and Title
tags = dict((t['id'], t['Tag']) for t in db['lst_tags'])