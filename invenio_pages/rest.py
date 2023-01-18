# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""REST API module of invenio-pages."""

from flask import Blueprint, abort
from invenio_rest import ContentNegotiatedMethodView
from sqlalchemy.orm.exc import NoResultFound

from invenio_pages import Page
from invenio_pages.serializers import page_response
from invenio_pages.serializers.links import default_links_item_factory

blueprint = Blueprint("invenio_pages_rest", __name__, url_prefix="/pages")


class PageDetailsResource(ContentNegotiatedMethodView):
    """Page details resource."""

    view_name = "rest_pages_list"

    def __init__(self, serializers=None, *args, **kwargs):
        """Constructor."""
        super(PageDetailsResource, self).__init__(serializers, *args, **kwargs)

    def get(self, page_id):
        """Get the details of requested page."""
        try:
            page = Page.get_by_id(page_id)
        except NoResultFound:
            abort(404)
        # check if the page got a new version
        etag = str(len(page.versions.all()))
        self.check_etag(etag)
        response = self.make_response(
            page, links_item_factory=default_links_item_factory
        )
        response.set_etag(etag)
        return response


serializers = {"application/json": page_response}


blueprint.add_url_rule(
    "/<string:page_id>",
    view_func=PageDetailsResource.as_view(
        "pages_item",
        serializers=serializers,
        default_media_type="application/json",
    ),
    methods=["GET"],
)
