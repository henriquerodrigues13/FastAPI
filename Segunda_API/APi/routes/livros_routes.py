from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select
from Segunda_API.APi.database import get_session
from Segunda_API.APi.models import *
from uuid import UUID, uuid4

router = APIRouter(prefix='/livros', tags=['Livros'])

SessionDep = Annotated[Session, Depends(get_session)]

# GET - lista todos os livros
@router.get(path="/", response_model=list[LivroRespota])
async def listar_livros(session: SessionDep) -> list[LivroRespota]:
    livros = session.scalars(select(Livro)).all()

    return [LivroRespota.model_validate(livro) for livro in livros]

@router.get(path='/{livro_id}', response_model=LivroRespota,
         responses={404: {'description': 'Livro não encontrado'}})
async def obter_livro(livro_id: UUID, session: SessionDep) -> LivroRespota:
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
        editor=livro.editor,
        ano=livro.ano
    )

    session.add(livro_gravado)
    session.commit()
    session.refresh(livro_gravado)

    return LivroRespota.model_validate(livro_gravado)

@router.put('/{livro_id}', response_model=LivroRespota,
         responses={404: {"description": "Livro não encontrado"}})
async def atualizar_livro(livro_id: UUID, livro_update: LivroPut, session: SessionDep) -> LivroRespota:
    if livro := session.execute(select(Livro).where(Livro.uuid == livro_id)).scalar_one():
        for key, value in livro_update:
            setattr(livro, key, value)

        session.add(livro)
        session.commit()
        session.refresh(livro)

        return LivroRespota.model_validate(livro)

    raise HTTPException(status_code=404, detail='Livro não encontrado.')


@router.patch('/{livro_id}', response_model=LivroRespota,
         responses={404: {"description": "Livro não encontrado"},
                    400: {"description": "Nenhum dado válido enviado para atualização"}})
async def atualizar_parcial(livro_id: UUID, livro_update: LivroPatch, session: SessionDep) -> LivroRespota:

    updata_data = livro_update.model_dump(exclude_unset=True, exclude_none=True)

    if not updata_data :
        raise HTTPException(status_code=400, detail= "Nenhum dado válido enviado para atualização")

    if livro := session.execute(select(Livro).where(Livro.uuid == livro_id)).scalar_one():
        for key, value in updata_data.items():
            setattr(livro, key, value)

        session.add(livro)
        session.commit()
        session.refresh(livro)

        return LivroRespota.model_validate(livro)


    raise HTTPException(status_code=404, detail='Livro não encontrado.')


@router.delete('/{livro_id}', response_model=ConfirmaDelete,
            responses={404: {'description': 'Livro não encontrado.'}})
async def deletar_livro(livro_id: UUID, session: SessionDep) -> ConfirmaDelete:
    if livro := session.execute(select(Livro).where(Livro.uuid == livro_id)).scalar_one():
        titulo = livro.titulo

        session.delete(livro)
        session.commit()

        return ConfirmaDelete(mensagem=f'Livro {titulo} deletado.', uuid=livro_id)

    raise HTTPException(status_code=404, detail='Livro não encontrado.')
