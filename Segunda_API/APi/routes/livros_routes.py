from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from Segunda_API.APi.database import get_session
from Segunda_API.APi.models import LivroRespota, Livro, LivroPost
from uuid import UUID, uuid4

router = APIRouter(prefix='/livros', tags=['Livros'])

SessionDep = Annotated[Session, Depends(get_session)]

# GET - lista todos os livros
@router.get(path="/", response_model=list[LivroRespota])
async def listar_livros(session: SessionDep) -> list[LivroRespota]:
    livros = session.execute(select(Livro)).all()

    return [LivroRespota.model_validate(livro) for livro in livros]

@router.get(path='/{livro_id}', response_model=LivroRespota,
         responses={404: {'description': 'Livro não encontrado'}})
async def obter_livro(livro_id: UUID, session: SessionDep) -> Livro:
    if livro := session.execute(select(Livro).where(Livro.uuid == livro_id)).scalar_one():
        return LivroRespota.model_validate(livro)
    raise HTTPException(status_code=404,detail='Livro não encontrado')

@router.post('/', response_model=LivroRespota)
async def adicionar_livro(livro: LivroPost, session: SessionDep) -> LivroRespota:
    novo_uuid = uuid4()

    livro_gravado = Livro(
        uuid= novo_uuid,
        autor=livro.autor,
        titulo=livro.titulo,
        editora=livro.editora,
        ano=livro.ano
    )

    session.add(livro_gravado)
    session.commit()

    return LivroRespota.model_validate(livro_gravado)