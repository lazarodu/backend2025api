import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
from pathlib import Path

# Load .env
load_dotenv(dotenv_path=Path(".env"))

# Alembic Config
config = context.config
fileConfig(config.config_file_name)

# Use env var for DB URL
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise Exception("DATABASE_URL not found in .env")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Target metadata
from blog.infra.database import Base 
from blog.infra.models.user_model import UserModel
from blog.infra.models.post_model import PostModel
from blog.infra.models.comment_model import CommentModel


target_metadata = Base.metadata
