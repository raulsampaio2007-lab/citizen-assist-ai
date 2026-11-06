from assistente import Assistente
from base_conhecimento import BaseConhecimento


def menu(assistente):
    while True:
        print(f"\n===== {assistente.nome} =====")
        print("Orientação para jovens no primeiro emprego")
        print("Este assistente não é canal oficial e não pede dados pessoais.")
        print("1 - Digitar minha dúvida")
        print("2 - Ver as categorias")
        print("3 - Ver os indicadores")
        print("4 - Exportar atendimentos para CSV")
        print("0 - Sair")
        opcao = assistente.ler_opcao("Escolha: ", 4)

        if opcao == 1:
            assistente.perguntar()
        elif opcao == 2:
            assistente.navegar()
        elif opcao == 3:
            assistente.indicadores()
        elif opcao == 4:
            assistente.exportar_csv()
        else:
            assistente.pedir_nota()
            assistente.exportar_csv()
            print("Até mais!")
            return


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    if not base.carregar():
        print("Sem a base de conhecimento o assistente não consegue responder. Encerrando.")
        return

    assistente = Assistente("Citizen Assist AI", base)
    try:
        menu(assistente)
    except (KeyboardInterrupt, EOFError):
        print("\nAtendimento encerrado.")


main()
