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

from __future__ import absolute_import, print_function

from flask import url_for
from jinja2.sandbox import SandboxedEnvironment

from . import config
from .views import handle_not_found


class _InvenioPagesState(object):
    """State object for Invenio Pages."""

    def __init__(self, app):
        """Initialize state."""
        self.app = app
        self._jinja_env = None

    @property
    def jinja_env(self):
        """Create a sandboxed Jinja environment."""
        if self._jinja_env is None:
            self._jinja_env = SandboxedEnvironment(
                extensions=[
                    'jinja2.ext.autoescape', 'jinja2.ext.with_', ],
                autoescape=True,
            )
            self._jinja_env.globals['url_for'] = url_for
            # Load whitelisted configuration variables.
            for var in self.app.config['PAGES_WHITELIST_CONFIG_KEYS']:
                self._jinja_env.globals[var] = self.app.config.get(var)
        return self._jinja_env

    def render_template(self, source, **kwargs_context):
        """Render a template string using sandboxed environment."""
        return self.jinja_env.from_string(source).render(
            kwargs_context)


class InvenioPages(object):
    """Invenio-Pages extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)

        try:
            existing_handler = app.error_handler_spec[None][404]
        except KeyError:
            existing_handler = None

        if existing_handler:
            app.error_handler_spec[None][404] = \
                lambda error: handle_not_found(error, wrapped=existing_handler)
        else:
            app.error_handler_spec[None][404] = handle_not_found

        app.extensions['invenio-pages'] = _InvenioPagesState(app)

        return app.extensions['invenio-pages']

    def init_config(self, app):
        """Initialize configuration."""
        app.config.setdefault(
            "PAGES_BASE_TEMPLATE",
            app.config.get("BASE_TEMPLATE",
                           "invenio_pages/base.html"))

        for k in dir(config):
            if k.startswith('PAGES_'):
                app.config.setdefault(k, getattr(config, k))
