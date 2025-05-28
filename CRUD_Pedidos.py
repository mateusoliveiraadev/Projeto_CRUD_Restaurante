import json
import os
from datetime import datetime
import terminal_bonito

arquivo_pedidos = os.path.join(os.path.dirname(__file__), os.pardir, 'dados/pedidos.json')
arquivo_cardapio = os.path.join(os.path.dirname(__file__), os.pardir, 'dados/cardapio.json')
arquivo_mesas = os.path.join(os.path.dirname(__file__), os.pardir, 'dados/mesas.json')

def carregar_json(caminho):
    if os.path.exists(caminho):
        with open(caminho, 'r') as f:
            return json.load(f)
    return {}

def salvar_json(dados, caminho):
    with open(caminho, 'w') as f:
        json.dump(dados, f, indent=4)

def verificar_item_cardapio(cardapio, id_item):
    return str(id_item) in cardapio
    
def verificar_mesa_existe(mesas, id_mesa):
    return str(id_mesa) in mesas

def ocupar_mesa(mesas, id_mesa):
    mesas[str(id_mesa)] = "ocupada"
    salvar_json(mesas, arquivo_mesas)

def criar_pedido():
    pedidos = carregar_json(arquivo_pedidos)
    cardapio = carregar_json(arquivo_cardapio)
    mesas = carregar_json(arquivo_mesas)

    while True:
        id_mesa = terminal_bonito.input_bonito("Número da mesa: ")
        if verificar_mesa_existe(mesas, id_mesa):
            break
        else:
            terminal_bonito.print_bonito("Número da mesa inválido. Tente novamente.")

    itens = []
    while True:
        id_item = terminal_bonito.input_bonito("ID do item do cardápio (0 para sair): ")
        if id_item == '0':
            break
        if not verificar_item_cardapio(cardapio, id_item):
            terminal_bonito.print_bonito("Item inválido.")
            continue

        quantidade = int(terminal_bonito.input_bonito("Quantidade: "))
        obs = terminal_bonito.input_bonito("Observação (opcional): ")

        itens.append({
            "id_cardapio": int(id_item),
            "quantidade": quantidade,
            "observacao": obs
        })

    if not itens:
        terminal_bonito.print_bonito("Pedido vazio. Cancelado.")
        return

    novo_id = str(max([int(k) for k in pedidos] + [0]) + 1)
    pedidos[novo_id] = {
        "mesa": int(id_mesa),
        "itens": itens,
        "status": "em preparo",
        "horario": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    ocupar_mesa(mesas, id_mesa)
    salvar_json(pedidos, arquivo_pedidos)
    terminal_bonito.print_bonito(f"Pedido {novo_id} criado com sucesso.")

def listar_pedidos():
    pedidos = carregar_json(arquivo_pedidos)
    cardapio = carregar_json(arquivo_cardapio)

    if not pedidos:
        terminal_bonito.print_bonito("Nenhum pedido encontrado.")
        return

    for pid, pedido in pedidos.items():
        terminal_bonito.print_bonito(f"\nPedido ID: {pid}")
        terminal_bonito.print_bonito(f" Mesa: {pedido['mesa']}")
        terminal_bonito.print_bonito(f" Status: {pedido['status']}")
        terminal_bonito.print_bonito(f" Horário: {pedido['horario']}")
        terminal_bonito.print_bonito(" Itens:")
        total = 0
        for item in pedido['itens']:
            id_item = str(item["id_cardapio"])
            nome = cardapio.get(id_item, {}).get("nome", "Desconhecido")
            preco = cardapio.get(id_item, {}).get("preco", 0.0)
            subtotal = preco * item["quantidade"]
            total += subtotal
            terminal_bonito.print_bonito(f"  - {nome} x{item['quantidade']} (R${subtotal:.2f}) - {item['observacao']}")
        terminal_bonito.print_bonito(f" Total: R${total:.2f}")
        terminal_bonito.linha_horizontal()

def atualizar_status_pedido():
    pedidos = carregar_json(arquivo_pedidos)
    if not pedidos:
        terminal_bonito.print_bonito("Nenhum pedido encontrado.")
        return

    id_pedido = terminal_bonito.input_bonito("ID do pedido a atualizar: ")
    if id_pedido not in pedidos:
        terminal_bonito.print_bonito("Pedido não encontrado.")
        return

    terminal_bonito.print_bonito("Status atual:" + "\n" + pedidos[id_pedido]["status"])
    terminal_bonito.print_bonito("1 - Em preparo")
    terminal_bonito.print_bonito("2 - Pronto")
    terminal_bonito.print_bonito("3 - Entregue")
    opcao = terminal_bonito.input_bonito("Novo status (1-3): ")

    status_map = {"1": "em preparo", "2": "pronto", "3": "entregue"}
    if opcao in status_map:
        pedidos[id_pedido]["status"] = status_map[opcao]
        salvar_json(pedidos, arquivo_pedidos)
        terminal_bonito.print_bonito("Status atualizado.")
    else:
        terminal_bonito.print_bonito("Opção inválida.")

def menu_pedidos():
    while True:
        terminal_bonito.print_bonito("\n=== MENU DE PEDIDOS ===")
        terminal_bonito.print_bonito("1. Criar novo pedido")
        terminal_bonito.print_bonito("2. Listar pedidos")
        terminal_bonito.print_bonito("3. Atualizar status de pedido")
        terminal_bonito.print_bonito("4. Voltar")
        opcao = terminal_bonito.input_bonito("Escolha uma opção: ")

        if opcao == '1':
            criar_pedido()
        elif opcao == '2':
            listar_pedidos()
        elif opcao == '3':
            atualizar_status_pedido()
        elif opcao == '4':
            break
        else:
            terminal_bonito.print_bonito("Opção inválida.")

if __name__ == "__main__":
    menu_pedidos()
