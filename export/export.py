# =================================================================
#
# Authors: Tom Kralidis <tomkralidis@gmail.com>
#
# Copyright (c) 2018 Tom Kralidis
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================

import csv
import os
import sys

from jinja2 import Environment, FileSystemLoader
from slugify import slugify

THISDIR = os.path.dirname(os.path.realpath(__file__))


def slugify_identifier(value):
    """helper function to slugify identifiers to pass gml:id constraints"""

    return slugify(value)


def dump_csv(version, version_date, csvfile, format_):
    """transforms link type CSV into ISO Codelist Catalogue or SKOS"""

    reader = csv.DictReader(open(csvfile))
    env = Environment(loader=FileSystemLoader(THISDIR))
    env.filters['slugify_identifier'] = slugify_identifier
    if format_ == 'skos':
        template = env.get_template('skos.j2')
    else:
        template = env.get_template('codelists.j2')
    return template.render(version=version, version_date=version_date,
                           link_types=reader)


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print('Usage: {} <version> <version_date> <csv> <format>'.format(
            sys.argv[0]))
        sys.exit(1)

    print(dump_csv(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
