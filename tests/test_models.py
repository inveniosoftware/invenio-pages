# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2022 CERN.
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

"""Models for Pages module."""

from invenio_pages import Page


def test_page_repr(module_scoped_pages_fixture, base_app):
    dog_page = Page.get_by_url("/dogs/shiba")
    assert dog_page.__repr__() == "URL: /dogs/shiba, title: Page for doge!"


def test_page_versions(module_scoped_pages_fixture, base_app, db):
    dog_page = Page.get_by_url("/dogs")
    dog_page.title = "Just a dog!"
    db.session.commit()

    dog_page = Page.get_by_url("/dogs")
    assert "Just a dog!" == dog_page.title
    assert 2 == dog_page.versions.count()
    assert "Page for Dogs!" == dog_page.versions[0].title
