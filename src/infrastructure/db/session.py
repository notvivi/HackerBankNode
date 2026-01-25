from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from src.config.settings import config

DB_PATH = Path(config["database"]["sqlite_path"])
DB_PATH.parent.mkdir(exist_ok=True, parents=True)

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Sql commands output in terminal, DO NOT USE IN PRODUCTION!!!
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def get_session() -> AsyncSession:
    """
    Provide an async SQLAlchemy session for SQLite.

    Usage:
        async with get_session() as session:
            repo = AccountRepository(session)
            await repo.list_accounts()
    """
    async with AsyncSessionLocal() as session:
        yield session
