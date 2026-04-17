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

def menu():
    while True:
        print('\n=== CLIENTE API DE LIVROS ===')
        print("1. Listar Livros")
        print('2. Obter livro por UUID')
        print('0. Sair')

        opcao = input('Escolha a opção: ').strip()

        if opcao == '1':
            listar_livros()
        elif opcao == '2':
            obter_livro()
        elif opcao == '0':
            print("Encerrando cliente ...")
            break

if __name__ == "__main__":
    menu()
