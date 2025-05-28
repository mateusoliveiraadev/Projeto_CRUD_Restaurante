

import json
import os
import terminal_bonito

arquivo = os.path.join(os.path.dirname(__file__), os.pardir,'dados/mesas.json')

TOTAL_MESAS = 10 

def carregar_mesas():
    if not os.path.exists(arquivo):
        mesas_iniciais = {str(i): "disponível" for i in range(1, TOTAL_MESAS + 1)}
        with open(arquivo, 'w') as f:
            json.dump(mesas_iniciais, f, indent=4, ensure_ascii=False)
    with open(arquivo, 'r') as f:
        return json.load(f)

def salvar_mesas(mesas):
    with open(arquivo, 'w') as f:
        json.dump(mesas, f, indent=4, ensure_ascii=False)

def mostrar_mesas():
    mesas = carregar_mesas()
    terminal_bonito.print_bonito("\nStatus de todas as mesas:")
    for num, status in mesas.items():
        terminal_bonito.print_bonito(f" Mesa {num}: {status.capitalize()}")
    print()

def mostrar_mesas_disponiveis():
    mesas = carregar_mesas()
    disponiveis = [num for num, status in mesas.items() if status == "disponível"]
    terminal_bonito.print_bonito("\nMesas disponíveis:")
    if disponiveis:
        terminal_bonito.print_bonito(" - " + ", ".join(disponiveis))
    else:
        terminal_bonito.print_bonito("Nenhuma mesa disponível no momento.")
    print()

def mostrar_mesas_reservadas():
    mesas = carregar_mesas()
    reservadas = [num for num, status in mesas.items() if status == "reservada"]
    terminal_bonito.print_bonito("\nMesas reservadas:")
    if reservadas:
        terminal_bonito.print_bonito(" - " + ", ".join(reservadas))
    else:
        terminal_bonito.print_bonito("Nenhuma mesa reservada no momento.")
    print()

def mostrar_mesas_ocupadas():
    mesas = carregar_mesas()
    ocupadas = [num for num, status in mesas.items() if status == "ocupada"]
    terminal_bonito.print_bonito("\nMesas ocupadas:")
    if ocupadas:
        terminal_bonito.print_bonito(" - " + ", ".join(ocupadas))
    else:
        terminal_bonito.print_bonito("Nenhuma mesa ocupada no momento.")
    print()

def reservar_mesa():
    mesas = carregar_mesas()
    mostrar_mesas_disponiveis()
    mesa = terminal_bonito.input_bonito("Digite o número da mesa para reservar: ")
    if mesas.get(mesa) == "disponível":
        mesas[mesa] = "reservada"
        terminal_bonito.print_bonito(f"Mesa {mesa} reservada com sucesso.")
    else:
        terminal_bonito.print_bonito("Mesa não está disponível para reserva.")
    salvar_mesas(mesas)

def ocupar_mesa():
    mesas = carregar_mesas()
    mostrar_mesas()
    mesa = terminal_bonito.input_bonito("Digite o número da mesa para ocupar: ")
    if mesas.get(mesa) in ["disponível", "reservada"]:
        mesas[mesa] = "ocupada"
        terminal_bonito.print_bonito(f"Mesa {mesa} agora está ocupada.")
    else:
        terminal_bonito.print_bonito("Mesa já está ocupada ou é inválida.")
    salvar_mesas(mesas)

def liberar_mesa():
    mesas = carregar_mesas()
    mostrar_mesas_ocupadas()
    mesa = terminal_bonito.input_bonito("Digite o número da mesa para liberar: ")
    if mesas.get(mesa) == "ocupada":
        mesas[mesa] = "disponível"
        terminal_bonito.print_bonito(f"Mesa {mesa} foi liberada com sucesso.")
    else:
        terminal_bonito.print_bonito("Essa mesa não está ocupada ou é inválida.")
    salvar_mesas(mesas)

def excluir_reserva():
    mesas = carregar_mesas()
    mostrar_mesas_reservadas()
    mesa = terminal_bonito.input_bonito("Digite o número da mesa para excluir a reserva: ")
    if mesas.get(mesa) == "reservada":
        mesas[mesa] = "disponível"
        terminal_bonito.print_bonito(f"Reserva da mesa {mesa} excluída.")
    else:
        terminal_bonito.print_bonito("Essa mesa não está reservada.")
    salvar_mesas(mesas)

def menu():
    while True:
        terminal_bonito.print_bonito("""
===== MENU =====
1. Mostrar status de todas as mesas
2. Mostrar apenas mesas disponíveis
3. Mostrar apenas mesas reservadas
4. Mostrar apenas mesas ocupadas
5. Reservar mesa
6. Ocupar mesa
7. Excluir reserva
8. Liberar mesa ocupada
9. Sair do sistema
""")
        opcao = terminal_bonito.input_bonito("Escolha uma opção: ")
        if opcao == "1":
            mostrar_mesas()
        elif opcao == "2":
            mostrar_mesas_disponiveis()
        elif opcao == "3":
            mostrar_mesas_reservadas()
        elif opcao == "4":
            mostrar_mesas_ocupadas()
        elif opcao == "5":
            reservar_mesa()
        elif opcao == "6":
            ocupar_mesa()
        elif opcao == "7":
            excluir_reserva()
        elif opcao == "8":
            liberar_mesa()
        elif opcao == "9":
            terminal_bonito.print_bonito("Saindo do sistema...")
            break
        else:
            terminal_bonito.print_bonito("Opção inválida. Tente novamente.")

# Iniciar o programa
if __name__ == "__main__":
    menu()

