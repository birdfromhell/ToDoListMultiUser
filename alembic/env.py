from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Impor Base dari models Anda
from models import Base

# Ini adalah objek Config Alembic, yang memberikan
# akses ke nilai-nama dalam file .ini yang sedang digunakan.
config = context.config

# Interpretasikan file konfigurasi untuk logging Python.
# Baris ini mengatur logger pada dasarnya.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tambahkan objek MetaData model Anda di sini
# untuk dukungan 'autogenerate'
target_metadata = Base.metadata


# Nilai lain dari config, yang ditentukan oleh kebutuhan env.py,
# bisa diperoleh:
# my_important_option = config.get_main_option("my_important_option")
# ... dll.
def run_migrations_offline():
    """Jalankan migrasi dalam mode 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Jalankan migrasi dalam mode 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
