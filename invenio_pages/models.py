# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015, 2016 CERN.
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

from flask import current_app
from invenio_db import db
from sqlalchemy.orm import validates
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

    content = db.Column(db.Text(), nullable=False, default='')
    """Page content. Default is pages/templates/default.html"""

    description = db.Column(db.String(200), nullable=False, default='')
    """Page description."""

    template_name = db.Column(db.String(70), nullable=False)
    """Page template name."""

    @classmethod
    def get_by_url(self, url):
        """Get a page by URL.

        :param url: The page URL.
        :returns: A :class:`invenio_pages.models.Page` instance.
        """
        return Page.query.filter_by(url=url).one()

    @classmethod
    def get_by_id(self, id):
        """Get a page by ID.

        :param id: The page ID.
        :returns: A :class:`invenio_pages.models.Page` instance.
        """
        return Page.query.filter_by(id=id).one()

    @validates('template_name')
    def validate_template_name(self, key, value):
        """Validate template name.

        :param key: The template path.
        :param value: The template name.
        :raises ValueError: If template name is wrong.
        """
        if value not in dict(current_app.config['PAGES_TEMPLATES']):
            raise ValueError(
                'Template "{0}" does not exist.'.format(value))
        return value

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

    id = db.Column(
        db.Integer, nullable=False, primary_key=True, autoincrement=True)
    """PageList identifier."""

    list_id = db.Column(
        db.Integer, db.ForeignKey(Page.id), nullable=False)
    """Id of a list."""

    page_id = db.Column(
        db.Integer, db.ForeignKey(Page.id), nullable=False)
    """Id of a page."""

    order = db.Column(db.Integer, nullable=False)

    list = db.relationship(
        Page,
        backref=db.backref("pages", cascade="all, delete-orphan"),
        foreign_keys=[list_id])
    """Relation to the list."""

    page = db.relationship(
        Page,
        backref=db.backref("lists", cascade="all, delete-orphan"),
        foreign_keys=[page_id])
    """Relation to the page."""
