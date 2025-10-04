# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context

# 1) Konfigurasi logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2) Import Base & engine dari modul merchants
#    Pastikan path kerja saat menjalankan Alembic adalah root project, sehingga import "src..." valid.
from src.merchants.database import Base, engine
from src.merchants import models  # noqa: F401  <-- penting: ini mendaftarkan tabel2 ke Base.metadata

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Offline mode: menghasilkan SQL tanpa koneksi DB."""
    url = str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,      # bandingkan perubahan tipe kolom
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online mode: menjalankan migrasi langsung ke DB."""
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
