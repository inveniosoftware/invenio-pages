..
    This file is part of Invenio.
    Copyright (C) 2015-2024 CERN.
    Copyright (C) 2024-2025 Graz University of Technology.
    Copyright (C) 2025 KTH Royal Institute of Technology.
    Copyright (C) 2026 Northwestern University.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Changes
=======

Version v7.3.0 (released 2026-01-15)

- refactor!: replace Link usage by EndpointLink
    PagesLink is removed but only used locally/low risk (see PR for details)

Version v7.2.1 (released 2025-10-21)

- i18n: pulled translations

Version v7.2.0 (released 2025-07-17)

- fix: setuptools require underscores instead of dashes
- i18n: pulled translations

Version v7.1.0 (released 2025-07-02)

- chore: fix classmethod argument names
- service: simplify search filtering logic
- fix: SADeprecationWarning

Version v7.0.0 (released 2025-6-03)

- setup: bump major dependencies
- fix: marshmallow DeprecationWarning
- fix: add configuration
- fix: setuptools require underscores instead of dashes
- i18n: removed deprecated messages

Version v6.0.0 (released 2025-03-26)

- global: add i18n support via "lang" column (#99)
    * Add support for multiple languages via the `lang` column.
    * Fix the tests and a bug that was uncovered thereby.
    * Adds alembic recipes

Version 5.0.0 (release 2024-12-10)

- comp: make compatible to flask-sqlalchemy>=3.1
- setup: bump major dependencies

Version 4.1.2 (release 2024-11-30)

- setup: change to reusable workflows
- setup: pin dependencies

Version v4.1.1 (released 2024-09-19)

- fix: add compatibility layer to move to flask>=3
- i18n: push translations

Version v4.1.0 (released 2024-08-07)

- http headers: use and adjust vnd.inveniordm.v1+json http accept header

Version 4.0.1 (released 2024-03-22)

- chore: fix CHANGES.rst format

Version 4.0.0 (released 2024-03-21)

- Major release because of fundamental change in the way the module is
  expected to be used for registering pages.
- global: remove `has_custom_view` model field
- views: allow passing Jinja context to `render_page`
- ext: remove finalize_app usage
    - The previous design of the module had some major usability issues:
        - The assumption that we have views that are dynamically registered
          without the need to redeploy/reload the application for code
          changes is fundamentally flawed. In reality order for such views
          to be accessible/discoverable, one has to be able to reference
          them in Jinja templates, which in turn means one has to make code
          changes.
        - The way we were registering page views, required having a
          connection to an already initialized database. This imposes having
          to perform checks at application initialization that go against
          well-established principles of the Flask/Invenio app lifecycle.
- fix: before_app_first_request deprecation

Version 3.3.0 (released 2024-02-21):
------------------------------------

- Add new DB column to pages table.
- Move to admin menu category site administration.

Version 3.2.0 (released 2023-11-30):
------------------------------------

- allow configuration for extra HTML tags and attributes when
  creating and editing static pages

Version 3.1.0 (released 2023-09-18):
------------------------------------

- schema: sanitize page content
- updated transifex config
- pulled latest translations

Version 3.0.1 (released 2023-03-09):
------------------------------------

- fix invenio-search dependencies

Version 3.0.0 (released 2023-03-09):
------------------------------------

- move the module to services/resources architecture
- add invenio-administration page
- remove deprecation of flask_babelex dependency


Version 2.0.0 (released 2023-01-25):
------------------------------------

- major release, tests cleanup
- License update
- global: refactor pages registration process
- Upgrade invenio packages
- Add alembic recipe
- Remove invenio-admin module


Version 2.0.0a2 (released 2023-01-20):
--------------------------------------

- License update
- global: refactor pages registration process

Version 2.0.0a1 (released 2023-01-05):
--------------------------------------

- Upgrade invenio packages
- Add alembic recipe
- Remove invenio-admin module


Version 1.0.0a5 (released 2020-04-14):
--------------------------------------

- Add REST API GET Static Page Resource
- Drop support for Python 2.7
- Update python dependencies


Version 1.0.0a4 (released 2017-08-18):
--------------------------------------

- Update minimum Flask version to 0.11.1.
- Improve documentation and examples.

Version 1.0.0a3 (released 2016-06-15):
--------------------------------------

- Major refactoring for Invenio 3.
- Adds versioning support for pages.


Version 0.1.2 (released 2015-10-07):
------------------------------------

- Removes calls to PluginManager consider_setuptools_entrypoints()
  removed in PyTest 2.8.0.
- Adds missing `invenio_base` dependency.

Version 0.1.1 (released 2015-08-25):
------------------------------------

- Adds missing `invenio_upgrader` dependency and amends past upgrade
  recipes following its separation into standalone package.
- Overrides default wtforms field for content column in order to
  display it properly. (closes inveniosoftware/invenio#3311)

Version 0.1.0 (released 2015-07-22):
------------------------------------

- Initial public release.
