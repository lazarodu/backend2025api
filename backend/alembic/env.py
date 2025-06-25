from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from logging.config import fileConfig

from blog.infra.database import Base
from blog.infra.settings import DATABASE_URL
from blog.infra.models.user_model import UserModel
from blog.infra.models.post_model import PostModel
from blog.infra.models.comment_model import CommentModel

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata
print("DATABASE_URL:", DATABASE_URL)
def run_migrations_online():
    connectable = create_async_engine(DATABASE_URL, echo=True)

    async def do_migrations():
        async with connectable.begin() as connection:
            await connection.run_sync(
                lambda conn: context.configure(
                    connection=conn,
                    target_metadata=target_metadata,
                    literal_binds=True,
                    render_as_batch=True,
                )
            )
            context.run_migrations()

    import asyncio
    asyncio.run(do_migrations())

run_migrations_online()
