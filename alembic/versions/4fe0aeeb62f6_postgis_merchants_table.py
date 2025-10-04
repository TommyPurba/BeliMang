"""postgis + merchants table"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography

# --- Alembic identifiers ---
revision = "4fe0aeeb62f6"          # <-- biarkan sesuai nama file kamu
down_revision = "f6c436735538"      # <-- revision sebelumnya (add_files_table)
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable PostGIS (idempotent)
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    # Create merchants table
    op.create_table(
        "merchants",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(30), nullable=False),
        sa.Column("merchantCategory", sa.String(32), nullable=False),
        sa.Column("imageUrl", sa.String(255), nullable=False),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("long", sa.Float(), nullable=False),
        sa.Column(
            "geog",
            Geography(geometry_type="POINT", srid=4326),
            sa.Computed("ST_SetSRID(ST_MakePoint(long, lat), 4326)::geography", persisted=True),
            nullable=False,
        ),
    )

    # Spatial index on geog (safe if re-run)
    op.execute('CREATE INDEX IF NOT EXISTS ix_merchants_geog ON merchants USING GIST (geog)')


def downgrade() -> None:
    op.execute('DROP INDEX IF EXISTS ix_merchants_geog')
    op.drop_table("merchants")
