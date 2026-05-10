from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Integer, String
from pydantic import BaseModel, ConfigDict
from uuid import UUID, uuid4

class Base(DeclarativeBase):
    pass


class Livro(Base):
    __tablename__ = "livrobase"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),default=uuid4, unique=True)
    autor: Mapped[str] = mapped_column(index=True)
    titulo: Mapped[str] = mapped_column(index=True)
    editor: Mapped[str]  = mapped_column(index=True)
    ano: Mapped[int] = mapped_column(index=True)

    def __repr__(self) -> str:
        return f"Livro(id={self.id}, titulo={self.titulo!r})"


class LivroBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    autor: str
    titulo: str
    editor: str
    ano: int


class LivroRespota(LivroBase):
    uuid: UUID

class LivroPost(LivroBase):
    ...

class LivroPut(LivroBase):
    ...

class LivroPatch(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    autor:   str | None = None
    titulo:  str | None = None
    editora: str | None = None
    ano:     int | None = None

class ConfirmaDelete(BaseModel):
    mensagem: str
    uuid:     UUID