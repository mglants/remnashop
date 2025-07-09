from types import TracebackType
from typing import Optional, Self, Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.db.repositories import Repository


class UnitOfWork:
    session_pool: async_sessionmaker[AsyncSession]
    session: Optional[AsyncSession]

    def __init__(self, session_pool: async_sessionmaker[AsyncSession]):
        self.session_pool = session_pool
        self.session: Optional[AsyncSession] = None

    async def __aenter__(self) -> Self:
        self.session = await self.session_pool().__aenter__()
        self.repository = Repository(session=self.session)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self.session is None:
            return

        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

        await self.session.close()
        self.session = None

    async def commit(self) -> None:
        if self.session:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session:
            await self.session.rollback()
