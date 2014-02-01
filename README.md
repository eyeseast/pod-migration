Migrating from Pod to WordPress
==============================

To run:

    $ python migrate.py

This puts rendered XML files in the `output` directory. Each table in the database gets its own file. Tables that are too big for one file will be split across multiple files.

Steps:

1. Read a table in the nieman database
2. For each row, render a chunk of XML in WXL format using a Jinja template
3. Write out a finished XML file.
4. Test that WordPress can import the XML file.

Complications:

Pod uses same-table versioning (like WP) so there are duplicates in the database. Do we want every version, or just the latest? How do we know which is the latest version?

What taxonomies are actually used in Pod? How do we find relationships?

All IDs are coming up as Decimal objects. That's weird.

taxonomies
----------

Issue:

Tags: Stored as a string of comma-separated IDs. For example, "100030,100077,100078". This is gross, but it also means there's no join table to find.

Versions: Article types use same-table versioning, so we only want the highest version number. I've solved this on the Python side, by grouping by ID and yielding the article with the highest version number.