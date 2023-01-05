..
    This file is part of Invenio.
    Copyright (C) 2015, 2016, 2017 CERN.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.


Changes
=======

Version 1.0.0a6 (released 2023-01-05):
--------------------------------------

- Upgrade invenio packages
- Add alembic recipe

Version 1.0.0a5 (released 2020-04-14):
--------------------------------------

- Add REST API GET Static Page Resource
- Drop support for Python 2.7
- Update python dependencies


Version 1.0.0a4 (released 2017-08-18):
--------------------------------------

- Update minimum Flask version to 0.11.1.
- Improve documentation and examples.

Version 1.0.0a3 (released 2016-06-15):
--------------------------------------

- Major refactoring for Invenio 3.
- Adds versioning support for pages.


Version 0.1.2 (released 2015-10-07):
------------------------------------

- Removes calls to PluginManager consider_setuptools_entrypoints()
  removed in PyTest 2.8.0.
- Adds missing `invenio_base` dependency.

Version 0.1.1 (released 2015-08-25):
------------------------------------

- Adds missing `invenio_upgrader` dependency and amends past upgrade
  recipes following its separation into standalone package.
- Overrides default wtforms field for content column in order to
  display it properly. (closes inveniosoftware/invenio#3311)

Version 0.1.0 (released 2015-07-22):
------------------------------------

- Initial public release.
