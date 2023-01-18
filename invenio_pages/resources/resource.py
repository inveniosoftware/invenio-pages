# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Pages is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Pages module to create REST APIs."""

from flask import g
from flask_resources import Resource, resource_requestctx, response_handler, route
from invenio_records_resources.resources.records.resource import (
    request_extra_args,
    request_search_args,
    request_view_args,
)


#
# Resource
#
class PageResource(Resource):
    """Page resource."""

    def __init__(self, config, service):
        """Constructor."""
        super(PageResource, self).__init__(config)
        self.service = service

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        return [
            route("GET", routes["item"], self.read),
        ]

    #
    # Primary Interface
    #
    @request_extra_args
    @request_view_args
    @response_handler()
    def read(self):
        """Read a page."""
        item = self.service.read_id(
            id=resource_requestctx.view_args["id"],
            identity=g.identity,
        )
        return item.to_dict(), 200

    @request_extra_args
    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over pages."""
        # TODO: implement

        return [], 200
