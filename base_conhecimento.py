import json

from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}


def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    # o "-" entrou aqui por causa de seguro-desemprego
    for sinal in "?!.,;:()-":
        texto = texto.replace(sinal, " ")
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.orientacoes = []
            for item in dados:
                orientacao = Orientacao(item["id"], item["categoria"], item["titulo"],
                                        item["palavras_chave"], item["resposta"],
                                        item["documentos"], item["onde"], item["fonte"],
                                        item["verificado_em"])
                self.orientacoes.append(orientacao)
            return True
        except FileNotFoundError:
            print(f"Erro: o arquivo {self.caminho} não foi encontrado.")
        except json.JSONDecodeError:
            print(f"Erro: o arquivo {self.caminho} está corrompido.")
        except (KeyError, TypeError):
            print(f"Erro: tem orientação com campo faltando em {self.caminho}.")
        return False

    def categorias(self):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria not in lista:
                lista.append(orientacao.categoria)
        return lista

    def por_categoria(self, categoria):
        lista = []
        for orientacao in self.orientacoes:
            if orientacao.categoria == categoria:
                lista.append(orientacao)
        return lista

    def pontuar(self, pergunta, orientacao):
        pergunta = normalizar(pergunta)
        titulo = normalizar(orientacao.titulo)
        pontos = 0
        for palavra_chave in orientacao.palavras_chave:
            if normalizar(palavra_chave) in pergunta:
                pontos += 3
        for palavra in pergunta.split():
            if len(palavra) >= 4 and " " + palavra + " " in titulo:
                pontos += 1
        return pontos

    def buscar(self, pergunta):
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda item: item[0], reverse=True)
        return resultados
