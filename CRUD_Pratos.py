
import json
import os
import terminal_bonito

POSSIVEIS_CATEGORIAS = ["Aperitivos", "Prato Principal", "Sobremesa", "Bebidas", "Bebidas Alcoólica"]

print("Módulo carregado:", terminal_bonito.__file__)

arquivo = os.path.join(os.path.dirname(__file__), os.pardir, 'dados/cardapio.json')

def carregar_cardapio():
    if not os.path.exists(arquivo):
        with open(arquivo, 'w') as f:
            json.dump({}, f)
    with open(arquivo, 'r') as f:
        return json.load(f)

def salvar_cardapio(cardapio):
    with open(arquivo, "w") as f:
        json.dump(cardapio, f, indent=4, ensure_ascii=False)


def criar_novo_item():
    nome = str(terminal_bonito.input_bonito("Insira aqui o nome do novo prato a ser adicionado ao cardápio: "))

    while True:
        try:
            preco = float(terminal_bonito.input_bonito("Insira aqui o valor do prato: "))
            if preco < 0:
                terminal_bonito.print_bonito("Preço não pode ser negativo. Tente novamente.")
            else:
                break
        except ValueError:
            terminal_bonito.print_bonito("Preço inválido. Digite um número válido.")

    while True:
        terminal_bonito.print_bonito("Categorias disponíveis:")
        for idx, cat in enumerate(POSSIVEIS_CATEGORIAS, 1):
            terminal_bonito.print_bonito(f"{idx}. {cat}")

        escolha = terminal_bonito.input_bonito("Escolha a categoria pelo número ou nome correspondente: ").strip()

        if escolha.isdigit():
            escolha_num = int(escolha)
            if 1 <= escolha_num <= len(POSSIVEIS_CATEGORIAS):
                categoria = POSSIVEIS_CATEGORIAS[escolha_num - 1]
                break
            else:
                terminal_bonito.print_bonito("Número inválido. Tente novamente.")
        else:
            escolha_formatada = escolha.lower()
            encontrado = None
            for cat in POSSIVEIS_CATEGORIAS:
                if escolha_formatada == cat.lower():
                    encontrado = cat
                    break
            if encontrado:
                categoria = encontrado
                break
            else:
                terminal_bonito.print_bonito("Categoria inválida. Tente novamente.")

    descricao = terminal_bonito.input_bonito("Descreva o prato: ")

    ingredientes = terminal_bonito.input_bonito("Liste os ingredientes separados por vírgula: ")
    lista_ingredientes = [ingred.strip() for ingred in ingredientes.split(",") if ingred.strip()]

    cardapio = carregar_cardapio()

    try:
        proximo_id = max([int(x) for x in cardapio.keys()]) + 1
    except ValueError:
        proximo_id = 1

    cardapio[str(proximo_id)] = {
        "nome": nome,
        "preco": preco,
        "categoria": categoria,
        "descricao": descricao,
        "ingredientes": lista_ingredientes
    }
    salvar_cardapio(cardapio)
    terminal_bonito.print_bonito("Prato salvo com sucesso.")



def listar_pratos():
    cardapio = carregar_cardapio()
    if not cardapio:
        terminal_bonito.print_bonito("Sem itens salvo no sistema")
        return
    terminal_bonito.print_bonito("Itens listados:")
    for i, prato in cardapio.items():
        terminal_bonito.print_bonito(f"{i} - {prato['nome']} | R${prato['preco']:.2f} | Categoria: {prato['categoria']}")
        terminal_bonito.print_bonito(f"  Descrição: {prato.get('descricao', 'N/A')}")
        ingredientes = prato.get('ingredientes', [])
        ingredientes_str = ', '.join(ingredientes) if ingredientes else 'N/A'
        terminal_bonito.print_bonito(f"  Ingredientes: {ingredientes_str}")
        terminal_bonito.print_bonito("-" * 40)

def atualizar_item():
    cardapio = carregar_cardapio()
    listar_pratos()
    try:
        numero = terminal_bonito.input_bonito("Digite o número do prato que deseja atualizar: ")
        if numero in cardapio:
            nome = terminal_bonito.input_bonito("Digite o novo nome: ")

            while True:
                try:
                    preco = float(terminal_bonito.input_bonito("Digite o novo preço: "))
                    if preco < 0:
                        terminal_bonito.print_bonito("Preço não pode ser negativo. Tente novamente.")
                    else:
                        break
                except ValueError:
                    terminal_bonito.print_bonito("Preço inválido. Digite um número válido.")

            categoria = terminal_bonito.input_bonito("Digite a nova categoria: ")
            descricao = terminal_bonito.input_bonito("Digite a nova descrição: ")
            ingredientes = terminal_bonito.input_bonito("Digite os ingredientes separados por vírgula: ")
            lista_ingredientes = [ingred.strip() for ingred in ingredientes.split(",") if ingred.strip()]

            cardapio[numero] = {
                "nome": nome,
                "preco": preco,
                "categoria": categoria,
                "descricao": descricao,
                "ingredientes": lista_ingredientes
            }
            salvar_cardapio(cardapio)
            terminal_bonito.print_bonito("Mudança feita com sucesso")
        else:
            terminal_bonito.print_bonito("Número inválido.")
    except (ValueError, IndexError):
        terminal_bonito.print_bonito("Entrada inválida.")

def deletar_item():
    cardapio = carregar_cardapio()
    listar_pratos()
    try:
        indice = terminal_bonito.input_bonito("Digite o número do prato que deseja deletar: ")
        if indice in cardapio:
            confirm = terminal_bonito.input_bonito(f"Tem certeza que deseja excluir este prato? '{cardapio[indice]['nome']}'? (s/n): ").lower()
            if confirm == 's':
                del cardapio[indice]
                salvar_cardapio(cardapio)
                terminal_bonito.print_bonito("Prato excluído com sucesso.")
            else:
                terminal_bonito.print_bonito("Exclusão cancelada.")
        else:
            terminal_bonito.print_bonito("Número inválido.")
    except (ValueError, IndexError):
        terminal_bonito.print_bonito("Entrada inválida.")

def menu():
    while True:
        terminal_bonito.print_bonito("\nMENU DO SISTEMA")
        terminal_bonito.print_bonito("1. Criar prato")
        terminal_bonito.print_bonito("2. Listar pratos")
        terminal_bonito.print_bonito("3. Atualizar prato")
        terminal_bonito.print_bonito("4. Deletar prato")
        terminal_bonito.print_bonito("5. Sair")
        opcao = terminal_bonito.input_bonito("Escolha uma opção: ")

        if opcao == '1':
            criar_novo_item()
        elif opcao == '2':
            listar_pratos()
        elif opcao == '3':
            atualizar_item()
        elif opcao == '4':
            deletar_item()
        elif opcao == '5':
            terminal_bonito.print_bonito("Encerrando o sistema. Até logo!")
            break
        else:
            terminal_bonito.print_bonito("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu()
