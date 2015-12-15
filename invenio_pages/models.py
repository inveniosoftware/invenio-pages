# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015 CERN.
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

"""Pages module models."""

from __future__ import absolute_import, print_function

import pkg_resources
from invenio_db import db
from sqlalchemy_utils.models import Timestamp


class Page(db.Model, Timestamp):
    """Represents a page."""

    __versioned__ = {}

    __tablename__ = 'pages_page'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    """Page identifier."""

    url = db.Column(db.String(100), unique=True, nullable=False)
    """Page url."""

    title = db.Column(db.String(200), nullable=False, default='')
    """Page title."""

    content = db.Column(db.Text(length=2**32-2), nullable=False, default='')
    """Page content. Default is pages/templates/default.html"""

    description = db.Column(db.String(200), nullable=False, default='')
    """Page description."""

    template_name = db.Column(db.String(70), nullable=True)
    """Page template name. Default is cfg["PAGES_DEFAULT_TEMPLATE"]."""

    @classmethod
    def get_by_url(self, url):
        """Get a page by URL."""
        return Page.query.filter_by(url=url).one()

    def __repr__(self):
        """Page representation.

        Used on Page admin view in inline model.
        :returns: unambiguous page representation.
        """
        return "URL: %s, title: %s" % (self.url, self.title)


class PageList(db.Model):
    """Represent association between page and list."""

    __versioned__ = {}

    __tablename__ = 'pages_pagelist'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    """PageList identifier."""

    list_id = db.Column(db.Integer,
                        db.ForeignKey(Page.id), nullable=False)
    """Id of a list."""

    page_id = db.Column(db.Integer,
                        db.ForeignKey(Page.id), nullable=False)
    """Id of a page."""

    order = db.Column(db.Integer, nullable=False)

    list = db.relationship(Page,
                           backref=db.backref("pages",
                                              cascade="all, delete-orphan"),
                           foreign_keys=[list_id])
    """Relation to the list."""

    page = db.relationship(Page,
                           backref=db.backref("lists",
                                              cascade="all, delete-orphan"),
                           foreign_keys=[page_id])
    """Relation to the page."""
