#
# This file is part of Invenio.
# Copyright (C) 2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create invenio_pages branch"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98e0a418340d'
down_revision = None
branch_labels = ('invenio_pages',)
depends_on = "dbdbc1b19cf2"


def upgrade():
    """Upgrade database."""
    pass


def downgrade():
    """Downgrade database."""
    pass
