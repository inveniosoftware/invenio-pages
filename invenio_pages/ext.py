# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Static pages module for Invenio."""

from flask import url_for
from jinja2.sandbox import SandboxedEnvironment
from werkzeug.exceptions import NotFound

from . import config
from .views import handle_not_found


class _InvenioPagesState(object):
    """State object for Invenio Pages."""

    def __init__(self, app):
        """Initialize state.

        :param app: The Flask application.
        """
        self.app = app
        self._jinja_env = None

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
            app.error_handler_spec[None][404][
                NotFound
            ] = lambda error: handle_not_found(error, wrapped=existing_handler)
        else:
            app.error_handler_spec.setdefault(None, {}).setdefault(404, {})
            app.error_handler_spec[None][404][NotFound] = handle_not_found

    def init_app(self, app):
        """Flask application initialization.

        :param app: The Flask application.
        :returns: The :class:`invenio_pages.ext.InvenioPages` instance
            initialized.
        """
        self.init_config(app)

        self.wrap_errorhandler(app)
        app.extensions["invenio-pages"] = _InvenioPagesState(app)

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


class InvenioPagesREST(InvenioPages):
    """Invenio App ILS REST API app."""
