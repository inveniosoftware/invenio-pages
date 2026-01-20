# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2025 CERN.
# Copyright (C) 2025      University of Münster.
# Copyright (C) 2025-2026 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Pages module models."""

from flask import current_app
from invenio_db import db
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import validates
from sqlalchemy.sql import text

from .errors import PageNotCreatedError, PageNotFoundError


class PageModel(db.Model, db.Timestamp):
    """Represents a page."""

    __versioned__ = {}

    __tablename__ = "pages_page"

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    """Page identifier."""

    url = db.Column(db.String(100), nullable=False)
    """Page url."""

    title = db.Column(db.String(200), nullable=False, default="")
    """Page title."""

    lang = db.Column(db.CHAR(2), nullable=False, server_default="en")
    """Page language. Default is 'en'"""

    content = db.Column(db.Text(), nullable=False, default="")
    """Page content. Default is pages/templates/default.html"""

    description = db.Column(db.String(200), nullable=False, default="")
    """Page description."""

    template_name = db.Column(db.String(70), nullable=False)
    """Page template name."""

    __table_args__ = (
        db.UniqueConstraint("url", "lang", name="uq_pages_page_url_lang"),
    )

    @classmethod
    def create(cls, data):
        """Create a new page."""
        try:
            with db.session.begin_nested():
                obj = cls(
                    url=data["url"],
                    title=data.get("title", ""),
                    content=data.get("content", ""),
                    lang=data.get("lang", "en"),
                    description=data.get("description", ""),
                    template_name=data["template_name"],
                )
                db.session.add(obj)

            return obj
        except IntegrityError:
            raise PageNotCreatedError(data["url"])

    @classmethod
    def get_by_url(cls, url, lang="en"):
        """Get a page by URL.

        :param url: The page URL.
        :returns: A :class:`invenio_pages.records.models.PageModel` instance.
        """
        try:
            return cls.query.filter_by(url=url, lang=lang).one()
        except NoResultFound:
            raise PageNotFoundError(url)

    @classmethod
    def get(cls, id):
        """Get a page by ID.

        :param id: The page ID.
        :returns: A :class:`invenio_pages.records.models.PageModel` instance.
        """
        try:
            return cls.query.filter_by(id=id).one()
        except NoResultFound:
            raise PageNotFoundError(id)

    @classmethod
    def search(cls, search_params, filters):
        """Get pages according to param filters.

        :param search_params: The maximum resources to retreive.
        :param filters: The search filters.
        :returns: A list of the :class:`invenio_pages.records.models.PageModel` instance.
        """
        pages = (
            cls.query.filter(*filters)
            .order_by(
                search_params["sort_direction"](text(",".join(search_params["sort"])))
            )
            .paginate(
                page=search_params["page"],
                per_page=search_params["size"],
                error_out=False,
            )
        )
        return pages

    @classmethod
    def update(cls, data, id):
        """Update an existing page."""
        with db.session.begin_nested():
            cls.query.filter_by(id=id).update(data)

    @classmethod
    def delete(cls, page):
        """Delete page by its id."""
        with db.session.begin_nested():
            db.session.delete(page)

    @classmethod
    def delete_all(cls):
        """Delete all pages."""
        cls.query.delete()

    @validates("template_name")
    def validate_template_name(self, key, value):
        """Validate template name.

        :param key: The template path.
        :param value: The template name.
        :raises ValueError: If template name is wrong.
        """
        if value not in dict(current_app.config["PAGES_TEMPLATES"]):
            raise ValueError('Template "{0}" does not exist.'.format(value))
        return value

    def __repr__(self):
        """Page representation.

        Used on Page admin view in inline model.
        :returns: unambiguous page representation.
        """
        return f"URL: {self.url}, title: {self.title}, language: {self.lang}"


class PageList(db.Model):
    """Represent association between page and list."""

    __versioned__ = {}

    __tablename__ = "pages_pagelist"

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    """PageList identifier."""

    list_id = db.Column(db.Integer, db.ForeignKey(PageModel.id), nullable=False)
    """Id of a list."""

    page_id = db.Column(db.Integer, db.ForeignKey(PageModel.id), nullable=False)
    """Id of a page."""

    order = db.Column(db.Integer, nullable=False)

    list = db.relationship(
        PageModel,
        backref=db.backref("pages", cascade="all, delete-orphan"),
        foreign_keys=[list_id],
    )
    """Relation to the list."""

    page = db.relationship(
        PageModel,
        backref=db.backref("lists", cascade="all, delete-orphan"),
        foreign_keys=[page_id],
    )
    """Relation to the page."""
