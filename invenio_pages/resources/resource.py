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
    request_data,
    request_headers,
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
        super().__init__(config)
        self.service = service

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        return [
            route("POST", routes["list"], self.create),
            route("GET", routes["item"], self.read),
            route("GET", routes["list"], self.search),
            route("DELETE", routes["item"], self.delete),
            route("PUT", routes["item"], self.update),
        ]

    #
    # Primary Interface
    #
    @request_data
    @response_handler()
    def create(self):
        """Create a page."""
        page = self.service.create(
            identity=g.identity,
            data=resource_requestctx.data or {},
        )
        return page.to_dict(), 201

    @request_view_args
    @response_handler()
    def read(self):
        """Read a page."""
        item = self.service.read(
            identity=g.identity,
            id=resource_requestctx.view_args["id"],
        )
        return item.to_dict(), 200

    @request_search_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over pages."""
        pages = self.service.search(
            identity=g.identity,
            params=resource_requestctx.args,
        )
        return pages.to_dict(), 200

    @request_view_args
    @request_data
    @response_handler()
    def update(self):
        """Update a page."""
        id = resource_requestctx.view_args["id"]
        page = self.service.update(
            identity=g.identity,
            data=resource_requestctx.data,
            id=id,
        )

        return page.to_dict(), 200

    @request_headers
    @request_view_args
    def delete(self):
        """Delete a page."""
        id = resource_requestctx.view_args["id"]
        page = self.service.delete(
            id=id,
            identity=g.identity,
        )

        return page.to_dict(), 204
