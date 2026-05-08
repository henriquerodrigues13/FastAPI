import requests
import json

API_URL= 'http://127.0.0.1:8000'

def tratar_resposta(resp: requests.Response):
    """Impririr de forma amigável respota da API, trantando erros."""
    try:
        data = resp.json()
    except ValueError:
        print(f'\nStatus: {resp.status_code}')
        print('resposta sem JSON.')
        print(resp.text)
        return
    
    if resp.status_code >= 400:
        print(f'\n Erro ({resp.status_code})')
    print(json.dumps(data, indent=4, ensure_ascii=False))

def listar_livros():
    resp = requests.get(f'{API_URL}/livros')
    print("\n Lista Livros:")
    tratar_resposta(resp)

def obter_livro():
    livro_uuid = input('UUID do livro: ').strip()
    resp = requests.get(f'{API_URL}/livros/{livro_uuid}')
    print('\nDetalhes do Livro:')
    tratar_resposta(resp)

def adicionar_livro():
    print('\nDigite os dados do novo livro:')
    autor = input('autor: ')
    titulo = input('título: ')
    editora = input('editora: ')
    ano = int(input('ano de publicação: '))

    payload ={
        'autor': autor,
        'titulo': titulo,
        'editora': editora,
        'ano': ano,
    }

    resp = requests.post(f'{API_URL}/livros/', json=payload)
    print('\n Livro Adicionado:')
    tratar_resposta(resp)

def atualizar_livro():
    livro_uuid = input("UUID do livro a atualizar (PUT): ").strip()
    
    print("\nDigite os NOVOS dados completos do livro:")
    autor = input('autor: ')
    titulo = input('título: ')
    editora = input('editora: ')
    ano = int(input('ano de publicação: '))

    payload ={
        'autor': autor,
        'titulo': titulo,
        'editora': editora,
        'ano': ano,
    }

    resp = requests.put(f'{API_URL}/livros/{livro_uuid}', json=payload)
    print('\n Livro Atualizado:')
    tratar_resposta(resp)

def atualizar_parcial():
    livro_uuid = input("UUID do livro a atualizar parcial(PATCH): ").strip()
    
    print("\nDigite APENAS os campos que deseja atualizar (deixe em branco para ignora):")
    autor = input('autor: ')
    titulo = input('título: ')
    editora = input('editora: ')
    ano = input('ano de publicação: ')

    payload ={}

    if autor:
        payload['autor'] = autor
    if editora:
        payload['editora'] = editora
    if titulo:
        payload['titula'] = titulo
    if ano:
        payload['ano'] = int(ano)
    resp = requests.patch(f'{API_URL}/livros/{livro_uuid}', json=payload)
    print('\n Livro Atualizado parcialmente (PATCH):')
    tratar_resposta(resp)

def deletar_livro():
    livro_uuid = input("UUID do livro a deletar (DELETE): ").strip()
    resp = requests.delete(f'{API_URL}/livros/{livro_uuid}')

    print('\n Resultado da exclusão (PATCH):')
    tratar_resposta(resp)

def menu():
    while True:
        print('\n=== CLIENTE API DE LIVROS ===')
        print("1. Listar Livros")
        print('2. Obter livro por UUID')
        print('3. adicionar livro(POST)')
        print('4. Atualizar livro inteiro (PUT)')
        print('5. Atualizar parcial (PATCH)')
        print('6. Deletar livro (DELETE)')
        print('0. Sair')

        opcao = input('Escolha a opção: ').strip()

        if opcao == '1':
            listar_livros()
        elif opcao == '2':
            obter_livro()
        elif opcao == '3':
            adicionar_livro()
        elif opcao == '4':
            atualizar_livro()
        elif opcao == '5':
            atualizar_parcial()
        elif opcao == '6':
            deletar_livro()
        elif opcao == '0':
            print("Encerrando cliente ...")
            break
        else:
            print('\n Opção invávida!')

if __name__ == "__main__":
    menu()
