import os
import terminal_bonito
from cruds import crud_mesas as mesas
from cruds import crud_pratos as pratos
from cruds import crud_pedidos as pedidos


def menu_inicial():
    terminal_bonito.limpar_terminal()
    terminal_bonito.linha_horizontal()
    terminal_bonito.print_bonito("BEM VINDO AO SISTEMA RESTAURANTE SOLUTIONS™")
    terminal_bonito.print_bonito("""
    1 - MÓDULO MESAS
    2 - MÓDULO PRATOS
    3 - MÓDULO PEDIDOS
    4 - SAIR
    """)

def main():

    entrada_invalida = False
    while True:
        terminal_bonito.limpar_terminal()
        menu_inicial()
        terminal_bonito.linha_horizontal()
        if entrada_invalida:
            terminal_bonito.print_bonito("OPÇÃO INVÁLIDA. TENTE NOVAMENTE!")
        opcao_inicial = int(terminal_bonito.input_bonito("INFORME SUA OPÇÃO: "))
        terminal_bonito.limpar_terminal()

        terminal_bonito.linha_horizontal()

        match opcao_inicial:
            case 1:
                mesas.menu()
                pass
            case 2:
                pratos.menu()
            case 3:
                pedidos.menu_pedidos()
            case 4:
                print("SAINDO...")
                break
            case __:
                entrada_invalida = True


if __name__ == "__main__":
    main()
