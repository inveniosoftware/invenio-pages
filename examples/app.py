# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Minimal Flask application example for development.

Run example development server:

.. code-block:: console

   $ cd examples
   $ python app.py
"""

from __future__ import absolute_import, print_function

import os

from flask import Flask
from invenio_db import InvenioDB, db

from invenio_pages import InvenioPages
from invenio_pages.models import Page
from invenio_pages.views import blueprint

# Create Flask application
app = Flask(__name__)

app.config.update(
    PAGES_TEMPLATES=[
        ('invenio_pages/default.html', 'Default'),
        ('app/mytemplate.html', 'App'),
    ],
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI',
                                      'sqlite:///app.db'),
)

InvenioDB(app)
InvenioPages(app)

app.register_blueprint(blueprint)


@app.cli.group()
def fixtures():
    """Command for working with test data."""


@fixtures.command()
def pages():
    """Load pages."""
    p1 = Page(
        url='/example1',
        title='My page with default template',
        description='my description',
        content='hello default page',
        template_name='invenio_pages/default.html',
    )
    p2 = Page(
        url='/example2',
        title='My page with my template',
        description='my description',
        content='hello my page',
        template_name='app/mytemplate.html',
    )
    with db.session.begin_nested():
        db.session.add(p1)
        db.session.add(p2)
    db.session.commit()
