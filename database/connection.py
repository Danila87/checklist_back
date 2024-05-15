from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE

engine = create_async_engine(
                                url=f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}',
                                echo=False
                                  )

db_session = async_sessionmaker(engine)
