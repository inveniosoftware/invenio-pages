# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Views for Pages module."""

from __future__ import absolute_import, print_function

import six
from flask import Blueprint, abort, current_app, render_template, request
from invenio_db import db
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound

from .models import Page

blueprint = Blueprint(
    'invenio_pages',
    __name__,
    url_prefix='/',
    template_folder='templates'
)


@blueprint.before_app_first_request
def preload_pages():
    """Register all pages before the first application request."""
    try:
        _add_url_rule([page.url for page in Page.query.all()])
    except Exception:  # pragma: no cover
        current_app.logger.warn('Pages were not loaded.')
        raise


@blueprint.app_template_filter('render_string')
def render_string(source):
    """Render a string in sandboxed environment.

    :param source: A string containing the page source.
    :returns: The rendered template.
    """
    return current_app.extensions['invenio-pages'].render_template(source)


def view():
    """Public interface to the page view.

    Models: `pages.pages`.
    Templates: Uses the template defined by the ``template_name`` field
    or ``pages/default.html`` if template_name is not defined.
    Context: page `pages.pages` object.
    """
    return render_page(request.path)  # pragma: no cover


def render_page(path):
    """Internal interface to the page view.

    :param path: Page path.
    :returns: The rendered template.
    """
    try:
        page = Page.get_by_url(request.path)
    except NoResultFound:
        abort(404)

    return render_template(
        [page.template_name, current_app.config['PAGES_DEFAULT_TEMPLATE']],
        page=page)


def handle_not_found(exception, **extra):
    """Custom blueprint exception handler."""
    assert isinstance(exception, NotFound)

    page = Page.query.filter(db.or_(Page.url == request.path,
                                    Page.url == request.path + "/")).first()

    if page:
        _add_url_rule(page.url)
        return render_template(
            [
                page.template_name,
                current_app.config['PAGES_DEFAULT_TEMPLATE']
            ],
            page=page
        )
    elif 'wrapped' in extra:
        return extra['wrapped'](exception)
    else:
        return exception


def _add_url_rule(url_or_urls):
    """Register URL rule to application URL map."""
    old = current_app._got_first_request
    # This is bit of cheating to overcome @flask.app.setupmethod decorator.
    current_app._got_first_request = False
    if isinstance(url_or_urls, six.string_types):
        url_or_urls = [url_or_urls]
    map(lambda url: current_app.add_url_rule(url, 'invenio_pages.view', view),
        url_or_urls)
    current_app._got_first_request = old
