# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2024 CERN.
# Copyright (C) 2023-2024 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Views for Pages module."""

from flask import Blueprint, abort, current_app, g, render_template, request
from invenio_db import db
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.exceptions import NotFound

from .proxies import current_pages_service
from .records.models import PageModel as Page

blueprint = Blueprint(
    "invenio_pages", __name__, url_prefix="/", template_folder="templates"
)


@blueprint.app_template_filter("render_string")
def render_string(source):
    """Render a string in sandboxed environment.

    :param source: A string containing the page source.
    :returns: The rendered template.
    """
    return current_app.extensions["invenio-pages"].render_template(source)


def handle_not_found(exception, **extra):
    """Custom blueprint exception handler."""
    assert isinstance(exception, NotFound)

    page = Page.query.filter(
        db.or_(Page.url == request.path, Page.url == request.path + "/")
    ).first()
    if page:
        add_url_rule(page.url)
        return render_template(
            [page.template_name, current_app.config["PAGES_DEFAULT_TEMPLATE"]],
            page=page,
        )
    elif "wrapped" in extra:
        return extra["wrapped"](exception)
    else:
        return exception


def add_url_rule(url, app=None):
    """Register URL rule to application URL map."""
    rule = current_app.url_rule_class(
        url,
        endpoint="invenio_pages.view",
        methods=["GET", "HEAD", "OPTIONS"],
        strict_slashes=True,
        merge_slashes=True,
    )
    current_app.url_map.add(rule)


def create_pages_api_bp(app):
    """Create the pages resource api blueprint."""
    ext = app.extensions["invenio-pages"]
    return ext.pages_resource.as_blueprint()


def render_page(path, **template_ctx):
    """Internal interface to the page view.

    :param path: Page path.
    :param template_ctx: Passed to the rendered template.
    :returns: The rendered template.
    """
    try:
        page = current_pages_service.read_by_url(g.identity, request.path).to_dict()
    except NoResultFound:
        abort(404)
    return render_template(
        [page["template_name"], current_app.config["PAGES_DEFAULT_TEMPLATE"]],
        page=page,
        **template_ctx,
    )


def create_page_view(page_path):
    """Create a page view.

    .. code-block:: python

        app = Flask(__name__)
        app.add_url_rule("/about", view_func=create_page_view("/about"))

    """

    def _view():
        """Public interface to the page view.

        Models: `pages.pages`.
        Templates: Uses the template defined by the ``template_name`` field
        or ``pages/default.html`` if template_name is not defined.
        Context: page `pages.pages` object.
        """
        return render_page(page_path)

    return _view
