# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2023 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

r"""Static pages for Invenio.

Invenio-Pages provides means to add static pages to Invenio. 
Once the module is installed, developers will be able to customise
their Invenio instance by registering custom static pages in a 
``pages.yaml`` file.
Define static pages
----------
To add static pages, the developer must create (if it doesn’t exist) a 
pages.yaml file inside the app_data folder of their instance folder.
.. code-block:: python
    <your_site>/
    └──app_data/
        └── pages.yaml
Once the file is created the developer has to define in it the static 
pages it wishes to create, using the following format for each page:
.. code-block:: python
    - url: "<URL used to access the page>"  # e.g. "/about"
      title: "<Title of the page>"  # e.g. "About"
      description: "<Description of the content of the page (won’t appear on the page itself)>"  # e.g. "About page"
      template: "<HTML template with the content of the page>"  # e.g. "about.html"
All the templates defined in this pages.yaml file should be created 
inside a pages folder inside the app_data folder of their instance folder.
.. code-block:: python
    <your_site>/
    └──app_data/
            └── pages/
                    └── about.html
                    └── …
Create pages
----------
Once the static pages have been defined, they can be created in two ways.
- Creating all the data of the instance by running the ``invenio-cli 
services setup`` command on the instance root. In case the data was already 
created, the ``invenio-cli services setup –force`` command should be used 
instead.
- Creating only the pages by running the ``pipenv run invenio rdm pages 
create`` on the instance root.
"""

from .ext import InvenioPages, InvenioPagesREST
from .records.models import PageList, PageModel

__version__ = "2.0.0"

__all__ = ("__version__", "InvenioPages", "InvenioPagesREST", "PageModel", "PageList")
