# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Static pages module for Invenio."""

from flask import request, url_for
from jinja2.sandbox import SandboxedEnvironment
from werkzeug.exceptions import NotFound

from . import config
from .records.models import PageModel as Page
from .resources import PageResource, PageResourceConfig
from .services import PageService, PageServiceConfig
from .views import add_url_rule, handle_not_found, render_page


class InvenioPages(object):
    """Invenio-Pages extension."""

    def __init__(self, app=None):
        """Extension initialization.

        :param app: The Flask application. (Default: ``None``)
        """
        if app:
            self.init_app(app)

    @staticmethod
    def wrap_errorhandler(app):
        """Wrap error handler.

        :param app: The Flask application.
        """
        try:
            existing_handler = app.error_handler_spec[None][404][NotFound]
        except (KeyError, TypeError):
            existing_handler = None

        if existing_handler:
            app.error_handler_spec[None][404][NotFound] = (
                lambda error: handle_not_found(error, wrapped=existing_handler)
            )
        else:
            app.error_handler_spec.setdefault(None, {}).setdefault(404, {})
            app.error_handler_spec[None][404][NotFound] = handle_not_found

    @property
    def jinja_env(self):
        """Create a sandboxed Jinja environment."""
        if self._jinja_env is None:
            self._jinja_env = SandboxedEnvironment(
                autoescape=True,
            )
            self._jinja_env.globals["url_for"] = url_for
            # Load whitelisted configuration variables.
            for var in self.app.config["PAGES_WHITELIST_CONFIG_KEYS"]:
                self._jinja_env.globals[var] = self.app.config.get(var)
        return self._jinja_env

    def render_template(self, source, **kwargs_context):
        r"""Render a template string using sandboxed environment.

        :param source: A string containing the page source.
        :param \*\*kwargs_context: The context associated with the page.
        :returns: The rendered template.
        """
        return self.jinja_env.from_string(source).render(kwargs_context)

    def init_app(self, app):
        """Flask application initialization.

        :param app: The Flask application.
        :returns: The :class:`invenio_pages.ext.InvenioPages` instance
            initialized.
        """
        self.init_config(app)
        self.init_services(app)
        self.init_resources(app)
        self.wrap_errorhandler(app)
        app.extensions["invenio-pages"] = self

        return app.extensions["invenio-pages"]

    def init_config(self, app):
        """Initialize configuration.

        :param app: The Flask application.
        """
        app.config.setdefault(
            "PAGES_BASE_TEMPLATE",
            app.config.get("BASE_TEMPLATE", "invenio_pages/base.html"),
        )

        for k in dir(config):
            if k.startswith("PAGES_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        """Initialize the services for pages."""
        self.pages_service = PageService(config=PageServiceConfig)

    def init_resources(self, app):
        """Initialize the resources for pages."""
        self.pages_resource = PageResource(
            service=self.pages_service,
            config=PageResourceConfig,
        )


class InvenioPagesREST(InvenioPages):
    """Invenio App ILS REST API app."""


def finalize_app(app):
    """Finalize app."""
    register_pages(app)


def register_pages(app):
    """Register URL rule of all static pages to the application."""
    # We need to set the function view, to be able to directly register the urls
    # in the Flask.url_map
    app.view_functions["invenio_pages.view"] = view

    for page in Page.query.all():
        add_url_rule(page.url)


def view():
    """Public interface to the page view.

    Models: `pages.pages`.
    Templates: Uses the template defined by the ``template_name`` field
    or ``pages/default.html`` if template_name is not defined.
    Context: page `pages.pages` object.
    """
    return render_page(request.path)  # pragma: no cover
