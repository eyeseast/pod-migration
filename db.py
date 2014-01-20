"""
Database setup here, so we can import.
"""
import dataset

db = dataset.connect('mysql://root@localhost/nieman')

# get tags once and store in a dictionary
# we probably only need id and Title
tags = dict((t['id'], t['Tag']) for t in db['lst_tags'])

# same for issues
issues = dict((t['id'], t['Label']) for t in db['lst_nieman_reports_issue_themes'])