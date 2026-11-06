import csv
import json
import time
from datetime import datetime

PONTOS_ALTA = 6
PONTOS_MEDIA = 3


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.caminho_historico = "data/historico.json"
        self.caminho_csv = "data/atendimentos.csv"
        self.historico = []
        self.atendimentos_sessao = []
        self.carregar_historico()

    def carregar_historico(self):
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                self.historico = json.load(arquivo)
        except FileNotFoundError:
            self.historico = []
        except json.JSONDecodeError:
            print("Aviso: historico.json estava corrompido, começando um histórico novo.")
            self.historico = []

    def salvar_historico(self):
        try:
            with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
                json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)
        except OSError:
            print("Não consegui salvar o histórico.")

    def ler_opcao(self, mensagem, maximo):
        while True:
            entrada = input(mensagem).strip()
            if entrada.isdigit() and int(entrada) <= maximo:
                return int(entrada)
            print(f"Opção inválida. Digite um número de 0 a {maximo}.")

    def ler_sim_nao(self, mensagem):
        while True:
            entrada = input(mensagem + " (s/n, 0 para voltar): ").strip().lower()
            if entrada == "s":
                return True
            if entrada == "n" or entrada == "0":
                return False
            print("Resposta inválida. Digite s, n ou 0.")

    def tem_dado_pessoal(self, texto):
        digitos = 0
        for caractere in texto:
            if caractere.isdigit():
                digitos += 1
        return digitos >= 8 or "@" in texto

    def confianca(self, pontos):
        if pontos >= PONTOS_ALTA:
            return "ALTA"
        return "MÉDIA"

    def sugerir_categorias(self):
        print("\nNão encontrei uma orientação para essa dúvida.")
        print("Tente outras palavras ou veja as categorias no menu:")
        for categoria in self.base.categorias():
            print(f"  - {categoria}")

    def mostrar_resultados(self, resultados):
        pontos, melhor = resultados[0]
        print(f"\nConfiança da resposta: {self.confianca(pontos)} ({pontos} pontos)")
        melhor.exibir()

        alternativas = []
        for item in resultados[1:3]:
            if item[0] >= PONTOS_MEDIA:
                alternativas.append(item[1])

        if len(alternativas) > 0:
            print("\nOutras orientações parecidas:")
            for i in range(len(alternativas)):
                print(f"  {i + 1} - {alternativas[i].titulo}")

        print()
        if self.ler_sim_nao("Essa orientação respondeu sua dúvida?"):
            return melhor, True

        if len(alternativas) > 0:
            opcao = self.ler_opcao("Quer ver uma das alternativas? Digite o número (0 para voltar): ",
                                   len(alternativas))
            if opcao != 0:
                escolhida = alternativas[opcao - 1]
                escolhida.exibir()
                print()
                if self.ler_sim_nao("Essa orientação respondeu sua dúvida?"):
                    return escolhida, True
        return melhor, False

    def perguntar(self):
        inicio = time.time()
        tentativas = 0
        ultima_pergunta = None
        ultima_orientacao = None

        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if pergunta == "0":
                break
            if pergunta == "":
                print("Você não digitou nada. Tente de novo.")
                continue
            if self.tem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            resultados = self.base.buscar(pergunta)

            if len(resultados) == 0 or resultados[0][0] < PONTOS_MEDIA:
                self.sugerir_categorias()
                ultima_pergunta = pergunta
                ultima_orientacao = None
            else:
                orientacao, ajudou = self.mostrar_resultados(resultados)
                if ajudou:
                    tempo = round(time.time() - inicio, 1)
                    self.registrar("pergunta", pergunta, orientacao, True, tentativas, tempo)
                    inicio = time.time()
                    tentativas = 0
                    ultima_pergunta = None
                    ultima_orientacao = None
                    continue
                ultima_pergunta = pergunta
                ultima_orientacao = orientacao

            if not self.ler_sim_nao("Quer tentar de novo com outras palavras?"):
                break

        if ultima_pergunta is not None:
            tempo = round(time.time() - inicio, 1)
            self.registrar("pergunta", ultima_pergunta, ultima_orientacao, False, tentativas, tempo)

    def navegar(self):
        categorias = self.base.categorias()
        while True:
            print("\n--- Categorias ---")
            for i in range(len(categorias)):
                print(f"{i + 1} - {categorias[i]}")
            print("0 - Voltar")
            opcao = self.ler_opcao("Escolha: ", len(categorias))
            if opcao == 0:
                return
            self.navegar_categoria(categorias[opcao - 1])

    def navegar_categoria(self, categoria):
        orientacoes = self.base.por_categoria(categoria)
        while True:
            print(f"\n--- {categoria} ---")
            for i in range(len(orientacoes)):
                print(f"{i + 1} - {orientacoes[i].titulo}")
            print("0 - Voltar")
            inicio = time.time()
            opcao = self.ler_opcao("Escolha: ", len(orientacoes))
            if opcao == 0:
                return
            orientacao = orientacoes[opcao - 1]
            orientacao.exibir()
            print()
            ajudou = self.ler_sim_nao("Essa orientação respondeu sua dúvida?")
            tempo = round(time.time() - inicio, 1)
            self.registrar("categoria", orientacao.titulo, orientacao, ajudou, 1, tempo)

    def registrar(self, origem, pergunta, orientacao, ajudou, tentativas, tempo):
        id_orientacao = None
        encontrou = False
        if orientacao is not None:
            id_orientacao = orientacao.id
            encontrou = True

        atendimento = {
            "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": tempo,
            "nota": None
        }
        self.historico.append(atendimento)
        self.atendimentos_sessao.append(atendimento)
        self.salvar_historico()

    def pedir_nota(self):
        if len(self.atendimentos_sessao) == 0:
            return
        while True:
            entrada = input("\nDe 1 a 5, quão fácil foi usar o assistente? (0 para pular): ").strip()
            if entrada == "0":
                return
            if entrada in ["1", "2", "3", "4", "5"]:
                for atendimento in self.atendimentos_sessao:
                    atendimento["nota"] = int(entrada)
                self.salvar_historico()
                return
            print("Nota inválida. Digite um número de 1 a 5.")

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("\nAinda não tem atendimento registrado.")
            return

        encontrados = 0
        ajudaram = 0
        soma_tentativas = 0
        tempos = []
        notas = []
        sem_solucao = []

        for atendimento in self.historico:
            soma_tentativas += atendimento["tentativas"]
            if atendimento["encontrou"]:
                encontrados += 1
                tempos.append(atendimento["tempo_segundos"])
            if atendimento["ajudou"]:
                ajudaram += 1
            elif atendimento["pergunta"] not in sem_solucao:
                sem_solucao.append(atendimento["pergunta"])
            if atendimento["nota"] is not None:
                notas.append(atendimento["nota"])

        print(f"\n--- Indicadores ({total} atendimentos) ---")
        print(f"Resposta encontrada: {encontrados / total * 100:.1f}%")
        print(f"Taxa de acerto (ajudou): {ajudaram / total * 100:.1f}%")
        if len(tempos) > 0:
            print(f"Tempo médio para encontrar: {sum(tempos) / len(tempos):.1f} segundos")
        print(f"Tentativas por atendimento: {soma_tentativas / total:.1f}")
        if len(notas) > 0:
            print(f"Facilidade de uso (1 a 5): {sum(notas) / len(notas):.1f}")
        else:
            print("Facilidade de uso (1 a 5): sem notas ainda")
        print("Dúvidas sem solução:")
        if len(sem_solucao) == 0:
            print("  nenhuma")
        for pergunta in sem_solucao:
            print(f"  - {pergunta}")

    def exportar_csv(self):
        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                  "ajudou", "tentativas", "tempo_segundos", "nota"]
        try:
            with open(self.caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(self.historico)
            print(f"\nCSV exportado em {self.caminho_csv} ({len(self.historico)} atendimentos).")
        except OSError:
            print("\nNão consegui salvar o CSV. Veja se ele não está aberto no Excel.")
