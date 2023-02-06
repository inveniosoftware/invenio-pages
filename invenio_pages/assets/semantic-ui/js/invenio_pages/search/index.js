/*
 * This file is part of Invenio.
 * Copyright (C) 2023 CERN.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

import { initDefaultSearchComponents } from "@js/invenio_administration";
import { createSearchAppInit } from "@js/invenio_search_ui";
import { SearchResultItem } from "./SearchResultItem";
import { SearchResultsContainer } from "./SearchResultsContainer";
import { parametrize } from "react-overridable";
import _get from "lodash/get";
import { NotificationController } from "@js/invenio_administration";

const domContainer = document.getElementById("invenio-search-config");

const sortColumns = (columns) =>
  Object.entries(columns).sort((a, b) => a[1].order - b[1].order);
const title = JSON.parse(domContainer.dataset.title);
const resourceName = JSON.parse(domContainer.dataset.resourceName);
const columns = JSON.parse(domContainer.dataset.fields);
const sortedColumns = sortColumns(columns);
const displayEdit = JSON.parse(domContainer.dataset.displayEdit);
const displayDelete = JSON.parse(domContainer.dataset.displayDelete);
const displayRead = JSON.parse(domContainer.dataset.displayRead);
const actions = JSON.parse(domContainer.dataset.actions);
const apiEndpoint = _get(domContainer.dataset, "apiEndpoint");
const idKeyPath = JSON.parse(_get(domContainer.dataset, "pidPath", "pid"));
const listUIEndpoint = domContainer.dataset.listEndpoint;
const resourceSchema = JSON.parse(domContainer.dataset.resourceSchema);

const defaultComponents = initDefaultSearchComponents(domContainer);
const SearchResultItemWithConfig = parametrize(SearchResultItem, {
  title: title,
  resourceName: resourceName,
  columns: sortedColumns,
  displayRead: displayRead,
  displayEdit: displayEdit,
  displayDelete: displayDelete,
  actions: actions,
  apiEndpoint: apiEndpoint,
  idKeyPath: idKeyPath,
  listUIEndpoint: listUIEndpoint,
  resourceSchema: resourceSchema,
});

const ResultsContainerWithConfig = parametrize(SearchResultsContainer, {
  columns: sortedColumns,
  displayEdit: displayEdit,
  displayDelete: displayDelete,
  actions: actions,
});

const overridenComponents = {
  ...defaultComponents,
  "ResultsList.item": SearchResultItemWithConfig,
  "ResultsList.container": ResultsContainerWithConfig,
};

createSearchAppInit(
  overridenComponents,
  true,
  "invenio-search-config",
  false,
  NotificationController
);
