"""create merchants (with PostGIS)"""

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geography

# --- Alembic IDs ---
revision = "927adf1ae040"               # biarkan sesuai nama file
down_revision = "86339da44c66"     # <-- ikut revision yang barusan kamu jalankan
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Pastikan PostGIS aktif
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    # Buat tabel merchants
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

    # Index spasial
    op.execute('CREATE INDEX IF NOT EXISTS ix_merchants_geog ON merchants USING GIST (geog)')


def downgrade() -> None:
    op.execute('DROP INDEX IF EXISTS ix_merchants_geog')
    op.drop_table("merchants")
