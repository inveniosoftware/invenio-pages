# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Pytest configuration."""
import pytest
from invenio_access.models import ActionRoles
from invenio_access.permissions import superuser_access
from invenio_accounts.models import Role
from invenio_administration.permissions import administration_access_action
from invenio_app.factory import create_api

from invenio_pages import PageModel as Page


@pytest.fixture(scope="module")
def app(base_app, database):
    """Invenio application with only database.

    Scope: module
    """
    yield base_app


@pytest.fixture(scope="module")
def create_app(instance_path, entry_points):
    """Application factory fixture."""
    return create_api


@pytest.fixture(scope="function")
def pages_fixture(app, db):
    """Page fixtures.

    Scope: function
    """
    pages = [
        Page(
            url="/dogs",
            title="Page for Dogs!",
            content="Generic dog.",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/dogs/shiba",
            title="Page for doge!",
            content="so doge!",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/cows/",
            title="Page for Cows!",
            content="Generic cow.",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/htmldog",
            title="Page for modern dogs!",
            content="<h1>HTML aware dog.</h1>.\n" '<p class="test">paragraph<br /></p>',
            template_name="invenio_pages/default.html",
        ),
    ]
    for page in pages:
        db.session.add(page)
    db.session.commit()


@pytest.fixture(scope="module")
def module_scoped_pages_fixture(app, database):
    """Page fixtures.

    Scope: module
    """
    db = database
    pages = [
        Page(
            url="/dogs",
            title="Page for Dogs!",
            content="Generic dog.",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/dogs/shiba",
            title="Page for doge!",
            content="so doge!",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/cows/",
            title="Page for Cows!",
            content="Generic cow.",
            template_name="invenio_pages/default.html",
        ),
        Page(
            url="/htmldog",
            title="Page for modern dogs!",
            content="<h1>HTML aware dog.</h1>.\n" '<p class="test">paragraph<br /></p>',
            template_name="invenio_pages/default.html",
        ),
    ]
    for page in pages:
        db.session.add(page)
    db.session.commit()


@pytest.fixture(scope="function")
def superuser_role_need(db):
    """Store 1 role with 'superuser-access' ActionNeed."""
    role = Role(name="superuser-access")
    db.session.add(role)

    action_role = ActionRoles.create(action=superuser_access, role=role)
    db.session.add(action_role)

    db.session.commit()
    return action_role.need


@pytest.fixture()
def superuser(UserFixture, app, db, superuser_role_need):
    """Admin user for requests."""
    u = UserFixture(
        email="superuser@inveniosoftware.org",
        password="superuser",
    )
    u.create(app, db)

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(u.user, "superuser-access")

    datastore.add_role_to_user(u.user, role)
    db.session.commit()
    return u


@pytest.fixture()
def superuser_identity(superuser):
    """Superuser identity fixture."""
    identity = superuser.identity
    return identity


@pytest.fixture(scope="function")
def admin_role_need(db):
    """Store 1 role with 'administration-access' ActionNeed."""
    role = Role(name="administration-access")
    db.session.add(role)

    action_role = ActionRoles.create(action=administration_access_action, role=role)
    db.session.add(action_role)

    db.session.commit()
    return action_role.need


@pytest.fixture()
def admin(UserFixture, app, db, admin_role_need):
    """Admin user for requests."""
    u = UserFixture(
        email="admin@inveniosoftware.org",
        password="admin",
    )
    u.create(app, db)

    datastore = app.extensions["security"].datastore
    _, role = datastore._prepare_role_modify_args(u.user, "administration-access")

    datastore.add_role_to_user(u.user, role)
    db.session.commit()
    return u


@pytest.fixture()
def admin_user_identity(admin):
    """Simple identity fixture."""
    identity = admin.identity
    return identity


@pytest.fixture()
def user(UserFixture, app, db):
    """General user for requests."""
    user = UserFixture(email="user1@example.org", password="user1")
    user.create(app, db)

    return user


@pytest.fixture()
def simple_user_identity(user):
    """Simple identity fixture."""
    identity = user.identity
    return identity
