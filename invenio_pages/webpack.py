# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio RDM Records is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for theme."""

from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    "assets",
    default="semantic-ui",
    themes={
        "semantic-ui": dict(
            entry={
                "invenio-pages-search": "./js/invenio_pages/search/index.js",
            },
            dependencies={
                "@babel/runtime": "^7.9.0",
                "@ckeditor/ckeditor5-build-classic": "^16.0.0",
                "@ckeditor/ckeditor5-react": "^2.1.0",
                "formik": "^2.1.0",
                "i18next": "^20.3.0",
                "i18next-browser-languagedetector": "^6.1.0",
                "luxon": "^1.23.0",
                "path": "^0.12.7",
                "prop-types": "^15.7.2",
                "react-copy-to-clipboard": "^5.0.0",
                "react-dnd": "^11.1.0",
                "react-dnd-html5-backend": "^11.1.0",
                "react-dropzone": "^11.0.0",
                "react-i18next": "^11.11.0",
                "react-invenio-deposit": "^1.0.0",
                "react-invenio-forms": "^1.0.0",
                "react-searchkit": "^2.0.0",
                "yup": "^0.32.0",
            },
            aliases={
                "@js/invenio_pages": "js/invenio_pages",
                "@translations/invenio_pages": "translations/invenio_pages",
            },
        ),
    },
)
