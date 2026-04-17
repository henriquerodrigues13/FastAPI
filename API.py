from uuid import UUID, uuid4
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List


app = FastAPI(title='API de Livros')

livros_db = {
    1: {
        "uuid": uuid4(),
        "autor": "George Orwell",
        "titulo": "1984",
        "editora": "Companhia das Letras",
        "ano": 1949
    },
    2: {
        "uuid": uuid4(),
        "autor": "J. K. Rowling",
        "titulo": "Harry Potter e a Pedra Filosofal",
        "editora": "Rocco",
        "ano": 1997
    }
}


class Livro(BaseModel):
    uuid: UUID
    autor: str
    titulo: str
    editora: str
    ano: int

# GET - lista todos os livros
@app.get(path="/livros", response_model=List[Livro])
async def listar_livros():
    return [Livro(**dados) for dados in livros_db.values()]

@app.get(path='/livros/{livro_id}', response_model=Livro,
         responses={404: {'description': 'Livro não encontrado'}})
async def obter_livro(livro_id: UUID) -> Livro:
    for livro in livros_db.values():
        if livro['uuid'] == livro_id:
            return Livro(**livro)
        
    raise HTTPException(status_code=400,
                        detail='Livro não encontrado')