# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Static pages module for Invenio."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=3.8.1',
]

extras_require = {
    'docs': [
        'Sphinx>=1.4.2',
    ],
    'mysql': [
        'invenio-db[mysql,versioning]>=1.0.0b2',
    ],
    'postgresql': [
        'invenio-db[postgresql,versioning]>=1.0.0b2',
    ],
    'sqlite': [
        'invenio-db[versioning]>=1.0.0b2',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name in ('mysql', 'postgresql', 'sqlite'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'invenio-base>=1.2.2',
    'invenio-admin>=1.2.0',
    'invenio-rest>=1.2.0'
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_pages', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-pages',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio pages',
    license='GPLv2',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-pages',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_pages = invenio_pages:InvenioPages',

        ],
        'invenio_base.api_apps': [
            'invenio_pages_rest = invenio_pages:InvenioPagesREST',
        ],
        'invenio_i18n.translations': [
            'messages = invenio_pages',
        ],
        'invenio_admin.views': [
            'invenio_pages_page = invenio_pages.admin:pages_adminview',
        ],
        'invenio_db.models': [
            'invenio_pages = invenio_pages.models',
        ],
        'invenio_base.blueprints': [
            'invenio_pages = invenio_pages.views:blueprint',

        ],
        "invenio_base.api_blueprints": [
            'invenio_pages_rest = invenio_pages.rest:blueprint',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 1 - Planning',
    ],
)
